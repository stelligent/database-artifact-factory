FROM alpine
ENV CREATE_MODE create
ENV DB_USERNAME ''
ENV DB_PASSWORD ''
ENV AWS_PROFILE ''
ARG DB_TARGET_NAME

RUN apk add bash python3 openjdk11 

RUN mkdir /liquibase && \
    cd /liquibase && \
    wget https://github.com/liquibase/liquibase/releases/download/v3.9.0/liquibase-3.9.0.zip && \
    unzip liquibase-3.9.0.zip && \
    wget https://jdbc.postgresql.org/download/postgresql-42.2.12.jar

RUN pip3 install requests sceptre

#copied from elsewhere by ImageBuilder
ADD ./db_artifact /db_artifact
ADD changelog.yaml /liquibase/changelog.yaml
COPY sceptre_config_create.yml /db_artifact/sceptre/config/prod/create.yaml
COPY sceptre_config_clone.yml /db_artifact/sceptre/config/prod/clone.yaml

RUN echo $DB_TARGET_NAME > /DB_TARGET_NAME

ENTRYPOINT PYTHONPATH=. python3 -m db_artifact.docker_converge_entrypoint $CREATE_MODE
