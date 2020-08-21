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
$ docker top <CONTAINER>

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
* User-defined bridge networks are best when you need multiple containers to communicate on the same Docker host.
* Host networks are best when the network stack should not be isolated from the Docker host, but you want other aspects of the 
container to be isolated.
* Overlay networks are best when you need containers running on different Docker hosts to communicate, or when multiple 
applications work together using swarm services.
* Macvlan networks are best when you are migrating from a VM setup or need your containers to look like physical hosts on 
your network, each with a unique MAC address.
* Third-party network plugins allow you to integrate Docker with specialized network stacks.

>User-defined bridges provide automatic DNS resolution between containers. Containers on the default bridge network can only 
>access each other by IP addresses.
>User-defined bridges provide better isolation.
>Containers can be attached and detached from user-defined networks on the fly.

## Create a user-defined bridge network
```
$ docker network create my-net
$ docker network create --driver=bridge --subnet=10.15.0.0/24 --gateway=10.15.0.1 app1-net
```
## Command to remove a user-defined bridge network
> If containers are currently connected to the network, disconnect them first.
```
$ docker network rm my-net
```
## Connect a container to a user-defined bridge
```$ docker run -itd --network=my-net busybox```
## Specify the IP address a container will use on a given network
```$ docker network connect --ip 10.10.36.122 multi-host-network container2```
## To connect a running container to an existing user-defined bridge
```$ docker network connect my-net my-nginx```
## Disconnect a container from a user-defined bridge
```$ docker network disconnect my-net my-nginx```
## Inspect the bridge network to see what containers are connected to it
```
$ docker network inspect bridge
$ docker network inspect app1-net
```
## [IPv6](https://medium.com/@skleeschulte/how-to-enable-ipv6-for-docker-containers-on-ubuntu-18-04-c68394a219a2)
```
cat /etc/docker/daemon.json
{
  "ipv6": true,
  "fixed-cidr-v6": "fd00::/80",
  "userland-proxy": false
}
$ sudo ip6tables -t nat -A POSTROUTING -s fd00::/80 ! -o docker0 -j MASQUERADE
OR
$ docker run -d --restart=always -v /var/run/docker.sock:/var/run/docker.sock:ro --cap-drop=ALL \
--cap-add=NET_RAW --cap-add=NET_ADMIN --cap-add=SYS_MODULE --net=host --name ipv6nat robbertkl/ipv6nat
and test it
$ docker run --rm -t busybox ping6 -c 4 google.com
```
## Configure [logging](https://docs.docker.com/config/containers/logging/log_tags/) drivers
```
--log-opt mode=blocking (default)
--log-opt mode=non-blocking

--log-opt tag="mailer"

--log-driver none
```
https://docs.docker.com/config/containers/logging/local/
* none	-No logs are available for the container and docker logs does not return any output.
* local	-Logs are stored in a custom format designed for minimal overhead.
* json-file	-The logs are formatted as JSON. The default logging driver for Docker.
* syslog	-Writes logging messages to the syslog facility. The syslog daemon must be running on the host machine.
* journald	-Writes log messages to journald. The journald daemon must be running on the host machine.
* gelf	-Writes log messages to a Graylog Extended Log Format (GELF) endpoint such as Graylog or Logstash.
* fluentd	-Writes log messages to fluentd (forward input). The fluentd daemon must be running on the host machine.
* awslogs	-Writes log messages to Amazon CloudWatch Logs.
* splunk	-Writes log messages to splunk using the HTTP Event Collector.
* etwlogs	-Writes log messages as Event Tracing for Windows (ETW) events. Only available on Windows platforms.
* gcplogs	-Writes log messages to Google Cloud Platform (GCP) Logging.
* logentries	-Writes log messages to Rapid7 Logentries.

## Private Docker registry
```
curl https://dockerhub.mydomain.local/v2/_catalog
{"repositories":["blabla","php5.6-apache"]}
curl https://dockerhub.mydomain.local/v2/blabla
{"name":"blabla","tags":["v0.0.59","v0.11","v0.0.62","v0.0.64","latest","v0.0.63"]}

$ docker -H 127.0.0.1:2375 run -d -p 5000:5000 --restart=always -v /home/john:/var/lib/registry --name registry registry:2
$ docker -H 127.0.0.1:2375 tag my-php-apache-app:v5.6 localhost:5000/my-php-apache-app:v5.6
$ docker -H 127.0.0.1:2375 push localhost:5000/my-php-apache-app:v5.6
```
в итоге создается в /home/john/docker/registry/v2/repositories
```
docker -H 127.0.0.1:2375 images
REPOSITORY                         TAG                 IMAGE ID            CREATED             SIZE
my-php-apache-app                  v5.6                a7540f835cb7        2 weeks ago         672MB
localhost:5000/my-php-apache-app   v5.6                a7540f835cb7        2 weeks ago         672MB

$ docker -H 127.0.0.1:2375 run -d --rm -p 8085:80 --name my-php56-app localhost:5000/my-php-apache-app:v5.6
```
https://gadelkareem.com/2018/10/23/deploy-a-docker-registry-with-letsencrypt-certificates-on-ubuntu-18-04/
```
sudo apt-get install certbot
sudo certbot certonly --standalone --preferred-challenges http --non-interactive --staple-ocsp --agree-tos \
-m gde@to.tam -d dockerhub.mydomain.host

cd /etc/letsencrypt/live/dockerhub.mydomain.host
cp privkey.pem domain.key
cat cert.pem chain.pem > domain.crt
chmod 777 domain.*

$ mkdir auth
$ docker run --entrypoint htpasswd registry:2 -Bbn admin passw4rd > auth/htpasswd
  
$ mkdir /var/lib/registry

$ docker run -d -p 443:5000 --restart=always --name registry \
  -v /home/arty/auth:/auth -e "REGISTRY_AUTH=htpasswd" \
  -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
  -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd \
  -v /etc/letsencrypt/live/dockerhub.mydomain.host:/certs \
  -v /var/lib/registry:/var/lib/registry \
  -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt \
  -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
  registry:2

docker login dockerhub.mydomain.host

docker build -t mydomain.host/notify:v0.0.1 .
docker push mydomain.host/notify:v0.0.1
curl https://mydomain.host/v2/_catalog
```
## Retaining your container’s bash history
```
docker run -e HIST_FILE=/root/.bash_history -v=$HOME/.bash_history:/root/.bash_history -ti ubuntu /bin/bash
```
## Remote volume mounting using SSHFS
```
docker run -t -i --privileged debian /bin/bash
# when it’s started up, run from within the container to install SSHFS.
apt-get update && apt-get install sshfs
$ LOCALPATH=/path/to/local/directory
$ mkdir $LOCALPATH
$ sshfs user@host:/path/to/remote/directory $LOCALPATH
```
## Using [Portainer](https://www.portainer.io/documentation/) to manage your Docker daemon
```
docker run -d -p 9000:9000 -p 8000:8000 --name portainer --restart always -v portainer_data:/data portainer/portainer \
-H tcp://192.168.198.115:2375
```
## Save and load images
```
docker image save <IMAGE> > <FILE>.tar
docker image save <IMAGE> -o <FILE>.tar
docker image save <IMAGE> --output <FILE>.tar

docker image load < <FILE>.tar
docker image load -i <FILE>.tar
docker image load --input <FILE>.tar
```
## Auto-restarting
```
--restart
no
on-failure
always
unless-stopped #если контейнер остановить, то он не будет запущен после рестарта!
```
