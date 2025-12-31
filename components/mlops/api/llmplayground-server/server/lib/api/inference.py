#  ================================================================================================================# 
# # ===============================================================================================================# 
# # Copyright 2024 Infosys Ltd.                                                                                    # 
# # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # 
# # http://www.apache.org/licenses/                                                                                # 
#  ================================================================================================================# 

import logging
import json
from math import log
import time
import threading

from sympy import true

from .response_utils import create_response_message
from ..inference import InferenceRequest, InferenceResult, InferenceRequest
from ..sse import Message

from concurrent.futures import ThreadPoolExecutor
from flask import g, request, Response, stream_with_context, Blueprint, current_app
from typing import List, Tuple

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

inference_bp = Blueprint('inference', __name__, url_prefix='/inference')

@inference_bp.before_app_request
def set_app_context():
    g.app = current_app

@inference_bp.route("/text/stream", methods=["POST"])
def stream_inference():
    data = request.get_json(force=True)
    logger.info(f"  Path: {request.path}, Request: {data}")

    storage = g.get('storage')
    global_state = g.get('global_state')

    if not is_valid_request_data(data):
        return create_response_message("Invalid request", 400)
    # logger.info(f"Valid request data: {data}")

    request_uuid = "1"
    prompt = data['prompt']
    models = data['models']
    
    all_tasks = [task for task in (create_inference_request(model, storage, prompt, request_uuid) for model in models) if task is not None]

    if not all_tasks:
        return create_response_message("Invalid Request", 400)

    thread = threading.Thread(target=bulk_completions, args=(global_state, all_tasks,))
    thread.start()

    return stream_response(global_state, request_uuid)

def is_valid_request_data(data):
    return isinstance(data['prompt'], str) and isinstance(data['models'], list)

def create_inference_request(model, storage, prompt, request_uuid):
    # logger.info(f"Create_Inference Model: {model}")
    model_name, provider_name, model_tag, parameters, tasktype, endpoint, metadata = extract_model_data(model)
    # model_name = model_name.removeprefix(f"{provider_name}:")
    prefix = f"{provider_name}:"
    if model_name.startswith(prefix):
        model_name = model_name[len(prefix):]
    provider = next((provider for provider in storage.get_providers() if provider.name == provider_name), None)
    if provider is None or not provider.has_model(model_name):
        logger.error(f"Provider not found: {provider_name}, model: {model_name}")
        return None
    logger.info(f"Provider found: {provider_name}, model: {model_name}")
    if validate_parameters(provider.get_model(model_name), parameters):
        logger.info(f"Details valid for model: {model_name}, provider: {provider_name}, tag: {model_tag}, parameters: {parameters}, tasktype: {tasktype}, metadata: {metadata}")
        return InferenceRequest(uuid=request_uuid, model_name=model_name, model_tag=model_tag,
            model_provider=provider_name, model_parameters=parameters, model_tasktype=tasktype,model_endpoint=endpoint, model_metadata=metadata, prompt=prompt
        )

    return None

def extract_model_data(model):
    return model['name'],  model['provider'], model['tag'], model['parameters'], model['tasktype'], model['endpoint'],model['metadata']

def validate_parameters(model, parameters):
    # logger.info(f"Model: {model}, Parameters: {parameters}")
    default_parameters = model.parameters
    for parameter in parameters:
        if parameter not in default_parameters:
            logger.info(f"Parameter {parameter} not in default parameters")
            return False

        value = parameters[parameter]
        parameter_range = default_parameters[parameter]["range"]

        if len(parameter_range) == 2:
            return true
            if value < parameter_range[0] or value > parameter_range[1]:
                return False
    return True

def stream_response(global_state, uuid):
    @stream_with_context
    def generator():
        SSE_MANAGER = global_state.get_sse_manager()
        messages = SSE_MANAGER.listen("inferences")
        try:
            while True:
                # logger.info(f"______________In stream_response {messages.get()}")
                message = json.loads(message := messages.get())
                # logger.info(f"_In stream_response message {message}")
                
                if message["type"] == "done":
                    logger.info("Done streaming SSE")
                    break
                logger.info(f"Yielding message: {json.dumps(message)}")
                yield str(Message(**message))
        except GeneratorExit:
            logger.info("GeneratorExit")
            SSE_MANAGER.publish("inferences", message=json.dumps({"uuid": uuid}))

    return Response(stream_with_context(generator()), mimetype='text/event-stream')

def bulk_completions(global_state, tasks: List[InferenceRequest]):
    time.sleep(1)
    local_tasks, remote_tasks = split_tasks_by_provider(tasks)

    if remote_tasks:
        with ThreadPoolExecutor(max_workers=len(remote_tasks)) as executor:
            futures = [executor.submit(global_state.text_generation, task) for task in remote_tasks]
            [future.result() for future in futures]

    for task in local_tasks:
        global_state.text_generation(task)

    global_state.get_announcer().announce(InferenceResult(
        uuid=tasks[0].uuid,
        model_name=None,
        model_tag=None,
        model_provider=None,
        token=None,
        probability=None,
        top_n_distribution=None
    ), event="done")

def split_tasks_by_provider(tasks: List[InferenceRequest]) -> Tuple[List[InferenceRequest], List[InferenceRequest]]:
    local_tasks, remote_tasks = [], []

    for task in tasks:
        (local_tasks if task.model_provider == "huggingface-local" else remote_tasks).append(task)

    return local_tasks, remote_tasks