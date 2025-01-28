This job use/ creates a Openshift AI data science pipeline and, experiment, and run's it.


example for pipeline creation can be seen in this repo: **TODO**

## Mandatory Variables

#### `PIPELINE_YAML_RAW_URL`

Defines the **RAW** URL of the compiled KFP pipeline program.



## Optional Variables (with Defaults)

#### `PIPELINE_NAME`

Specifies the name of the pipeline.

Default Name: Default


#### `EXPERIMENT_NAME`

Specifies the name of the experiment.

Default Name: Default


#### `RUN_NAME`

Specifies the name of the run.

Default: 1


#### `PIPELINE_PARAMS`

Additional parameters for the pipeline in JSON dict string format.

Example: '{"load_from_repo": True, "load_from_s3": False, "load_from_urls": False}'
