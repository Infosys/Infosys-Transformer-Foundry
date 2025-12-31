# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import os
import uuid
import jinja2
import argparse
import json
import urllib.request
import sys
import math

TEMPLATE_PATH = "/var/lib/jenkins/workspace/utils/templates/dev/pipln_v1/"
TEMPLATE_NAME = "J2_PRETRAINED_PIPELINE_TEMPLATE.j2"

def validate(data, key, raise_err):
        if (data == None or data == ''):
            errormsg = key+" should not be empty"
            if (raise_err):
                raise Exception(errormsg)
                return False          
            return True
            
class CodeGenerationKubeflow:
    def __init__(self) -> None:
        self.__env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_PATH), trim_blocks=True, lstrip_blocks=True)
        self.__kubeflow_template = self.__env.get_template(TEMPLATE_NAME)

    def save_file(self, kubeflow_code,file_name):
        file_path=file_name
        with open(file_path, 'w') as f :
            f.write(kubeflow_code)   

    def replace_component_file(self,filename,comp_type):
        if comp_type == "train":
            container_image=self.container_image
            compoent_name=self.train_component_name
            with open(filename, 'r') as f :
                content=f.read()
                content=content.replace("COMPONENT_NAME",compoent_name)
                content=content.replace("COMPONENT_BASE_IMAGE",container_image)
                content=content.replace("S3_INPUT_ARTIFACTS",self.inputArtifacts_uri)
                content=content.replace("S3_OUTPUT_ARTIFACTS",self.outputArtifacts)
                content=content.replace("PROJECT_ID",self.project_id)
                content=content.replace("PIPELINENAME",self.pipeline_name)
                content=content.replace("VERSION",str(self.pipeline_version))
                content=content.replace("RUNNAME",self.pipeline_run_name)
                content=content.replace("UNZIPCOMMAND","")
                content=content.replace("COMPKEYVALUE","train")
                content=content.replace("BUCKET_NAME",self.bucketName)
                content=content.replace("DEPLOYENVIRONMENT",self.deployEnv)
                content=content.replace("DEPEDANCY_FILE_PATH",self.dependancyFilePath)
            
            self.save_file(content,"component_train.yaml")
        elif comp_type == "exit_task":
            with open(filename, 'r') as f :
                content=f.read()  
                content=content.replace("DEPLOYENVIRONMENT",self.deployEnv)
            self.save_file(content,"component_exit_task.yaml")
        else:
            print("invalid component")

    def get_input(self, get_input_details_url):
        
        try:
            
            self.format_brackets = ""
            urlinput = urllib.request.urlopen(get_input_details_url)
            input = json.loads(urlinput.read())

            self.pipeline_data=input['data']['inputData']
            compdetails = ""
            src_dir = ""
            validate(self.pipeline_data['projectId'], "projectId", True)
            validate(self.pipeline_data['pipelineId'], "pipelineId", True)
            validate(self.pipeline_data['runId'], "runId", True)
            validate(self.pipeline_data['pipelineName'], "pipelineName", True)
            validate(self.pipeline_data['pipelineVersion'], "pipelineVersion", True)
            validate(self.pipeline_data['experimentName'], "experimentName", True)

            self.container_image = self.pipeline_data['containerImage']
            self.project_id = self.pipeline_data['projectId']
            self.pipeline_id = self.pipeline_data['pipelineId']
            self.prunid = self.pipeline_data['runId']
            new_pipeline_name = self.pipeline_data['pipelineName']
            new_pipeline_name=new_pipeline_name.replace('-', '')
            self.pipeline_name = new_pipeline_name
            self.tenant_name=self.pipeline_data['tenantName']
            self.pipeline_version = self.pipeline_data['pipelineVersion']
            self.preTrainedMdlVal=""
            self.func_args =""
            self.run_arg_name = ""
            self.pipeline_args_json =""
            self.train_args = ""
            self.main_script_file = ""
            self.metric_name = "NA"
            self.metric_log_path = ""
            self.metric_regex ="NA"
            self.replace_word = ""
            self.namespace = ""
            self.pipeline_run_name = ""
            self.cookie = ""
            self.pipelineUrl = ""
            self.experimentName = ""
            self.bucketName = ""
            self.main_script_file = ""
            self.train_log_dir = ""
            self.volume_size_gb = ""
            self.mlflow_expname = self.pipeline_data['experimentName']
            self.mlflow_url = ""
            self.mlflow_log_artifact = ""
            i = 0
            for run_arg in self.pipeline_data['runArguments']:
                i = i + 1
                validate(run_arg['name'], str(i)+" runArguments name", True)
                validate(run_arg['argValue'], str(i)+" runArguments value", True)
                self.format_brackets = self.format_brackets + "{} {} "
                self.run_arg_name = self.run_arg_name + run_arg['name'] +","
                self.train_args = self.train_args + '\'--' + run_arg['name'] + "', " + run_arg['name'] + ","
                self.pipeline_args_json = self.pipeline_args_json + "\"" + run_arg['name'] + "\": \"" + run_arg['argValue'] + "\","
            self.run_arg_name = self.run_arg_name.rstrip(self.run_arg_name[-1])
            self.train_args = self.train_args.rstrip(self.train_args[-1])
            self.pipeline_args_json = self.pipeline_args_json.rstrip(self.pipeline_args_json[-1])
            self.train_args = "\"" + " {}"*(i*2) + "\".format(" + self.train_args + ")" 
            self.pipeline_args_json = "{" + self.pipeline_args_json + "}"
            self.inputArtifacts = None
            self.outputArtifacts = None
            self.bucketName="mmsrepo"
            self.preTrainedMdlArifacts=self.pipeline_data['preTrainedMdl']['artifacts']
            print(self.pipeline_data['inputArtifacts'])
            print('inputArtifacts' in self.pipeline_data)
            if 'inputArtifacts' in self.pipeline_data:
                self.inputArtifacts = self.pipeline_data['inputArtifacts']
                self.inputArtifacts_uri = self.pipeline_data['inputArtifacts']['uri']
                if(self.pipeline_data['inputArtifacts']['uri'].index("s3:") != -1):
                    inputArtifacts_part1 = self.inputArtifacts_uri.replace("s3://","")
                    self.bucketName=inputArtifacts_part1[0:inputArtifacts_part1.index("/")]

            print("self.inputArtifacts")
            print(self.inputArtifacts)        
            if 'outputArtifacts' in self.pipeline_data:
                self.outputArtifacts = self.pipeline_data['outputArtifacts']
                    
            self.deployEnv = 'PRODUCTION'
            self.replace_word = ""
            if (self.deployEnv == 'PRODUCTION'):
                self.namespace = 'training'
                self.pipelineUrl= os.getenv('PIPELINE_URL')
                self.experimentName='mms_experiment'
                                
            elif (self.deployEnv == 'DEV'):
                self.namespace='aicloud-dev'
                self.pipelineUrl= os.getenv('PIPELINE_URL')
                self.experimentName='testing'

            if(self.mlflow_expname != None or self.mlflow_expname != "NA"):
                self.mlflow_url = os.getenv('MLFLOW_URL')
                self.mlflow_log_artifact = True

            self.checkGPUAvailbility="False"
            self.gpu_set_limit = ""
            self.cpu_set_limit = ""
            self.memory_limit = ""
            self.volume_size_gb = "10Gi"
            if(validate(self.pipeline_data['resourceConfig']['volumeSizeinGB'], "", False) and self.pipeline_data['resourceConfig']['volumeSizeinGB'] != 0):
                self.volume_size_gb = self.pipeline_data['resourceConfig']['volumeSizeinGB'] + "Gi"
                            

            for comp in self.pipeline_data['resourceConfig']['computes']:
                if(comp['type'] == 'GPU'):
                    self.checkGPUAvailbility="True"
                    self.gpuQty=comp['maxQty']
                    self.gpuMemory=comp['memory']
                    if (comp['maxQty']):
                        self.gpu_set_limit = "train.set_gpu_limit("+ str(comp['maxQty']) +")"                    
                    prop_key = self.tenant_name+"-train"
                    if(comp['memory'] == '80GB'):
                        self.replace_word = "nvidia.com/gpu"
                        self.namespace = prop_key
                    elif(comp['memory'] == '40GB'):
                        self.replace_word = "nvidia.com/mig-7g.40gb"
                        self.namespace = prop_key
                    elif(comp['memory'] == '20GB'):
                        self.replace_word = "nvidia.com/mig-3g.20gb"
                        self.namespace = prop_key
                    else:
                        self.errorMsg="Requested GPU Memory not allowed.Please check with administrator."
                        raise Exception("Requested GPU Memory not allowed.Please check with administrator.") 
                                    
                if(comp['type'] == 'CPU'):
                    if (comp['maxQty']):
                        self.cpu_set_limit = "train.set_cpu_limit(\""+ str(comp['maxQty']) +"\")"      
                    if(comp['memory']):
                        mem=comp['memory'].replace("Gi","")
                        mem=math.ceil(float(mem))
                        memstr=str(mem)+"Gi"
                        self.memory_limit = "train.set_memory_limit(\""+ memstr +"\")"
                                        
                self.dependancyFilePath = "NA"
                new_pipeline_run_name = self.pipeline_data['runName']
                new_pipeline_run_name = new_pipeline_run_name.replace('-','')
                self.pipeline_run_name = new_pipeline_run_name
                if 'env_variables' in self.pipeline_data:
                     self.container_env_var = self.pipeline_data['env_variables']
                else:
                     self.container_env_var = []
                self.preTrainedMdlVal=self.pipeline_data['preTrainedMdl']['artifacts']['uri']

                validate(self.pipeline_data['mainScriptFile'], "mainScriptFile", True)
                python_cmd = self.pipeline_data['mainScriptFile'].split(' ')
                        #self.main_script_file = ""
                for cmd in python_cmd:
                    if(cmd.endswith('.py')):
                        self.main_script_file =  cmd
                        break
                self.train_component_name = self.pipeline_data['stepName'] 
                validate(self.pipeline_data['metricDetails'], "Metric Details", True)
                if self.pipeline_data['metricDetails'] != "NA" and self.pipeline_data['metricDetails'] != None:
                   
                    if(validate(self.pipeline_data['metricDetails']['name'], "", False)):
                        self.metric_name = self.pipeline_data['metricDetails']['name']
                    self.metric_log_path = self.pipeline_data['metricDetails']['logFileUri']  

                    if(self.metric_log_path != None and self.metric_log_path != "NA" and self.metric_log_path != ''):
                        print(self.metric_log_path)
                        self.train_log_dir=os.path.split(self.metric_log_path)[0]
                        print(self.train_log_dir)
                                    
                    if(validate(self.pipeline_data['metricDetails']['regex'], "", False)):
                        metric_regex = self.pipeline_data['metricDetails']['regex']
                        self.metric_regex =metric_regex.replace("\\", "\\\\")
                                    
                self.memory_limit = ""
        except Exception as e:
            print(e)

    def get_kubeflow_code(self, cookie):
                kubeflow_code = self.__kubeflow_template.render(
        PIPELINE_NAME = self.pipeline_name,
        RUN_ARG_NAME = self.run_arg_name,
        PIPELINE_TRAIN_ARGS = self.train_args,
        input_artifacts=self.inputArtifacts,
        pretrained_model_artifacts=self.preTrainedMdlArifacts,
        trial_id=self.prunid,
        pipeline_id=self.pipeline_id,
        INPUT_FILE_NAME = self.main_script_file,
        METRIC_LOG_PATH = self.metric_log_path,
        METRIC_REGEX = self.metric_regex,
        METRIC_NAME= self.metric_name,
        GPU_LIMIT_CONFIG = self.gpu_set_limit,
        PIPELINE_ARGS_JSON = self.pipeline_args_json,
        GPU_REPLACE_WORD = self.replace_word,
        TRAIN_NAMESPACE = self.namespace,
        PIPELINE_RUN_NAME = self.pipeline_run_name,
        AUTH_TOKEN = cookie,
        PIPELINE_URL = self.pipelineUrl,
        PIPL_EXPERIMENT_NAME = self.experimentName,
        PIPL_PRETRAINED_MODEL_PATH = self.preTrainedMdlVal,
        BUCKET_NAME = self.bucketName,
        PIPELINENAME = self.pipeline_name,
        VERSION = self.pipeline_version,
        RUNNAME = self.pipeline_run_name,
        TRAIN_LOG_FILE_DIR = self.train_log_dir,
        CPU_LIMIT_CONFIG = self.cpu_set_limit,
        MEMORY_LIMIT_CONFIG = self.memory_limit,
        PROJECT_ID = self.project_id,
        VOLUMESIGEINGB = self.volume_size_gb,
        MLFLOW_EXPNAME = self.mlflow_expname,
        MLFLOW_URL = self.mlflow_url,
        MLFLOW_LOG_ARTIFACT = self.mlflow_log_artifact,
        globalvariables=self.container_env_var)
                self.replace_component_file("component_keyword_arg_train.yaml","train")
                self.replace_component_file("component_exit_task.yaml","exit_task")
                pipeline_name = self.pipeline_name
                print(pipeline_name)
                file_name = "{}.py".format(self.pipeline_name)
                print("kfp_file_name", file_name)
                self.save_file(kubeflow_code,file_name)
                return kubeflow_code

if __name__ == "__main__":
    kubeflw_obj = CodeGenerationKubeflow()
    get_input_details_url = sys.argv[1]
    cookie = sys.argv[2]
    #env = json.load(get_input_details_url, cookie)
    kubeflw_obj.get_input(get_input_details_url)
    kubeflow_code = kubeflw_obj.get_kubeflow_code(cookie)
    print("pipeine code generated successfully")
   
