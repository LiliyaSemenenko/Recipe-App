# TO BUILD: docker build -t app-dev -f Dockerfile .

# Commnads:
# apk [options] command: (Alpine Package Keeper) package of Alpine Linux. It handles all the package management operations including searching, installing, upgrading, listing, and removing software packages
# mkdir [<drive>:]<path>: creates intermediate directories in a specified path.
# chown [OPTION]... [OWNER][:[GROUP]] FILE...: changes the user and/or group ownership of each given file.
# chmod [OPTION]... MODE[,MODE]... FILE...: sets the permissions of files or directories.


FROM python:3.9-alpine3.18
LABEL maintainer="liliyasemenenko"

ENV PYTHONUNBUFFERED 1
ENV PATH="/usr/local/bin:$PATH"

# Install Node.js and npm
# RUN apk add --update --no-cache nodejs npm

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# creating a dir scripts used for creating helper scripts run by docker app
COPY ./scripts /scripts
COPY ./app /app
WORKDIR /app
# port
EXPOSE 8000

# default value for Development mode is false
ARG DEV=false

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
#
    # install postgresql-client package inside Alpine image to connect Psycopg2 to Postgresql
    # remains dependencies on docker image after it's built
    apk add --update --no-cache postgresql-client jpeg-dev && \
    # install virtual dependency package (groups them inside the "tem-build-deps" dir so that we can remove them later)
    # should match line 38: .tmp-build-deps
    apk add --update --no-cache --virtual .tmp-build-deps \
        # list of packages that need to be installed
        # linux-headers: requirment for uwsgi package installation
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
#
    /py/bin/pip install -r /tmp/requirements.txt && \
#
    # install dev dependencies is dev=true on docker image
    if [ $DEV = "true" ]; \
        # tmp for current location
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
#
    rm -rf /tmp && \
#
    # remove packages inside "tmp-build-deps" installed on line 24: build-base postgresql-dev musl-dev zlib zlib-dev linux-headers
    # to keep Dockerfile lightweight and clean
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    # to make scripts dir executable
    chmod -R +x /scripts

# change path dir to scripts
ENV PATH="/scripts:/py/bin:$PATH"

USER django-user

# name of the script that runs the app
# default command that's run for docker containers that are spawned
# from our image that's built from this Docker file.
# , "node", "server.js"
CMD ["run.sh"]
