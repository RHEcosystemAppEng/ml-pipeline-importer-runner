import kfp
import datetime
import requests
import os 
import json

PIPELINE_NAME = os.getenv('PIPELINE_NAME', 'Default')
EXPERIMENT_NAME = os.getenv('EXPERIMENT_NAME','Default')
RUN_NAME = os.getenv('RUN_NAME', '1')
URL = os.getenv('PIPELINE_YAML_RAW_URL')
PIPELINE_PARAMS = os.getenv('PIPELINE_PARAMS', None)

YAML_FILE = 'pipeline.yaml'
dt = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

def load_yaml_from_raw_url(url: str):
    text = requests.get(url).text
    with open(YAML_FILE, 'w') as f:
        f.write(text)
    return YAML_FILE

def get_first_pipeline_version(client: kfp.Client, pipeline_id, version_name):
    response = client.list_pipeline_versions(pipeline_id=pipeline_id)
    
    if response and response.pipeline_versions:
        for version in response.pipeline_versions:
            if version.display_name == version_name:
                return version.pipeline_version_id
    return None

def get_pipeline_id_by_name(client, pipeline_name):
    pipelines = client.list_pipelines()

    if pipelines and pipelines.pipelines:
        for pipeline in pipelines.pipelines:
            if pipeline.display_name == pipeline_name:
                return pipeline
    return None

def get_experiment_id(client:kfp.Client, experiment_name: str):
    response = client.list_experiments()
    
    if response and response.experiments:
        for experiment in response.experiments:
            if experiment.display_name == experiment_name:
                return experiment.experiment_id
    return None

if __name__ == '__main__':
    with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r') as namespace_file:
        namespace = namespace_file.read().strip()
    with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as token_file:
        token = token_file.read().strip()
    pipeline_file = load_yaml_from_raw_url(URL)
    pipeline_param = json.loads(PIPELINE_PARAMS) if PIPELINE_PARAMS else None
    # Connect to client
    dspa_host = f"ds-pipeline-dspa.{namespace}.svc.cluster.local"
    route = f"https://{dspa_host}:8443"
    client = kfp.Client(host=route, verify_ssl=False, existing_token=token)

    pipeline = get_pipeline_id_by_name(client, PIPELINE_NAME)

    if pipeline:
        
        pipeline_version_name = f"{PIPELINE_NAME} version {dt}"

        pipeline = client.upload_pipeline_version(
            pipeline_package_path=pipeline_file,
            pipeline_version_name=pipeline_version_name,
            pipeline_id=pipeline.pipeline_id
        )

        pipeline_version_id = pipeline.pipeline_version_id
    else:      

        pipeline_version_name = PIPELINE_NAME

        pipeline = client.upload_pipeline(
            pipeline_package_path=pipeline_file,
            pipeline_name=PIPELINE_NAME
        )

        pipeline_version_id = get_first_pipeline_version(client, pipeline.pipeline_id, pipeline_version_name)
    
    experiment_id = get_experiment_id(client, EXPERIMENT_NAME)
    if experiment_id is None:
        experiment_id = client.create_experiment(name=EXPERIMENT_NAME).experiment_id

    run = client.run_pipeline(
        experiment_id=experiment_id,
        job_name=RUN_NAME,
        params=pipeline_param,
        pipeline_id=pipeline.pipeline_id,
        version_id=pipeline_version_id
    )