# Nginx
#
# VERSION               0.0.1
FROM      ubuntu
LABEL Description="This image is used to start the foobar executable" Vendor="ACME Products" Version="1.0"
RUN apt-get update && apt-get install -y inotify-tools nginx apache2 openssh-server


ARG  CODE_VERSION=latest
FROM base:${CODE_VERSION}

LABEL maintainer="SvenDowideit@home.org.au"

ENV foo /bar
WORKDIR ${foo}   # WORKDIR /bar

COPY /home/user/app /app

RUN apt-get update && apt-ger install -y mc
RUN ["executable", "param1", "param2"]

ADD hom* /mydir/        # adds all files starting with "hom"
ADD hom?.txt /mydir/    # ? is replaced with any single character, e.g., "home.txt"

EXPOSE <port> [<port>/<protocol>...]
EXPOSE 80/tcp
EXPOSE 80/udp

# Understand how CMD and ENTRYPOINT interact
https://docs.docker.com/engine/reference/builder/
ENTRYPOINT ['cowsay']
ENTRYPOINT ["executable", "param1", "param2"]

HEALTHCHECK [OPTIONS] CMD command (check container health by running a command inside the container)
HEALTHCHECK NONE (disable any healthcheck inherited from the base image)
The options that can appear before CMD are:
--interval=DURATION (default: 30s)
--timeout=DURATION (default: 30s)
--start-period=DURATION (default: 0s)
--retries=N (default: 3)

# The USER instruction sets the user name (or UID) and optionally the user group (or GID) to use when running the image and 
# for any RUN, CMD and ENTRYPOINT instructions that follow it in the Dockerfile.
USER <user>[:<group>]
or
USER <UID>[:<GID>]
