#  ================================================================================================================# 
# # ===============================================================================================================# 
# # Copyright 2024 Infosys Ltd.                                                                                    # 
# # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # 
# # http://www.apache.org/licenses/                                                                                # 
#  ================================================================================================================# 

from re import L
import re
import anthropic
import cachetools
import math
import openai
import json
import requests
import sseclient
import urllib
import traceback
import logging
import base64

from aleph_alpha_client import Client as aleph_client, CompletionRequest, Prompt
from datetime import datetime
from dataclasses import dataclass
from typing import Callable, Union

from sympy import false, parallel_poly_from_expr

from .huggingface.hf import HFInference
import curlify

from server.lib import storage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@dataclass
class ProviderDetails:
    '''
    Args:
        api_key (str): API key for provider
        version_key (str): version key for provider
    '''
    api_key: str
    version_key: str

@dataclass
class InferenceRequest:
    '''
    Args:
        uuid (str): unique identifier for inference request
        model_name (str): name of model to use
        model_tag (str): tag of model to use
        model_provider (str): provider of model to use
        model_parameters (dict): parameters for model
        model_tasktype (str): for tasktype value
        model_endpoint (str): endpoint for model
        model_metadata (dict): metadata for model
        prompt (str): prompt to use for inference
    '''
    uuid: str
    model_name: str
    model_tag: str
    model_provider: str
    model_parameters: dict
    model_tasktype: str
    model_endpoint: str
    model_metadata: dict
    prompt: str


@dataclass
class ProablityDistribution:
    '''
    Args:
        log_prob_sum (float): sum of log probabilities
        simple_prob_sum (float): sum of simple probabilities
        tokens (dict): dictionary of tokens and their probabilities
    '''
    log_prob_sum: float
    simple_prob_sum: float
    tokens: dict

@dataclass
class InferenceResult:
    '''
    Args:
        uuid (str): unique identifier for inference request
        model_name (str): name of model to use
        model_tag (str): tag of model to use
        model_provider (str): provider of model to use
        token (str): token returned by inference
        probability (float): probability of token
        top_n_distribution (ProablityDistribution): top n distribution of tokens
    '''
    uuid: str
    model_name: str
    model_tag: str
    model_provider: str
    token: str
    probability: Union[float, None]
    top_n_distribution: Union[ProablityDistribution, None]

InferenceFunction = Callable[[str, InferenceRequest], None]

class InferenceAnnouncer:
    def __init__(self, sse_topic):
        self.sse_topic = sse_topic
        self.cancel_cache = cachetools.TTLCache(maxsize=1000, ttl=60)

    def __format_message__(self, event: str, infer_result: InferenceResult) -> str:
        logger.debug("formatting message")
        encoded = {
            "message": infer_result.token,
            "modelName": infer_result.model_name,
            "modelTag": infer_result.model_tag,
            "modelProvider": infer_result.model_provider,
        }

        if infer_result.probability is not None:
            encoded["prob"] = round(math.exp(infer_result.probability) * 100, 2) 

        if infer_result.top_n_distribution is not None:
            encoded["topNDistribution"] = {
                "logProbSum": infer_result.top_n_distribution.log_prob_sum,
                "simpleProbSum": infer_result.top_n_distribution.simple_prob_sum,
                "tokens": infer_result.top_n_distribution.tokens
            }

        return json.dumps({"data": encoded, "type": event})
    
    def announce(self, infer_result: InferenceResult, event: str):
        if infer_result.uuid in self.cancel_cache:
            return False

        message = None
        if event == "done":
            message = json.dumps({"data": {}, "type": "done"})
        else:
            message = self.__format_message__(event=event, infer_result=infer_result)

        logger.debug(f"Announcing {event} for uuid: {infer_result.uuid}, message: {message}")
        self.sse_topic.publish(message)

        return True

    def cancel_callback(self, message):
        if message['type'] == 'pmessage':
            data = json.loads(message['data'])
            uuid = data['uuid']
            logger.info(f"Received cancel message for uuid: {uuid}")
            self.cancel_cache[uuid] = True      
   
