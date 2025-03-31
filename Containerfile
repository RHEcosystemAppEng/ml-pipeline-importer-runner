FROM registry.access.redhat.com/ubi9/python-311

USER root
WORKDIR /app/

COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

COPY entrypoint.sh /app/
COPY init_pipeline.py /app/
RUN chmod -R 777 /app/ && ls -la /app/
