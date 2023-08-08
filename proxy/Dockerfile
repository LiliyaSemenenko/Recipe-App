# base nginx image
# put 'unprivilaged' to avoid security issues and run app as root user
FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="Liliya Semenenko"

# copy './default.conf.tp' and store it in docker image '/etc/nginx/default.conf.tpl'
COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

# default values for container's environment variables that are running from this image
# the port that our server will listen on
ENV LISTEN_PORT=8000
# where uwsgi app is running
ENV APP_HOST=app
# port that uwsgi app runs on
ENV APP_PORT=9000

# switch to the root user to set up an image to get it ready
# (run commands on 'RUN' below)
USER root

    # create a new dir /vol/static to storee the static files
RUN mkdir -p /vol/static && \
    # set permissions to 755 (to read contents of static file)
    chmod 755 /vol/static && \
    # set permissions on this file so nginx user can modify it
    # (required by 'envsubst' command in run.sh)
    touch /etc/nginx/conf.d/default.conf && \
    # making nginx user that exists as part as this base image
    # making it an owner of the new file we created
    chown nginx:nginx / etc/nginx/conf.d/default.conf && \
    # add execute permissions to /run.sh script
    chmod +x /run.sh

# set up a default volume to this image
VOLUME /col/static

# switch from root user (privileged) to nginx user (unprevileged)
USER nginx

# call instance to run this image
CMD ["/run.sh"]