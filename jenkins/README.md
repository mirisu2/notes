## Java 8 distr:
https://www.oracle.com/java/technologies/javase-downloads.html

## Java 8 installation steps:
```
sudo mkdir -p /usr/lib/jvm
sudo tar -xf jdk-8u251-linux-x64.tar.gz -C /usr/lib/jvm

sudo update-alternatives --install /usr/bin/java java /usr/lib/jvm/jdk1.8.0_251/bin/java 1
sudo update-alternatives --install /usr/bin/javac javac /usr/lib/jvm/jdk1.8.0_251/bin/javac 1
sudo update-alternatives --install /usr/bin/javaws javaws /usr/lib/jvm/jdk1.8.0_251/bin/javaws 1

sudo update-alternatives --config java
sudo update-alternatives --config javac
sudo update-alternatives --config javaws
java -version
java version "1.8.0_251"
Java(TM) SE Runtime Environment (build 1.8.0_251-b08)
Java HotSpot(TM) 64-Bit Server VM (build 25.251-b08, mixed mode)
```
## Jenkins installation steps:
https://pkg.jenkins.io/debian-stable/
```
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -

sudo nano /etc/apt/sources.list
deb https://pkg.jenkins.io/debian-stable binary/

sudo apt-get update
sudo apt-get install jenkins
```
## Plugins
* Periodic Backup
* Ansible
* Locale
* Nexus Platform
* Green Balls

## Jenkins env (чтобы не указывать в cli -auth) .bashrc
```
export JENKINS_USER_ID=john
export JENKINS_API_TOKEN=q43v346vh3j3e55h6yu
```
- http://ip-addr:8080/pipeline-syntax/
- http://ip-addr:8080/env-vars.html/
- https://e.printstacktrace.blog/jenkins-pipeline-environment-variables-the-definitive-guide/
```
java -jar jenkins-cli.jar -s http://localhost:8080/ safe-restart
```
## pipeline
```
pipeline {
	agent {}
	*environment {
		TELEGRAM_ID      = credentials('TELEGRAM_ID')
        	X_NOTIFY_API_Key = credentials('X_NOTIFY_API_Key')
	}
	*tools {
		maven 'apache-maven-3.0.1'
	}
	*options {
		timestamps()
		timeout(time: 1, unit: 'HOURS')
		disableConcurrentBuilds()
		buildDiscarder(logRotator(numToKeepStr: ''))
	}
	*triggers {
		cron('H */4 * * 1-5')
		pollSCM('H */4 * * 1-5')
	}
	*parameters {}
	*libraries {}
	stages {
		stage('Build...') {
			*when {
				expression { BRANCH_NAME ==~ /(production|staging)/ }
				environment name: 'DEPLOY_TO', value: 'production'
				allOf {
				    branch 'production'
				    environment name: 'DEPLOY_TO', value: 'production'
				}
				anyOf {
				    environment name: 'DEPLOY_TO', value: 'production'
				    environment name: 'DEPLOY_TO', value: 'staging'
				}				
			}
			*agent {}
			*environment {}
			*tools {}
			steps {
				DSL statements
			}
			*post {}
		}
		...
		stage {}
	}
	*post {}
}
```
