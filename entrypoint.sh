
echo "PIPELINE_YAML_RAW_URL : $PIPELINE_YAML_RAW_URL"


if [ -z ${PIPELINE_YAML_RAW_URL+x} ]; then
    echo "Provide a raw url file with yaml of complied kfp"
    exit 1
fi

python3 -u ./init_pipeline.py