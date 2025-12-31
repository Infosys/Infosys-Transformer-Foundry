# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import kfp
import kfp.dsl as dsl
from kubernetes import client as k8s_client
from kfp import components
import kfp.compiler as compiler
import gzip
import string
import time
import tarfile

run_train_op=components.load_component('component_train.yaml')

run_exit_task_op=components.load_component('component_exit_task.yaml')

@dsl.pipeline(
	name='PIPELINE_NAME',
	description='null')

def PIPELINE_NAME(RUN_ARG_NAME):

	dsl.get_pipeline_conf().set_image_pull_secrets([k8s_client.V1ObjectReference(name="artifactory-cred")])
	train_params=PIPELINE_TRAIN_ARGS
	run_id=dsl.RUN_ID_PLACEHOLDER
        	
	config_ref=k8s_client.V1ConfigMapEnvSource(name='minio-configuration')
	env_config_from=k8s_client.V1EnvFromSource(config_map_ref=config_ref)
	secret_ref1=k8s_client.V1SecretKeySelector(key='awsAccessKeyID',name='minio-secret-1')
	value_from1=k8s_client.V1EnvVarSource(secret_key_ref=secret_ref1)
	env_var1 = k8s_client.V1EnvVar(name='AWS_ACCESS_KEY_ID', value_from=value_from1)
	secret_ref2=k8s_client.V1SecretKeySelector(key='awsSecretAccessKey',name='minio-secret-1')
	value_from2=k8s_client.V1EnvVarSource(secret_key_ref=secret_ref2)
	env_var2 = k8s_client.V1EnvVar(name='AWS_SECRET_ACCESS_KEY', value_from=value_from2)

	config_ref1=k8s_client.V1ConfigMapEnvSource(name='nutanix-configuration')
	env_config_from1=k8s_client.V1EnvFromSource(config_map_ref=config_ref1)

	secret_ref5=k8s_client.V1SecretKeySelector(key='awsAccessKeyID',name='nutanix-secret-1')
	value_from5=k8s_client.V1EnvVarSource(secret_key_ref=secret_ref5)
	env_var8 = k8s_client.V1EnvVar(name='AWS_ACCESS_KEY_ID', value_from=value_from5)

	secret_ref6=k8s_client.V1SecretKeySelector(key='awsSecretAccessKey',name='nutanix-secret-1')
	value_from6=k8s_client.V1EnvVarSource(secret_key_ref=secret_ref6)
	env_var9 = k8s_client.V1EnvVar(name='AWS_SECRET_ACCESS_KEY', value_from=value_from6)

	secret_ref3=k8s_client.V1SecretKeySelector(key='artifactoryID',name='artifactory-creds')
	value_from3=k8s_client.V1EnvVarSource(secret_key_ref=secret_ref3)
	env_var3 = k8s_client.V1EnvVar(name='ARTIFACTORY_UN', value_from=value_from3)
	secret_ref4=k8s_client.V1SecretKeySelector(key='artifactoryToken',name='artifactory-creds')
	value_from4=k8s_client.V1EnvVarSource(secret_key_ref=secret_ref4)
	env_var4 = k8s_client.V1EnvVar(name='ARTIFACTORY_TOKEN', value_from=value_from4)
	volume_mount = k8s_client.V1VolumeMount(mount_path='/dev/shm',name='dshm')
	empty_dir_src=k8s_client.V1EmptyDirVolumeSource(medium='Memory')
	vol1 = k8s_client.V1Volume(name='dshm',empty_dir=empty_dir_src)
	volume={"/dev/shm": vol1}
	volume_mount1 = k8s_client.V1VolumeMount(mount_path='/s3util',name='s3-utility-vol')
	empty_dir_src1=k8s_client.V1EmptyDirVolumeSource(medium='Memory')
	vol2 = k8s_client.V1Volume(name='s3-utility-vol',empty_dir=empty_dir_src1)
	volume2={"/s3util": vol2}
	volume_mount2 = k8s_client.V1VolumeMount(mount_path='/mnt/models',name='storage-vol')
	empty_dir_src2=k8s_client.V1EmptyDirVolumeSource(medium='Memory')
	vol3 = k8s_client.V1Volume(name='storage-vol',empty_dir=empty_dir_src2)
	volume3={"/mnt/models": vol3}
	volume_mount3 = k8s_client.V1VolumeMount(mount_path='/s3cert',name='s3-cert-vol')
	pvc = k8s_client.V1PersistentVolumeClaimVolumeSource(claim_name='s3-util-vol')
	vol4 = k8s_client.V1Volume(name='s3-cert-vol', persistent_volume_claim=pvc)
	volume4={"/s3cert": vol4}
	volume_mount4 = k8s_client.V1VolumeMount(mount_path='TRAIN_LOG_FILE_DIR',name='log-vol')
	empty_dir_src3=k8s_client.V1EmptyDirVolumeSource(medium='Memory')
	vol5 = k8s_client.V1Volume(name='log-vol',empty_dir=empty_dir_src3)
	volume5={"TRAIN_LOG_FILE_DIR": vol5}
	volume_mount5 = k8s_client.V1VolumeMount(mount_path='/output/genModel/',name='model-store-vol')
	empty_dir_src4=k8s_client.V1EmptyDirVolumeSource(medium='Memory')
	vol6 = k8s_client.V1Volume(name='model-store-vol',empty_dir=empty_dir_src4)
	volume6={"/output/genModel/": vol6}

	env_var5 = k8s_client.V1EnvVar(name='AI_CLD_PRETRAINED_MDL_PATH', value='/mnt/models')
	env_var6 = k8s_client.V1EnvVar(name='AICLD_MODEL_STORE_PATH', value='/output/genModel/')
	env_var7 = k8s_client.V1EnvVar(name='AICLD_INPUT_ARTIFACTS_PATH', value='/input/artifacts/')
	env_var10 = k8s_client.V1EnvVar(name='LOG_FILE_PATH', value='TRAIN_LOG_FILE_PATH')
	env_var11 = k8s_client.V1EnvVar(name='S3_LOG_FILE_PATH', value='PROJECT_ID/pipeline/PIPELINENAME/VERSION/runs/RUNNAME/outputartifacts/logs/')

	capab=k8s_client.V1Capabilities(add=['SYS_ADMIN'])
	securityctx=k8s_client.V1SecurityContext(privileged=True,capabilities=capab)

	storage_op = dsl.Sidecar(
				name="download-from-s3",
				image="${STORAGE_INIT_IMAGE}",
				args=["PIPL_PRETRAINED_MODEL_PATH", "/mnt/models"],
				mirror_volume_mounts=True
          )
	storage_op.add_env_from(env_config_from1)
	storage_op.add_env_variable(env_var8)
	storage_op.add_env_variable(env_var9)

	util_storage_op = dsl.Sidecar(
				name="download-util-files-from-s3",
				image="${KF_STORAGE_INIT_IMAGE}",
				args=["s3://mlpipeline/utility", "/s3util"],
				mirror_volume_mounts=True
          )
	util_storage_op.add_env_from(env_config_from)
	util_storage_op.add_env_variable(env_var1)
	util_storage_op.add_env_variable(env_var2)

	log_stream_op = dsl.Sidecar(
				name="stream-log-s3",
				image="${LOG_STREAMING_IMAGE}",
                command=["/app/startup.sh"],
				mirror_volume_mounts=True
          )
	log_stream_op.add_env_from(env_config_from)
	log_stream_op.add_env_variable(env_var1)
	log_stream_op.add_env_variable(env_var2)
	log_stream_op.add_env_variable(env_var10)
	log_stream_op.add_env_variable(env_var11)

	upload_s3_op = dsl.Sidecar(
				name="upload-s3",
				image="${UPLOAD_TO_S3_IMAGE}",
				command=["/app/runScript"],
				args=["/output/genModel/", "s3://BUCKET_NAME/PROJECT_ID/pipeline/PIPELINENAME/VERSION/runs/RUNNAME/outputartifacts/models"],
				mirror_volume_mounts=True
          )
	upload_s3_op.add_env_from(env_config_from)
	upload_s3_op.add_env_variable(env_var1)
	upload_s3_op.add_env_variable(env_var2)

	exit_task = run_exit_task_op(
				run_id=run_id,
				run_status='{{workflow.status}}'
				)
	exit_task.add_init_container(util_storage_op)
	exit_task.add_pvolumes(volume2)
	exit_task.execution_options.caching_strategy.max_cache_staleness ="P0D"
	with dsl.ExitHandler(exit_task):
				train=run_train_op(
						filename="INPUT_FILE_NAME",
						parameters=train_params,
						log_path="METRIC_LOG_PATH",
						rgex="METRIC_REGEX",
						metricname="METRIC_NAME",
						run_id=run_id
				)
				train.add_pvolumes(volume)
				train.add_pvolumes(volume2)
				train.add_pvolumes(volume3)
				train.add_pvolumes(volume4)
				train.add_pvolumes(volume5)
				train.add_pvolumes(volume6)
				train.add_init_container(storage_op)
				train.add_init_container(util_storage_op)
				train.add_sidecar(log_stream_op)
				train.add_sidecar(upload_s3_op)
				train.add_env_from(env_config_from)
				train.add_env_variable(env_var1)
				train.add_env_variable(env_var2)
				train.add_env_variable(env_var3)
				train.add_env_variable(env_var4)
				train.add_env_variable(env_var5)
				train.add_env_variable(env_var6)
				train.add_env_variable(env_var7)
				train.add_pod_label("pipeline/trialid","TRIAL_ID")
				train.add_pod_label("pipeline/pipelineid","PIPELINE_ID")
				train.set_security_context(securityctx)
				train.set_image_pull_policy('Always')
				GPU_LIMIT_CONFIG
				CPU_LIMIT_CONFIG
				MEMORY_LIMIT_CONFIG
				train.execution_options.caching_strategy.max_cache_staleness ="P0D"


args=PIPELINE_ARGS_JSON

if __name__ == '__main__':
	compiler.Compiler().compile(PIPELINE_NAME,__file__ +'.tar.gz')
	tfile = tarfile.open(__file__ +'.tar.gz')
	tfile.extractall()
	tfile.close()
	file = open('pipeline.yaml', "r")
	outfile=open(__file__ + '.yaml', "w")
	word='nvidia.com/gpu'
	replaceword='GPU_REPLACE_WORD'
	for line in file:
		if word in line:
			new_line =line.replace(word,replaceword)
			outfile.write(new_line)
		else:
			outfile.write(line)

	outfile.close()
	file.close()
	pipelin_run = kfp.Client(host='PIPELINE_URL',cookies='authservice_session=AUTH_TOKEN').create_run_from_pipeline_package(__file__ + '.yaml', arguments=args,run_name="PIPELINE_RUN_NAME",namespace="TRAIN_NAMESPACE",experiment_name="PIPL_EXPERIMENT_NAME")
	print(pipelin_run)  