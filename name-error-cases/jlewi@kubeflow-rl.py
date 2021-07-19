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
# For this to work you first need to use kubectl exec -ti to login as root
# You can than do chmod a+rw /usr/local/bin
# Move ks appears to cause an exec format error when we run it.
#!mv ks_0.8.0_linux_amd64/ks /usr/local/bin/ks
#!chmod a+x /usr/local/bin/ks
SECRET_FILE_NAME="secret.json"
# Change to the ksonnet directory
os.chdir(os.path.join(APP_DIR))
# Check your cluster and see if that matches one of the existing ksonnet environments
# You want the kubernetes master server to be the same as the server listed for the ks environment
# Create the environment if needed
import datetime
import uuid
import os
os.chdir(os.path.join(ROOT_DIR, "rl-app"))
HPARAM_SET="pybullet-kuka-ff"
now=datetime.datetime.now()
JOB_SALT=now.strftime("%m%d-%H%M") + "-" + uuid.uuid4().hex[0:4]
JOB_NAME=HPARAM_SET + "-" + JOB_SALT
LOG_DIR="gs://{0}/jobs/{1}".format(BUCKET, JOB_NAME)
# Dev cluster only has 4 CPU machine's; ideally would like to use 30 CPUs
import subprocess
master_pod = subprocess.check_output(["kubectl", "-n", NAMESPACE, "get", "pods", "--selector=tf_job_name=" + JOB_NAME,
                                      "-o", "jsonpath='{.items[*].metadata.name}'"]).decode("utf-8")
print(master_pod)
print("Tensorboard will be available at:")
print("https://" + HOSTNAME + "/tensorboard/" + JOB_NAME+"/")
PROXY_PORT=8001
url=print("http://127.0.0.1:{proxy_port}/api/v1/proxy/namespaces/{namespace}/services/{service_name}:80/".format(
    proxy_port=PROXY_PORT, namespace=NAMESPACE, service_name=JOB_NAME + "-tb"))
print(url)
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