class InferenceManager:
    def __init__(self, sse_topic):
        self.announcer = InferenceAnnouncer(sse_topic)
        

    def __error_handler__(self, inference_fn: InferenceFunction, provider_details: ProviderDetails, inference_request: InferenceRequest):
        logger.info(f"Requesting inference from {inference_request.model_name} on {inference_request.model_provider}")
        infer_result = InferenceResult(
            uuid=inference_request.uuid,
            model_name=inference_request.model_name,
            model_tag=inference_request.model_tag,
            model_provider=inference_request.model_provider,
            token=None,
            probability=None,
            top_n_distribution=None
        )

        if not self.announcer.announce(InferenceResult(
            uuid=inference_request.uuid,
            model_name=inference_request.model_name,
            model_tag=inference_request.model_tag,
            model_provider=inference_request.model_provider,
            token="[INITIALIZING]",
            probability=None,
            top_n_distribution=None
        ), event="status"):
            return

        try:
            inference_fn(provider_details, inference_request)
        except openai.error.Timeout as e:
            infer_result.token = f"[ERROR] OpenAI API request timed out: {e}"
            logger.error(f"OpenAI API request timed out: {e}")
        except openai.error.APIError as e:
            infer_result.token = f"[ERROR] OpenAI API returned an API Error: {e}"
            logger.error(f"OpenAI API returned an API Error: {e}")
        except openai.error.APIConnectionError as e:
            infer_result.token = f"[ERROR] OpenAI API request failed to connect: {e}"
            logger.error(f"OpenAI API request failed to connect: {e}")
        except openai.error.InvalidRequestError as e:
            infer_result.token = f"[ERROR] OpenAI API request was invalid: {e}"
            logger.error(f"OpenAI API request was invalid: {e}")
        except openai.error.AuthenticationError as e:
            infer_result.token = f"[ERROR] OpenAI API request was not authorized: {e}"
            logger.error(f"OpenAI API request was not authorized: {e}")
        except openai.error.PermissionError as e:
            infer_result.token = f"[ERROR] OpenAI API request was not permitted: {e}"
            logger.error(f"OpenAI API request was not permitted: {e}")
        except openai.error.RateLimitError as e:
            infer_result.token = f"[ERROR] OpenAI API request exceeded rate limit: {e}"
            logger.error(f"OpenAI API request exceeded rate limit: {e}")
        except requests.exceptions.RequestException as e:
            logging.error(f"RequestException: {e}")
            infer_result.token = f"[ERROR] No response from {infer_result.model_provider } after sixty seconds"
        # except Exception as e:
        #     logger.error(f"\nError --------------------: {e}")
        except ValueError as e:
            if infer_result.model_provider == "huggingface-local":
                infer_result.token = f"[ERROR] Error parsing response from local inference: {traceback.format_exc()}"
                logger.error(f"Error parsing response from local inference: {traceback.format_exc()}")
            else:
                infer_result.token = f"[ERROR] Error parsing response from API: {e}"
                logger.error(f"Error parsing response from API: {e}")
        except Exception as e:
            infer_result.token = f"[ERROR] {e}"
            logger.error(f"Error: {e}")
        finally:
            if infer_result.token is None:
                infer_result.token = "[COMPLETED]"
            self.announcer.announce(infer_result, event="status")
            logger.info(f"Completed inference for {inference_request.model_name} on {inference_request.model_provider}")
    
    # Custom function to call AI Cloud models
    def __aicloud_text_generation__(self, provider_details: ProviderDetails, inference_request: InferenceRequest):
        # logger.info(f"----> {inference_request}")

        request_url, request_headers, request_data = self.aicloud_request_framer(provider_details, inference_request)

        logger.info(f"Request URL: {request_url}, {request_headers}, {request_data}")

        response = requests.post(
            request_url,
            headers=request_headers,
            data=json.dumps(request_data),
            verify=false
        )

        logger.info(curlify.to_curl(response.request))

        content_type = response.headers["content-type"]

        cancelled = False

        if response.status_code != 200 :
            raise Exception(f"Request failed: {response.status_code} {response.reason}")

        if content_type == "application/json":
            return_data = json.loads(response.content.decode("utf-8"))
            # logger.info(f"Return from ai cloud - {return_data}")
            
            if 'code' in return_data and return_data['code'] == "424":
                Error_message = "Unknown Error" if return_data['error'] == "" else return_data['error']
                logger.info(f"Error from AI cloud ================================ - {Error_message}")
                raise Exception(f"Request failed: {Error_message}")
        
            outputs = self.process_output(inference_request,return_data)
            outputs = self.removeprefix(outputs,inference_request.prompt)
            logger.info(f"Reached output-----------{outputs}")
            self.announcer.announce(InferenceResult(
                uuid=inference_request.uuid,
                model_name=inference_request.model_name,
                model_tag=inference_request.model_tag,
                model_provider=inference_request.model_provider,
                token=outputs,
                probability=None,
                top_n_distribution=None
            ), event="infer")
            # logger.info("Reached the end go AI cloud request-----------")
        else:
            total_tokens = 0
            for response in response.iter_lines():
                response = response.decode('utf-8')
                if response == "":
                    continue

                response_json = json.loads(response[5:])
                if "error" in response:
                    error = response_json["error"]
                    raise Exception(f"{error}")

                token = response_json['token']

                total_tokens += 1

                if token["special"]:
                    continue

                if cancelled: continue

                if not self.announcer.announce(
                    InferenceResult(
                        uuid=inference_request.uuid,
                        model_name=inference_request.model_name,
                        model_tag=inference_request.model_tag,
                        model_provider=inference_request.model_provider,
                        token=" " if token['id'] == 3 else token['text'],
                        probability=token['logprob'],
                        top_n_distribution=None,
                    ),
                    event="infer",
                ):
                    cancelled = True
                    logger.info(f"Cancelled inference for {inference_request.uuid} - {inference_request.model_name}")

    def aicloud_text_generation(self, provider_details: ProviderDetails, inference_request: InferenceRequest):
        # logger.info("Requesting inference on -----------AI CLOUD------------")
        self.__error_handler__(self.__aicloud_text_generation__, provider_details, inference_request) 

    # Custom function to call Azure models
    def __azure_openai_text_generation__(self, provider_details: ProviderDetails, inference_request: InferenceRequest):
        
        # logger.info("Reaching azure block")
        model_metadata = inference_request.model_metadata
        # Base URL for Azure
        request_url = model_metadata['endpoint']

        headers = {
                'Content-Type': 'application/json',
        }

        for key, value in inference_request.model_parameters.items():
            headers[key] = str(value)

        requestTemplate = inference_request.model_metadata['requestTemplate']
        inputFormatMap = inference_request.model_metadata['inputFormatMap']

        data = requestTemplate
        data = json.dumps(requestTemplate)
        data = data.replace("<role>", "user").replace("<content>", inference_request.prompt)
        data = json.loads(data)
        # logger.info(f"Data to be sent to Azure - {data}, {type(data)}")

        # Send the request and get the response
        response = requests.put(request_url, headers=headers, data=data)
        logger.info(curlify.to_curl(response.request))

        content_type = response.headers["content-type"]

        cancelled = False

        outputFormatMap = inference_request.model_metadata['outputFormatMap'][0]

        if content_type == "application/json":
            return_data = json.loads(response.content.decode("utf-8"))
            logger.info(f"Return from azure - {return_data}")
                  
            generated_token = self.extract_value_by_path(return_data, outputFormatMap["key"])

            self.announcer.announce(InferenceResult(
                uuid=inference_request.uuid,
                model_name=inference_request.model_name,
                model_tag=inference_request.model_tag,
                model_provider=inference_request.model_provider,
                token=generated_token,
                probability=None,
                top_n_distribution=None
            ), event="infer")
    
            # logger.info("Reached the end Azure request-----------")

        else:
            total_tokens = 0
            for response in response.iter_lines():
                response = response.decode('utf-8')
                if response == "":
                    continue

                response_json = json.loads(response[5:])
                if "error" in response:
                    error = response_json["error"]
                    raise Exception(f"{error}")

                token = response_json['token']

                total_tokens += 1

                if token["special"]:
                    continue

                if cancelled: continue

                if not self.announcer.announce(
                    InferenceResult(
                        uuid=inference_request.uuid,
                        model_name=inference_request.model_name,
                        model_tag=inference_request.model_tag,
                        model_provider=inference_request.model_provider,
                        token=" " if token['id'] == 3 else token['text'],
                        probability=token['logprob'],
                        top_n_distribution=None,
                    ),
                    event="infer",
                ):
                    cancelled = True
                    logger.info(f"Cancelled inference for {inference_request.uuid} - {inference_request.model_name}")

    def azure_openai_text_generation(self, provider_details: ProviderDetails, inference_request: InferenceRequest):
        logger.info("Requesting inference on -----------AZURE------------")
        self.__error_handler__(self.__azure_openai_text_generation__, provider_details, inference_request) 
    

    def removeprefix(self,text, prefix):
        """
        Remove the specified prefix from the given text if it is included anywhere in the text.
    
        Parameters:
        text (str): The original string.
        prefix (str): The prefix to remove.
    
        Returns:
        str: The string with the prefix removed, if it was present.
        """
        if prefix in text:
            logger.info(f"Prefix found in text")
            return text.replace(prefix, "", 1)
        return text 
    
    def __openai_text_generation__(self, provider_details: ProviderDetails, inference_request: InferenceRequest):
        openai.api_key = provider_details.api_key

        response = openai.Completion.create(
            model=inference_request.model_name,
            prompt=inference_request.prompt,
            temperature=inference_request.model_parameters['temperature'],
            max_tokens=inference_request.model_parameters['max_new_tokens'],
            top_p=inference_request.model_parameters['topP'],
            stop=None if len(inference_request.model_parameters['stopSequences']) == 0 else inference_request.model_parameters['stopSequences'],
            frequency_penalty=inference_request.model_parameters['frequencyPenalty'],
            presence_penalty=inference_request.model_parameters['presencePenalty'],
            logprobs=5,
            stream=True
        )
        cancelled = False

        for event in response:
            generated_token = event['choices'][0]['text']
            infer_response = None
            try:
                chosen_log_prob = 0
                likelihood = event['choices'][0]["logprobs"]['top_logprobs'][0]

                prob_dist = ProablityDistribution(
                    log_prob_sum=0, simple_prob_sum=0, tokens={},
                )

                for token, log_prob in likelihood.items():
                    simple_prob = round(math.exp(log_prob) * 100, 2)
                    prob_dist.tokens[token] = [log_prob, simple_prob]

                    if token == generated_token:
                        chosen_log_prob = round(log_prob, 2)
  
                    prob_dist.simple_prob_sum += simple_prob
                
                prob_dist.tokens = dict(
                    sorted(prob_dist.tokens.items(), key=lambda item: item[1][0], reverse=True)
                )
                prob_dist.log_prob_sum = chosen_log_prob
                prob_dist.simple_prob_sum = round(prob_dist.simple_prob_sum, 2)
             
                infer_response = InferenceResult(
                    uuid=inference_request.uuid,
                    model_name=inference_request.model_name,
                    model_tag=inference_request.model_tag,
                    model_provider=inference_request.model_provider,
                    token=generated_token,
                    probability=event['choices'][0]['logprobs']['token_logprobs'][0],
                    top_n_distribution=prob_dist
                )
            except IndexError:
                infer_response = InferenceResult(
                    uuid=inference_request.uuid,
                    model_name=inference_request.model_name,
                    model_tag=inference_request.model_tag,
                    model_provider=inference_request.model_provider,
                    token=generated_token,
                    probability=-1,
                    top_n_distribution=None
                )

            if cancelled: continue

            if not self.announcer.announce(infer_response, event="infer"):
                cancelled = True
                logger.info(f"Cancelled inference for {inference_request.uuid} - {inference_request.model_name}")
         
    def __openai_chat_generation__(self, provider_details: ProviderDetails, inference_request: InferenceRequest):
        openai.api_key = provider_details.api_key

        current_date = datetime.now().strftime("%Y-%m-%d")

        if inference_request.model_name == "gpt-4":
            system_content = "You are GPT-4, a large language model trained by OpenAI. Answer as concisely as possible"
        else:
            system_content = f"You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible. Knowledge cutoff: 2021-09-01 Current date: {current_date}"

        response = openai.ChatCompletion.create(
             model=inference_request.model_name,
             messages = [
                {"role": "system", "content": system_content},
                {"role": "user", "content": inference_request.prompt},
            ],
            temperature=inference_request.model_parameters['temperature'],
            max_tokens=inference_request.model_parameters['max_new_tokens'],
            top_p=inference_request.model_parameters['topP'],
            frequency_penalty=inference_request.model_parameters['frequencyPenalty'],
            presence_penalty=inference_request.model_parameters['presencePenalty'],
            stream=True,
            timeout=60
        )

        tokens = ""
        cancelled = False

        for event in response:
            response = event['choices'][0]
            if response['finish_reason'] == "stop":
                break

            delta = response['delta']

            if "content" not in delta:
                continue

            generated_token = delta["content"]
            tokens += generated_token

            infer_response = InferenceResult(
                uuid=inference_request.uuid,
                model_name=inference_request.model_name,
                model_tag=inference_request.model_tag,
                model_provider=inference_request.model_provider,
                token=generated_token,
                probability=None,
                top_n_distribution=None
             )

            if cancelled: continue

            if not self.announcer.announce(infer_response, event="infer"):
                cancelled = True
                logger.info(f"Cancelled inference for {inference_request.uuid} - {inference_request.model_name}")

    def openai_text_generation(self, provider_details: ProviderDetails, inference_request: InferenceRequest):
        # TODO: Add a meta field to the inference so we know when a model is chat vs text
        if inference_request.model_name in ["gpt-3.5-turbo", "gpt-4"]:
            self.__error_handler__(self.__openai_chat_generation__, provider_details, inference_request)
        else:
            self.__error_handler__(self.__openai_text_generation__, provider_details, inference_request)

    def __cohere_text_generation__(self, provider_details: ProviderDetails, inference_request: InferenceRequest):
        with requests.post("https://api.cohere.ai/generate",
            headers={
                "Authorization": f"Bearer {provider_details.api_key}",
                "Content-Type": "application/json",
                "Cohere-Version": "2021-11-08",
            },
            data=json.dumps({
                "prompt": inference_request.prompt,
                "model": inference_request.model_name,
                "temperature": float(inference_request.model_parameters['temperature']),
                "p": float(inference_request.model_parameters['topP']),
                "k": int(inference_request.model_parameters['topK']),
                "stopSequences": inference_request.model_parameters['stopSequences'],
                "frequencyPenalty": float(inference_request.model_parameters['frequencyPenalty']),
                "presencePenalty": float(inference_request.model_parameters['presencePenalty']),
                "return_likelihoods": "GENERATION",
                "max_tokens": int(inference_request.model_parameters['max_new_tokens']),
                "stream": True,
            }),
            stream=True
        ) as response:
            if response.status_code != 200 or response.reason != "OK":
                raise Exception(f"Request failed: {response.status_code} {response.reason}")

            cancelled = False

            for token in response.iter_lines():
                token = token.decode('utf-8')
                token_json = json.loads(token)
                if cancelled: continue

                if not self.announcer.announce(InferenceResult(
                    uuid=inference_request.uuid,
                    model_name=inference_request.model_name,
                    model_tag=inference_request.model_tag,
                    model_provider=inference_request.model_provider,
                    token=token_json['text'],
                    probability=None, #token_json['likelihood']
                    top_n_distribution=None
                ), event="infer"):
                    cancelled = True
                    logger.info(f"Cancelled inference for {inference_request.uuid} - {inference_request.model_name}")

    def cohere_text_generation(self, provider_details: ProviderDetails, inference_request: InferenceRequest):
        self.__error_handler__(self.__cohere_text_generation__, provider_details, inference_request)
    
    def __huggingface_text_generation__(self, provider_details: ProviderDetails, inference_request: InferenceRequest):
        response = requests.request("POST",
            f"https://api-inference.huggingface.co/models/{inference_request.model_name}",
            headers={"Authorization": f"Bearer {provider_details.api_key}"},
            json={
                "inputs": inference_request.prompt,
                "stream": True,
                "parameters": {
                    "max_length": min(inference_request.model_parameters['max_new_tokens'], 250), # max out at 250 tokens per request, we should handle for this in client side but just in case
                    "temperature": inference_request.model_parameters['temperature'],
                    "top_k": inference_request.model_parameters['topK'],
                    "top_p": inference_request.model_parameters['topP'],
                    "repetition_penalty": inference_request.model_parameters['repetitionPenalty'],
                    "stop_sequences": inference_request.model_parameters['stopSequences'],
                },
                "options": {
                    "use_cache": False
                }
            },
            timeout=60
        )

        content_type = response.headers["content-type"]

        cancelled = False

        if response.status_code != 200:
            raise Exception(f"Request failed: {response.status_code} {response.reason}")

        if content_type == "application/json":
            return_data = json.loads(response.content.decode("utf-8"))
            outputs = return_data[0]["generated_text"]
            outputs = outputs.removeprefix(inference_request.prompt)

            self.announcer.announce(InferenceResult(
                uuid=inference_request.uuid,
                model_name=inference_request.model_name,
                model_tag=inference_request.model_tag,
                model_provider=inference_request.model_provider,
                token=outputs,
                probability=None,
                top_n_distribution=None
            ), event="infer")
        else:
            total_tokens = 0
            for response in response.iter_lines():
                response = response.decode('utf-8')
                if response == "":
                    continue

                response_json = json.loads(response[5:])
                if "error" in response:
                    error = response_json["error"]
                    raise Exception(f"{error}")

                token = response_json['token']

                total_tokens += 1

                if token["special"]:
                    continue

                if cancelled: continue

                if not self.announcer.announce(
                    InferenceResult(
                        uuid=inference_request.uuid,
                        model_name=inference_request.model_name,
                        model_tag=inference_request.model_tag,
                        model_provider=inference_request.model_provider,
                        token=" " if token['id'] == 3 else token['text'],
                        probability=token['logprob'],
                        top_n_distribution=None,
                    ),
                    event="infer",
                ):
                    cancelled = True
                    logger.info(f"Cancelled inference for {inference_request.uuid} - {inference_request.model_name}")
           
    def huggingface_text_generation(self, provider_details: ProviderDetails, inference_request: InferenceRequest):
        self.__error_handler__(self.__huggingface_text_generation__, provider_details, inference_request)

    def __forefront_text_generation__(self, provider_details: ProviderDetails, inference_request: InferenceRequest):
        with requests.post(
                f"https://shared-api.forefront.link/organization/gPn2ZLSO3mTh/{inference_request.model_name}/completions/{provider_details.version_key}",
                headers={
                    "Authorization": f"Bearer {provider_details.api_key}",
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "text": inference_request.prompt,
                    "top_p": float(inference_request.model_parameters['topP']),
                    "top_k": int(inference_request.model_parameters['topK']),
                    "temperature":  float(inference_request.model_parameters['temperature']),
                    "repetition_penalty":  float(inference_request.model_parameters['repetitionPenalty']),
                    "length": int(inference_request.model_parameters['max_new_tokens']),
                    "stop": inference_request.model_parameters['stopSequences'],
                    "logprobs": 5,
                    "stream": True,
                }),
                stream=True
            ) as response:
            if response.status_code != 200:
                raise Exception(f"Request failed: {response.status_code} {response.reason}")
            cancelled = False
            total_tokens = 0
            aggregate_string_length = 0

            for packet in sseclient.SSEClient(response).events():
                generated_token = None
                probability = None
                prob_dist = None

                if packet.event == "update":
                    packet.data = urllib.parse.unquote(packet.data)
                    generated_token = packet.data[aggregate_string_length:]
                    aggregate_string_length = len(packet.data)

                    if not self.announcer.announce(InferenceResult(
                        uuid=inference_request.uuid,
                        model_name=inference_request.model_name,
                        model_tag=inference_request.model_tag,
                        model_provider=inference_request.model_provider,
                        token=generated_token,
                        probability=probability,
                        top_n_distribution=prob_dist
                    ), event="infer"):
                        cancelled = True
                        logger.info(f"Cancelled inference for {inference_request.uuid} - {inference_request.model_name}")
                elif packet.event == "message":
                    data = json.loads(packet.data)

                    logprobs = data["logprobs"][0]
                    tokens = logprobs["tokens"]
                    token_logprobs = logprobs["token_logprobs"]

                    new_tokens = tokens[total_tokens:]

                    for index, new_token in enumerate(new_tokens):
                        generated_token = new_token

                        probability = token_logprobs[total_tokens + index]
                        top_logprobs = logprobs["top_logprobs"][total_tokens + index]

                        chosen_log_prob = 0
                        prob_dist = ProablityDistribution(
                            log_prob_sum=0, simple_prob_sum=0, tokens={},
                        )

                        for token, log_prob in top_logprobs.items():
                            if log_prob == -3000.0: continue
                            simple_prob = round(math.exp(log_prob) * 100, 2)
                            prob_dist.tokens[token] = [log_prob, simple_prob]

                            if token == generated_token:
                                chosen_log_prob = round(log_prob, 2)

                            prob_dist.simple_prob_sum += simple_prob

                        prob_dist.tokens = dict(
                            sorted(prob_dist.tokens.items(), key=lambda item: item[1][0], reverse=True)
                        )
                        prob_dist.log_prob_sum = chosen_log_prob
                        prob_dist.simple_prob_sum = round(prob_dist.simple_prob_sum, 2)

                        if not self.announcer.announce(InferenceResult(
                            uuid=inference_request.uuid,
                            model_name=inference_request.model_name,
                            model_tag=inference_request.model_tag,
                            model_provider=inference_request.model_provider,
                            token=generated_token,
                            probability=probability,
                            top_n_distribution=prob_dist
                        ), event="infer"):
                            cancelled = True
                            logger.info(f"Cancelled inference for {inference_request.uuid} - {inference_request.model_name}")

                    total_tokens = len(tokens)
                elif packet.event == "end":
                    break
                else:
                    continue

                if cancelled: continue

    def forefront_text_generation(self, provider_details: ProviderDetails, inference_request: InferenceRequest):
        self.__error_handler__(self.__forefront_text_generation__, provider_details, inference_request)

    def __local_text_generation__(self, provider_details: ProviderDetails, inference_request: InferenceRequest):
        cancelled = False
        logger.info(f"Starting inference for {inference_request.uuid} - {inference_request.model_name}")

        hf = HFInference(inference_request.model_name)
        output = hf.generate(
            prompt=inference_request.prompt,
            max_length=int(inference_request.model_parameters['max_new_tokens']),
            top_p=float(inference_request.model_parameters['topP']),
            top_k=int(inference_request.model_parameters['topK']),
            temperature=float(inference_request.model_parameters['temperature']),
            repetition_penalty=float(inference_request.model_parameters['repetitionPenalty']),
            stop_sequences=None,
        )

        infer_response = None
        for generated_token in output:
            if cancelled: break
            infer_response = InferenceResult(
                uuid=inference_request.uuid,
                model_name=inference_request.model_name,
                model_tag=inference_request.model_tag,
                model_provider=inference_request.model_provider,
                token=generated_token,
                probability=None,
                top_n_distribution=None
            )
        
            if not self.announcer.announce(infer_response, event="infer"):
                cancelled = True
                logger.info(f"Cancelled inference for {inference_request.uuid} - {inference_request.model_name}")

    def local_text_generation(self, provider_details: ProviderDetails, inference_request: InferenceRequest):
       self.__error_handler__(self.__local_text_generation__, provider_details, inference_request)
    
    def __anthropic_text_generation__(self, provider_details: ProviderDetails, inference_request: InferenceRequest):
        c = anthropic.Client(provider_details.api_key)

        response = c.completion_stream(
            prompt=f"{anthropic.HUMAN_PROMPT} {inference_request.prompt}{anthropic.AI_PROMPT}",
            stop_sequences=[anthropic.HUMAN_PROMPT] + inference_request.model_parameters['stopSequences'],
            temperature=float(inference_request.model_parameters['temperature']),
            top_p=float(inference_request.model_parameters['topP']),
            max_tokens_to_sample=inference_request.model_parameters['max_new_tokens'],
            model=inference_request.model_name,
            stream=True,
        )

        completion = ""
        cancelled = False

        for data in response:
            new_completion = data["completion"]
            generated_token = new_completion[len(completion):]
            if cancelled: continue

            if not self.announcer.announce(InferenceResult(
                uuid=inference_request.uuid,
                model_name=inference_request.model_name,
                model_tag=inference_request.model_tag,
                model_provider=inference_request.model_provider,
                token=generated_token,
                probability=None,
                top_n_distribution=None
             ), event="infer"):
                cancelled = True
                logger.info(f"Cancelled inference for {inference_request.uuid} - {inference_request.model_name}")

            completion = new_completion

    def anthropic_text_generation(self, provider_details: ProviderDetails, inference_request: InferenceRequest):
        self.__error_handler__(self.__anthropic_text_generation__, provider_details, inference_request)
    
    def __aleph_alpha_text_generation__(self, provider_details: ProviderDetails, inference_request: InferenceRequest):
        client = aleph_client(provider_details.api_key)
        
        request = CompletionRequest(
            prompt = Prompt.from_text(inference_request.prompt),
            temperature= inference_request.model_parameters['temperature'],
            maximum_tokens=inference_request.model_parameters['max_new_tokens'],
            top_p=float(inference_request.model_parameters['topP']),
            top_k=int(inference_request.model_parameters['topK']),
            presence_penalty=float(inference_request.model_parameters['repetitionPenalty']),
            stop_sequences=inference_request.model_parameters['stopSequences']
        )
        
        response = client.complete(request, model=inference_request.model_name)
        
        self.announcer.announce(InferenceResult(
            uuid=inference_request.uuid,
            model_name=inference_request.model_name,
            model_tag=inference_request.model_tag,
            model_provider=inference_request.model_provider,
            token=response.completions[0].completion,
            probability=None,
            top_n_distribution=None
        ), event="infer")

    def aleph_alpha_text_generation(self, provider_details: ProviderDetails, inference_request: InferenceRequest):
        self.__error_handler__(self.__aleph_alpha_text_generation__, provider_details, inference_request)
    
    def get_announcer(self):
        return self.announcer  
    
    # util functions to process requests and responses.
    def aicloud_request_framer(self, provider_details: ProviderDetails, inference_request: InferenceRequest):
        """
        This function takes in the provider details and the inference request and returns a dictionary that can be used to make a request to the provider
        
        param: provider_details: ProviderDetails
        param: inference_request: InferenceRequest contains model details, input and output formats.

        returns: dict
        """
        # the flow will be very different if the model is llama-3.1, this here is for other aicloud models.
        model_tasktype = inference_request.model_tasktype
        model_metadata = inference_request.model_metadata
        logger.info(f"Inference {inference_request.model_metadata}")

        request_url = model_metadata['endpoint']
        request_headers = {}
        request_data = {}

        if("Llama-3.1" in model_metadata['displayName']):
            logger.info("Llama-3.1 model detected")
            logger.info(inference_request)
            request_template = json.loads(model_metadata['requestTemplate'])
            logger.info(f"Request template: {type(request_template)}{str(request_template)}")

            request_data['messages'] = request_template['messages']
            request_data['messages'][0]['role'] = "user"
            request_data['messages'][0]['content'] = inference_request.prompt

            request_headers = request_template['headers']

            for key,value in inference_request.model_parameters.items():
                request_data[key] = value

            logger.info(f"Request data: {request_data}, {request_headers}")

            # return request_url,request_headers, request_data
            # raise Exception(f"Model {inference_request.model_name} not supported by playground")
        # if model_tasktype == "text generation":
        #     task_type = "language/generate"
        # elif model_tasktype == "code generation":
        #     task_type = "code/complete"
        # else: 
        #     raise Exception(f"Task type {task_type} not supported by playground")


        
        else:
            # for url, now hardcoded to ai cloud url.
            # request_url = inference_request.model_endpoint
            # AI_CLOUD_BASE_URL.format(task_type, model_name, model_version)
            # request_url = model_metadata['endpoint']

            inputformatMap = model_metadata['inputFormatMap'][0]


            # request header
            request_headers = {
                "Content-Type": "application/json"
            }

            # Check if encoding is required
            if inputformatMap['encode']:
                # Encode the prompt to base64
                input_prompt = base64.b64encode(inference_request.prompt.encode('utf-8')).decode('utf-8')
            else:
                # Use the original prompt
                input_prompt = inference_request.prompt

            inputFormatMap = inference_request.model_metadata['inputFormatMap']

            for input in inputFormatMap:
                # logger.info(input)
                if input['key'] == "inputs":
                    input_placeholder = input["value"]

            # for input format
            request_data = inference_request.model_metadata['requestTemplate']

            # logger.info(f"Str or dict {request_data}, {type(request_data)}")
            
            request_data = request_data.replace(input_placeholder, input_prompt)

            # logger.info(f"Request data {request_data}")

            request_data = json.loads(request_data)
            # Replace placeholders with actual values from model_parameters
            for key,value in inference_request.model_parameters.items():
                request_data["parameters"][key] = value
                # logger.info(f"Request data YYY{request_data}")

            
            # logger.info(f"Request data {request_data}")

        return request_url, request_headers, request_data
        
    def process_output(self,inference_request, return_data):
        """
        This function takes in the response from the provider and processes it to return the output
        :param return_data: dict
        :return: str
        """
        outputFormatMap = inference_request.model_metadata['outputFormatMap']
        outputFormat = inference_request.model_metadata['outputFormat']
        logger.info(f"processing return data: {return_data}, {outputFormat} ,{outputFormatMap}")

        output_encode = false
        
        if not outputFormatMap:
            generated_text = return_data[0]
        else:
            # specifically for LLama-3.1 models.
            if(outputFormatMap[0]['key'] != "generated_text"):
                return self.extract_value_by_path(return_data, outputFormatMap[0]['key'])
            output_key:str  = outputFormatMap[0]['key']
            output_encode = outputFormatMap[0]['encode'] 
            logger.info(f"processing return data: {return_data}, {outputFormat} ,{output_key}")

            if outputFormat.lower() == "array":
                # Assuming return_data is a list of dictionaries and we want to access the first item's value by a dynamic key
                logger.info(f"output_item: {return_data}")
                output_item = return_data[0]  # Access the first dictionary in the list
                generated_text = output_item[output_key] # Safely get the value by key from the dictionary
                # logger.info(f"generated_text: {generated_text}")
            else:
                # Directly access the value from return_data assuming it's a dictionary
                output_item = return_data  # Access the first dictionary in the list
                # logger.info(f"output_item: in else {output_item}")
                generated_text = return_data[str(output_key)]  # Safely get the value by key from the dictionary
            

        if output_encode:
            logger.info("decoding base64")
            generated_text = base64.b64decode(generated_text)
            output = generated_text.decode("utf-8")
        else: 
            output = generated_text

        logger.info(f"processed output: {output}")  
        return output
    
    
    def extract_value_by_path(self,data, path):
        """
        Extracts a value from a nested dictionary or list based on a given path.
        :param data: The nested dictionary or list to search.
        :param path: The path to the value, using dot notation for dictionaries and brackets for list indices.
        :return: The value found at the path, or None if the path is invalid.
        """
        # Split the path by '.' to handle nested dictionaries and by '][' to handle nested lists
        keys = []
        for part in path.replace("][", ".").split('.'):
            if '[' in part and ']' in part:
                # Extract the part before the '[' and the index inside '[]'
                key, index = part.split('[')
                index = index.replace(']', '')  # Remove the closing bracket
                keys.append(key)  # Add the dictionary key
                keys.append(index)  # Add the list index as a separate key
            else:
                keys.append(part)
        
        print(f"keys: {keys}")
        try:
            for key in keys:
                if key.isdigit():  # If the key is a digit, access the list
                    data = data[int(key)]
                else:  # Otherwise, access the dictionary
                    data = data[key]
            return data
        except (KeyError, IndexError, TypeError):
            return None  # Return None or raise an error if the path is invalid
