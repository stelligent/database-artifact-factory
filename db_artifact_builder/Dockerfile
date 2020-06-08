FROM alpine
ENV DB_PASSWORD ''
ENV AWS_PROFILE ''

RUN apk add bash python3 

RUN pip3 install requests sceptre

#copied from elsewhere by ImageBuilder
ADD ./db_artifact /db_artifact
COPY sceptre_config_clone.yml /db_artifact/sceptre/config/prod/clone.yaml

ENTRYPOINT PYTHONPATH=. python3 -m db_artifact.docker_converge_entrypoint
