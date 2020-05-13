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
usermod -aG docker yourUserName

# Print version information and quit
docker -v

# .bashrc
```
export DOCKER_HOST=127.0.0.1:2375
```
