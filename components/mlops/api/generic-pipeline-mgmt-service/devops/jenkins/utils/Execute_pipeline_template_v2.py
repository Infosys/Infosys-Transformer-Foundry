# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import os
import json
import uuid
import jinja2
import time
import urllib.request
import sys

TEMPLATE_PATH = "/var/lib/jenkins/workspace/utils/templates/prod/pipln_v2/"
TEMPLATE_NAME = "execute_kfpipeline_template_v4.9.j2"

class CodeGenerationKubeflow:
    def __init__(self,get_piplndata_url,kfp_url,cookie,experiment_name) -> None:
        self.__env = jinja2.Environment(loader=jinja2.FileSystemLoader(
            TEMPLATE_PATH), trim_blocks=True, lstrip_blocks=True)
        self.__kubeflow_template = self.__env.get_template(TEMPLATE_NAME)

        urlinput = urllib.request.urlopen(get_piplndata_url)
        input_data = json.loads(urlinput.read())
        self.pipeline_data=input_data['data']['inputData']
        self.kfp_url=kfp_url
        self.cookie=cookie
        self.experiment_name=experiment_name
        self.namespace ="${namespace}"
        self.gpuMigSlice = "nvidia.com/gpu"

    def get_kubeflow_code(self):
        func_args = ""
        run_arg_name = ""
        pipeline_args_json = "{"
        format_brackets = ""
        train_args = ""
        i = 0
        for run_arg in self.pipeline_data['runArguments']:
            i = i + 1
            format_brackets = format_brackets + "{} {} "
            run_arg_name = run_arg_name + run_arg['name'] +","
            train_args = train_args + "\\x27--" + run_arg['name'] + "\\x27, " + run_arg['name'] + ","
            pipeline_args_json = pipeline_args_json+ "\""+run_arg['name']+ "\": \"" +run_arg['argValue']+ "\","
        print(pipeline_args_json)
        if pipeline_args_json != "{" and len(pipeline_args_json) != 1:
            pipeline_args_json = pipeline_args_json[0:(len(pipeline_args_json)-1)]
        pip_args = pipeline_args_json + "}"

        # render template
        kueflow_code = self.__kubeflow_template.render(
            description=self.pipeline_data['description'],
            pipeline_name=self.pipeline_data['pipeline']['name'],
            flow=self.pipeline_data['pipeline']['flow'],
            pip_volume=self.pipeline_data['pipeline']['volume'],	
            pipeline_variables=self.pipeline_data['pipeline']['variables'],
            pipeline_data_storage=self.pipeline_data['pipeline']['dataStorage'],
            globalvariables=self.pipeline_data['pipeline']['globalVariables'],
            unique_id=str(uuid.uuid4())[:8],
            pipeline_url = self.kfp_url,
            auth_token = self.cookie,
            experiment_name = self.experiment_name,
            pipeline_id = self.pipeline_data['pipelineId'],
            execution_id = self.pipeline_data['executionId'],
            project_id = self.pipeline_data['projectId'],
            pipeline_run_name = self.pipeline_data['runName'],
            kfp_namespace = self.namespace,
            gpu_mig_slice = self.gpuMigSlice,
            pipln_args = pip_args,
            yaml_file_name="pipeline.yaml"
        )
        return kueflow_code

if __name__ == "__main__":
    # Initialize the class
    get_piplndata_url = sys.argv[1]
    workspace_path=sys.argv[2]
    cookie = sys.argv[3]
    kfp_url = sys.argv[4]
    experiment_name = sys.argv[5]
    kubeflw_obj = CodeGenerationKubeflow(get_piplndata_url,kfp_url,cookie,experiment_name)
    kubeflow_code = kubeflw_obj.get_kubeflow_code()
    code_generation_python_file=workspace_path+"/code_generation.py"
    with open(code_generation_python_file, 'w') as f:	
        f.write(kubeflow_code)