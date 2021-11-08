#!/usr/bin/env python
# coding: utf-8
# In[53]:
# GCP project to use
#
# settings for project: kubeflow-rl
PROJECT="kubeflow-dev"
# Bucket to use
BUCKET=PROJECT+"-jlewi"
# K8s cluster to use
CLUSTER="gpu-cluster"
ZONE="us-central1-a"
NAMESPACE="jlewi-rl"
# Root directory for the kubeflow-rl repository
ROOT_DIR = "/home/jovyan/git_kubeflow-rl"
SECRET_NAME = "kubeflow-rl-gcp"
KEY_FILE="/home/jovyan/jlewi-kubeflow-rl@kubeflow-dev.iam.gserviceaccount.com.json"
APP_DIR=os.path.join(ROOT_DIR, "rl-app")
KSBIN=os.path.join("/home/jovyan/ks_0.8.0_linux_amd64/ks")
IMAGE="gcr.io/kubeflow-dev/agents-ppo:cpu-cae5b3af"
# ksonnet env to use
ENV="jlewi-dev"
# The hostname used for Kubeflow
HOSTNAME="dev.kubeflow.org"
# In[48]:
# GCP project to use
#
# settings for project: kubeflow-rl
#PROJECT="kubeflow-rl"
# Bucket to use
#BUCKET=PROJECT+"-kf"
# K8s cluster to use
#CLUSTER="kubeflow"
#ZONE="us-east1-d"
#NAMESPACE="rl"
# Root directory for the kubeflow-rl repository
#ROOT_DIR = "/home/jovyan/git_kubeflow-rl"
#SECRET_NAME = "kubeflow-rl-gcp"
#KEY_FILE="/home/jovyan/kubeflow-rl-f673306814d4.json"
IMAGE="gcr.io/kubeflow-rl/agents-ppo:cpu-cae5b3af"
# In[8]:
get_ipython().system('gcloud auth activate-service-account --key-file={KEY_FILE}')
# In[9]:
get_ipython().system('gsutil mb -p {PROJECT} gs://{BUCKET}')
# In[12]:
get_ipython().system('gcloud container clusters --project={PROJECT} --zone={ZONE} get-credentials {CLUSTER}')
# In[13]:
get_ipython().system('kubectl create namespace {NAMESPACE}')
# In[34]:
# For this to work you first need to use kubectl exec -ti to login as root
# You can than do chmod a+rw /usr/local/bin
get_ipython().system('wget -O ~/ks_0.8.0_linux_amd64.tar.gz --quiet https://github.com/ksonnet/ksonnet/releases/download/v0.8.0/ks_0.8.0_linux_amd64.tar.gz')
get_ipython().system('tar -C ~/ -zvxf ~/ks_0.8.0_linux_amd64.tar.gz ')
# Move ks appears to cause an exec format error when we run it.
#!mv ks_0.8.0_linux_amd64/ks /usr/local/bin/ks
#!chmod a+x /usr/local/bin/ks
# In[14]:
SECRET_FILE_NAME="secret.json"
get_ipython().system('kubectl create -n {NAMESPACE} secret generic {SECRET_NAME}  --from-file={SECRET_FILE_NAME}={KEY_FILE}')
# In[26]:
# Change to the ksonnet directory
os.chdir(os.path.join(APP_DIR))
# In[38]:
# Check your cluster and see if that matches one of the existing ksonnet environments
# You want the kubernetes master server to be the same as the server listed for the ks environment
get_ipython().system('kubectl cluster-info')
get_ipython().system('{KSBIN} env list')
# In[41]:
# Create the environment if needed
get_ipython().system('{KSBIN} env add {ENV}')
# In[50]:
import datetime
import uuid
import os
os.chdir(os.path.join(ROOT_DIR, "rl-app"))
HPARAM_SET="pybullet-kuka-ff"
now=datetime.datetime.now()
JOB_SALT=now.strftime("%m%d-%H%M") + "-" + uuid.uuid4().hex[0:4]
JOB_NAME=HPARAM_SET + "-" + JOB_SALT
LOG_DIR="gs://{0}/jobs/{1}".format(BUCKET, JOB_NAME)
get_ipython().system('{KSBIN} param set --env={ENV} agents-ppo namespace {NAMESPACE}')
get_ipython().system('{KSBIN} param set --env={ENV} agents-ppo gcp_project {PROJECT}')
get_ipython().system('{KSBIN} param set --env={ENV} agents-ppo image {IMAGE}')
# Dev cluster only has 4 CPU machine's; ideally would like to use 30 CPUs
get_ipython().system('{KSBIN} param set --env={ENV} agents-ppo num_cpu 2')
get_ipython().system('{KSBIN} param set --env={ENV} agents-ppo job_tag {JOB_SALT}')
get_ipython().system('{KSBIN} param set --env={ENV} agents-ppo log_dir {LOG_DIR}')
get_ipython().system('{KSBIN} param set --env={ENV} agents-ppo name {JOB_NAME}')
get_ipython().system('{KSBIN} param set --env={ENV} agents-ppo gcp_secret {SECRET_NAME}')
get_ipython().system('{KSBIN} param set --env={ENV} agents-ppo secret_file_name {SECRET_FILE_NAME}')
get_ipython().system('{KSBIN} show {ENV} -c agents-ppo')
get_ipython().system('{KSBIN} apply {ENV} -c agents-ppo')
# In[55]:
get_ipython().system('kubectl get tfjobs.kubeflow.org -n {NAMESPACE} -o yaml {JOB_NAME}')
# In[56]:
get_ipython().system('kubectl get pods -n {NAMESPACE} --show-all')
# In[57]:
import subprocess
master_pod = subprocess.check_output(["kubectl", "-n", NAMESPACE, "get", "pods", "--selector=tf_job_name=" + JOB_NAME,
                                      "-o", "jsonpath='{.items[*].metadata.name}'"]).decode("utf-8")
print(master_pod)
get_ipython().system('kubectl -n {NAMESPACE} get pods -o yaml {master_pod}')
# In[58]:
get_ipython().system('kubectl logs -n {NAMESPACE} {master_pod}')
# In[54]:
get_ipython().system('{KSBIN} param set --env={ENV} tensorboard name {JOB_NAME}')
get_ipython().system('{KSBIN} param set --env={ENV} tensorboard namespace {NAMESPACE}')
get_ipython().system('{KSBIN} param set --env={ENV} tensorboard log_dir {LOG_DIR}')
get_ipython().system('{KSBIN} param set --env={ENV} tensorboard secret {SECRET_NAME}')
get_ipython().system('{KSBIN} param set --env={ENV} tensorboard secret_file_name {SECRET_FILE_NAME}')
print("Tensorboard will be available at:")
print("https://" + HOSTNAME + "/tensorboard/" + JOB_NAME+"/")
get_ipython().system('{KSBIN} show {ENV} -c tensorboard')
get_ipython().system('{KSBIN} apply {ENV} -c tensorboard')
# In[3]:
get_ipython().system('kubectl delete tfjobs -n {NAMESPACE} {JOB_NAME}')
# In[9]:
import io
import base64
from IPython.display import HTML
# Replace with the 
mp4_path = 'render.mp4'
video = io.open(mp4_path, 'r+b').read()
encoded = base64.b64encode(video)
HTML(data='''<video alt="test" controls>
                <source src="data:video/mp4;base64,{0}" type="video/mp4" />
             </video>'''.format(encoded.decode('ascii')))