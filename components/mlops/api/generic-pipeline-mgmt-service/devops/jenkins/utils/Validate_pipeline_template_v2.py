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
TEMPLATE_NAME = "validate_kfpipeline_template_v4.9.j2"

class CodeGenerationKubeflow:
    def __init__(self,pipeline_url) -> None:
        self.__env = jinja2.Environment(loader=jinja2.FileSystemLoader(
            TEMPLATE_PATH), trim_blocks=True, lstrip_blocks=True)
        self.__kubeflow_template = self.__env.get_template(TEMPLATE_NAME)

        urlinput = urllib.request.urlopen(pipeline_url)
        input_data = json.loads(urlinput.read())
        self.pipeline_data=input_data['data']['inputData']
	    
    def get_kubeflow_code(self):
        # render template
        kueflow_code = self.__kubeflow_template.render(
            description=self.pipeline_data['description'],
            pipeline_name=self.pipeline_data['pipeline']['name'],
            flow=self.pipeline_data['pipeline']['flow'],
            pip_volume=self.pipeline_data['pipeline']['volume'],	
            pipeline_variables=self.pipeline_data['pipeline']['variables'],
            pipeline_data_storage=self.pipeline_data['pipeline']['dataStorage'],
            pipeline_inputartifacts_flag=self.pipeline_data['inputArtifacts_flag'],
            globalvariables=self.pipeline_data['pipeline']['globalVariables'],
            unique_id=str(uuid.uuid4())[:8],
            yaml_file_name="pipeline.yaml"
        )
        print(self.pipeline_data['pipeline']['dataStorage'])
        return kueflow_code

if __name__ == "__main__":
    # Initialize the class
    pipeline_url = sys.argv[1]
    workspace_path=sys.argv[2]
    kubeflw_obj = CodeGenerationKubeflow(pipeline_url)
    kubeflow_code = kubeflw_obj.get_kubeflow_code()
    code_generation_python_file=workspace_path+"/code_generation.py"
    with open(code_generation_python_file, 'w') as f:	
        f.write(kubeflow_code)