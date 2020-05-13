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
# Manage Docker as a non-root user
```$ sudo usermod -aG docker yourUserName```

# Print version information and quit
```$ docker -v```
# Print help message
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
# .bashrc
```export DOCKER_HOST=127.0.0.1:2375```
# Verify that Docker Engine is installed correctly by running the "hello-world" image
```$ docker run hello-world```
# Search the Docker Hub for images
```$ docker search imageName```
# What images do I have locally
```$ docker images```
# Show only ID of images
```$ docker images -q```
# List containers
```$ docker ps [-aq]```
# Delete container
```$ docker rm <id>/<name>```
# Delete local images
```$ docker rmi [-f] <id>/<name>```
# Delete all images
```$ docker rmi $(docker images -q)```
# Stop one or more running containers
```$ docker stop CONTAINER```
