[Command-line reference](https://docs.docker.com/engine/reference/commandline/docker/)
#
[Install Docker Engine on Debian 10.3.0-amd64](https://docs.docker.com/engine/install/debian/#install-from-a-package)
```
apt-get remove docker docker-engine docker.io containerd runc
apt-get update
apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
apt-get update
apt-get install docker-ce docker-ce-cli containerd.io
```
## Manage Docker as a non-root user
```$ sudo usermod -aG docker yourUserName```

## Print version information and quit
```$ docker -v```
## Print help message
```
$ docker --help

$ docker info
$ docker system info
$ docker stats

$ sudo vim /lib/systemd/system/docker.service
ExecStart=/usr/bin/dockerd -H 0.0.0.0:2375
$ sudo systemctl daemon-reload
$ sudo service docker restart
$ docker -H 127.0.0.1:2375 run hello-world
```
## .bashrc
```export DOCKER_HOST=127.0.0.1:2375```
## Verify that Docker Engine is installed correctly by running the "hello-world" image
```$ docker run hello-world```
## Search the Docker Hub for images
```$ docker search imageName```
## What images do I have locally
```$ docker images```
## Show only ID of images
```$ docker images -q```
## List containers
```$ docker ps [-aq]```
## Delete container
```$ docker rm <id>/<name>```
## Delete local images
```$ docker rmi [-f] <id>/<name>```
## Delete all images
```$ docker rmi $(docker images -q)```
## Stop one or more running containers
```$ docker stop CONTAINER```
## Build an image from a Dockerfile
```$ docker build -t my-app:v1 .
~/Containers/cont3$ docker build -t localhost:5000/php-apache-app:v5.6 -f Dockerfile .
~/Containers/cont3$ docker build -t localhost:5000/php-apache-app:v7.2 -f Dockerfile.7.2 .
```
## Run a command in a running container
```
$ docker exec [OPTIONS] CONTAINER COMMAND [ARG...]
$ docker exec -it 93c44ecdc022 /bin/bash
```
## Create a new image from a container’s changes
```
$ docker commit [OPTIONS] CONTAINER [REPOSITORY[:TAG]]
$ docker commit dee2cb192c6c ubuntu_with_git
```
## Check what has changed in the container 
```$ docker diff dee2cb192c6c```
## Fetch the logs of a container
```$ docker logs [OPTIONS] CONTAINER```
## Log in to a Docker registry
```$ docker login -u userName -p userPassword```
## Log out from a Docker registry
```$ docker logout [SERVER]```
## Push an image or a repository to a registry
```$ docker push [OPTIONS] NAME[:TAG]```
## Pull an image or a repository from a registry
```$ docker pull [OPTIONS] NAME[:TAG|@DIGEST]```
## Run a command in a new container
```
$ docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
$ docker run -it --rm --env-file ./env.list my-ubuntu /bin/bash
```
## Options:
```
-e MYVAR1 --env MYVAR2=foo --env-file ./env.list
-v /home/USER/docs/app/resourses/:/usr/src/app/resourses/
--rm
-d
-it
-p 127.0.0.1:80:8080/tcp
-P (--publish-all): publish all ports exposed by the container to the unused host ports
$ docker run -d -P tomcat
$ docker port 078e9d12a1c8
8080/tcp -> 0.0.0.0:32772
--restart=on-failure[:max-retries]
--add-host=docker:10.180.0.1 #You can add other hosts into a container’s /etc/hosts
-m 2GB #Specify hard limits on memory available to containers
--device=/dev/sda:/dev/xvdc:rw
```
## docker start/stop/pause/unpause
```
$ docker start [OPTIONS] CONTAINER [CONTAINER...]
$ docker stop [OPTIONS] CONTAINER [CONTAINER...]
$ docker restart [OPTIONS] CONTAINER [CONTAINER...]
```
## Create and manage volumes 
[url](https://docs.docker.com/storage/volumes/)
> If you start a container with a volume that does not yet exist, Docker creates the volume for you.
```
$ docker volume create my-vol
$ docker volume ls
$ docker volume inspect my-vol
$ docker volume rm my-vol
$ docker run -d --name devtest -v myvol2:/app nginx:latest
$ docker run -d --name=nginxtest -v nginx-vol:/usr/share/nginx/html nginx:latest
$ docker run -i -t -v ~/docker_ubuntu:/host_directory ubuntu:16.04 /bin/bash
```
## To remove all unused volumes and free up space
```$ docker volume prune```
## Networking
[url](https://docs.docker.com/network/)
>If you don’t specify the --driver option, the command automatically creates a bridge network for you. 
>When you install Docker Engine it creates a bridge network automatically. 
>This network corresponds to the docker0 bridge that Engine has traditionally relied on. 
>When you launch a new container with docker run it automatically connects to this bridge network. 
>You cannot remove this default bridge network, but you can create new ones using the network create command.
