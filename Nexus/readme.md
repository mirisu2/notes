## [Repository Manager 3](https://help.sonatype.com/repomanager3)
**File Handle Limits**
```
To set the maximum number of open files for both soft and hard limits for the nexus user to 65536
vim /etc/security/limits.conf
nexus - nofile 65536
```
*Ubuntu **ignores** the /etc/security/limits.conf file for processes started by init.d.
So if NXRM is started using init.d there, edit /etc/pam.d/common-session and uncomment the following line ( remove the hash # and space at the beginning of the line)*
```
# session    required   pam_limits.so
```
*If you're using systemd to launch the server the above won't work. Instead, modify the configuration file to add a **LimitNOFILE** line:*
```
[Unit]
Description=nexus service
After=network.target

[Service]
Type=forking
LimitNOFILE=65536
ExecStart=/opt/nexus/bin/nexus start
ExecStop=/opt/nexus/bin/nexus stop
User=nexus
Restart=on-abort

[Install]
WantedBy=multi-user.target
```
*Docker*
```
--ulimit nofile=65536:65536
```
*Nexus Repository Manager **requires** a Java 8 Runtime Environment (JRE).*
```
Additionally, we strongly recommend to avoid using NFS, Amazon EFS, CIFS and SMB for anything other than blob storage 
in Nexus Repository 3, especially in large installations and high availability setups, as this can cause severe performance 
degradation. If NFS is used for blob storage we recommend to only use NFSv4; NFSv3 is known to provide inadequate performance. 
```
*The downloaded GZip’d TAR archive can be extracted with the command tar xvzf. For production it is not recommend that nexus be run from a users
home directory, a common practice is to use /opt. Running the appTo start the repository manager from application directory in the bin folder 
on a Unix-like platform like Linux use:*
```
./nexus run
```
### [Run as a Service](https://help.sonatype.com/repomanager3/installation/run-as-a-service)
### [Configuring the Runtime Environment](https://help.sonatype.com/repomanager3/installation/configuring-the-runtime-environment)
### Accessing the User Interface
```
http://localhost:8081/
```
## Get Maven
```
# Downloading Apache Maven
https://maven.apache.org/download.cgi

# Installing Apache Maven
https://maven.apache.org/install.html

# Add link
sudo ln -s /home/vagrant/apache-maven-3.6.3/bin/mvn /usr/bin/mvn

# Confirm 
mvn -v
```
`Much like a production environment and a staging environment, we recommend using the release repository for stable components in production and a snapshot repository for components still in the development phase.`

```
maven-central	proxy
maven-public	group
maven-releases	hosted
maven-snapshots	hosted
```
```
A repository group is:

- Its own access point, separate from proxy and hosted repositories.
- Created by adding repositories as members of a ordered list.
- A combined repository of locally published and remotely cached components.
- A unique endpoint that users can access without having to retrieve components from hosted and proxy repositories.
```
```
Repository groups become necessary if your organization has multiple teams working on multiple projects. 
If you’re an administrator you’ll find it less cumbersome to order your proxy and hosted repositories into a group 
designed for a development team.
```
*It’s **important** to note that a group doesn’t store components. You can’t publish or deploy components directly to this repository type. Groups just aggregate content from other repositories. If you want to modify components in a group repository, publish those changes to a hosted repository included in the group.*
