###### Create template CentOS7
```
yum update -y
rpm -q open-vm-tools # return the local version of the rpm files
or
yum list open-vm-tools # show the version in the repo

service rsyslog stop
service auditd stop
/bin/package-cleanup --oldkernels --count=1
/usr/bin/yum clean all

logrotate -f /etc/logrotate.conf
rm -f /var/log/*-???????? /var/log/*.gz
rm -f /var/log/dmesg.old
rm -rf /var/log/anaconda
cat /dev/null > /var/log/audit/audit.log
cat /dev/null > /var/log/wtmp
cat /dev/null > /var/log/lastlog
cat /dev/null > /var/log/grubby
rm -f /etc/ssh/*key*
rm -f ~root/.bash_history
unset HISTFILE
rm -rf ~root/.ssh/
history -c
sys-unconfig
```
###### ALL:
```
yum -y install epel-release centos-release-openshift-origin311
yum -y install origin origin-clients vim-enhanced atomic-openshift-utils NetworkManager python-rhsm-certificates
systemctl enable NetworkManager --now

vim /etc/resolve.conf
  search home.lab
  nameserver 172.16.16.16

vim /etc/NetworkManager/NetworkManager.conf
  [main]
  plugins=ifcfg-rh,ibft
  dns=none
systemctl restart NetworkManager
systemctl status NetworkManager
```
###### NODE:
```
yum -y install docker libcgroup-tools
lsblk
cat <<EOF > /etc/sysconfig/docker-storage-setup
DEVS=/dev/sdb
VG=docker-vg
EOF
docker-storage-setup
lsblk

systemctl enable docker.service --now
systemctl status docker

setsebool -P virt_use_nfs 1
setsebool -P virt_sandbox_use_nfs 1
```
###### MASTER:
```
yum -y install httpd-tools gcc python-devel python-pip
ssh-keygen
ssh-copy-id oc-i-1.home.lab
ssh-copy-id oc-n-1.home.lab
ssh-copy-id oc-n-2.home.lab
ssh-copy-id oc-m-1.home.lab

git clone https://github.com/openshift/openshift-ansible
cd openshift-ansible/
git checkout remotes/origin/release-3.11
check requirements.txt
pip -v install ansible==2.9.13

ansible-playbook -i /etc/ansible/hosts playbooks/prerequisites.yml
ansible-playbook -i /etc/ansible/hosts playbooks/deploy_cluster.yml
```
###### cat /etc/hosts
```
172.16.16.100   oc-m-1.home.lab oc-m-1
172.16.16.101   oc-n-1.home.lab oc-n-1
172.16.16.102   oc-n-2.home.lab oc-n-2
172.16.16.105   oc-i-1.home.lab oc-i-1
```
###### cat /etc/ansible/hosts
```
[OSEv3:children]
masters
nodes
etcd

[masters]
oc-m-1.home.lab

[etcd]
oc-m-1.home.lab

[nodes]
oc-m-1.home.lab openshift_ip=172.16.16.100 openshift_schedulable=true openshift_node_group_name='node-config-master'
oc-n-1.home.lab openshift_ip=172.16.16.101 openshift_schedulable=true openshift_node_group_name='node-config-compute'
oc-n-2.home.lab openshift_ip=172.16.16.102 openshift_schedulable=true openshift_node_group_name='node-config-compute'
oc-i-1.home.lab openshift_ip=172.16.16.105 openshift_schedulable=true openshift_node_group_name='node-config-infra'

[nodes:vars]
openshift_disable_check=disk_availability,memory_availability,docker_storage

[masters:vars]
openshift_disable_check=disk_availability,memory_availability,docker_storage

[OSEv3:vars]
debug_level=4
ansible_ssh_user=root
openshift_enable_service_catalog=true
ansible_service_broker_install=true

openshift_node_groups=[{'name': 'node-config-master', 'labels': ['node-role.kubernetes.io/master=true']}, {'name': 'node-config-infra', 'labels': ['node-role.kubernetes.io/infra=true']}, {'name': 'node-config-compute', 'labels': ['node-role.kubernetes.io/compute=true']}]

containerized=false
os_sdn_network_plugin_name='redhat/openshift-ovs-multitenant'
openshift_disable_check=disk_availability,docker_storage,memory_availability,docker_image_availability

deployment_type=origin
openshift_deployment_type=origin

openshift_release=v3.11.0
openshift_pkg_version=-3.11.0
openshift_image_tag=v3.11.0
openshift_service_catalog_image_version=v3.11.0
template_service_broker_image_version=v3.11
osm_use_cockpit=true

openshift_master_cluster_method=native
openshift_master_default_subdomain=apps.home.lab
openshift_public_hostname=oc-m-1.home.lab
```
###### Install oc cli
```
curl -L https://github.com/openshift/origin/releases/download/v3.11.0/openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz -o openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz

tar -xzf openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz

mv openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit openshift3.11

cd openshift3.11/
chmod u+x oc
chmod u+x kubectl
./oc version
sudo ln -s $(pwd)/oc /usr/bin/oc

oc login -u admin -p admin https://oc-m-1.home.lab:8443

arty@ntp:~/openshift3.11$ oc new-project python-hello-world --display-name='Python hello world app'
Now using project "python-hello-world" on server "https://oc-m-1.home.lab:8443".

You can add applications to this project with the 'new-app' command. For example, try:

    oc new-app centos/ruby-25-centos7~https://github.com/sclorg/ruby-ex.git

to build a new example application in Ruby.
arty@ntp:~/openshift3.11$ oc project
Using project "python-hello-world" on server "https://oc-m-1.home.lab:8443".
```
###### Build configs
A build config contains all the information needed to build an application using its source code. This includes all the information required to build the application container image:
 - URL for the application source code
 - Name of the builder image to use
 - Name of the application container image that’s created
 - Events that can trigger a new build to occur
 
The build config is used to track what’s required to build your application and to trigger the creation of the application’s container image.
After the build config does its job, it `triggers the deployment config` that’s created for your newly created application.

###### Deployment configs
The job of `deploying and upgrading the application` is handled by the deployment config component.
- Deployment configs track several pieces of information about an application:
- Currently deployed version of the application.
- Number of replicas to maintain for the application.
- Trigger events that can trigger a redeployment. By default, configuration
changes to the deployment or changes to the container image trigger an automatic application redeployment
- Upgrade strategy. app-cli uses the default rolling-upgrade strategy.
- Application deployments.

*A key feature of applications running in OpenShift is that they’re horizontally scalable. This concept is represented in the deployment config by the number of replicas.*

`The number of replicas specified in a deployment config is passed into a Kubernetes object called a replication controller. This is a special type of Kubernetes pod that allows
for multiple replicas—copies of the application pod—to be kept running at all times.`

*Each deployment for an application is monitored and available to the deployment config component using deployments.*

###### DEPLOYMENTS
Each time a new version of an application is created by its build config, a new deployment is created and tracked by the deployment config. A deployment represents a
unique version of an application. Each deployment references a version of the application image that was created, and creates the replication controller to create and
maintain the pods to serve the application.

###### MANAGING UPGRADE METHODS
The default application-upgrade method in OpenShift is to perform a `rolling upgrade`. Rolling upgrades create new versions of an application, allowing new connections to
the application to access only the new version. As traffic increases to the new deployment, the pods for the old deployment are removed from the system.
New application deployments can be automatically triggered by events such as configuration changes to your application, or a new version of a container image being
available. These sorts of trigger events are monitored by `image streams` in OpenShift.
###### Image streams
Image streams are used to automate actions in OpenShift. They consist of links to one
or more container images. Using image streams, you can monitor applications and
trigger new deployments when their components are updated.

*Each service gets an IP address that’s only routable from within the OpenShift cluster.*
###### Services
Services provide a consistent gateway into your application deployment. But the IP
address of a service is available only in your OpenShift cluster. To connect users to your
applications and make DNS work properly, you need one more application component.
Next, you’ll create a `route` to expose app-cli externally from your OpenShift cluster.
#### osm_cluster_network_cidr 
When you configure the installation inventory file
before deploying OpenShift, set the osm_cluster_network_cidr variable to the IP
address range you want to use for the pod network.
*Be careful when you select the IP range for the pod network—once you deploy OpenShift, it’s all but impossible to change it*

`A VXLAN is a protocol that acts as an overlay network between the nodes in your
OpenShift cluster. An overlay network is a software-defined network that’s deployed
on top of another network. The VXLANs used in OpenShift are deployed on top of the
networking configuration of the hosts. To communicate securely between pods, the VXLAN encapsulates pod network traffic
in an additional layer of network information so it can be delivered to the proper pod
on the proper server by IP address. The overlay network is the pod network in your
OpenShift cluster. The VXLAN interfaces on each node provide access to and from
that network.`

*A TUN interface (short for network TUNnel) is a virtual network device that mimics
the functionality of a physical interface. In the case of OpenShift, the tun0 interface
acts as the default gateway on each node for the pod network. Because it’s a virtual
device and not a physical one, it can be used to route traffic on and off the nonroutable pod network.*

```
[root@oc-n-1 ~]# ip a | egrep '^[0-9].*:' | awk '{ print $1 $2}'
1:lo:
2:ens192:
3:docker0:
4:ovs-system:
9:br0:
10:vxlan_sys_4789:
11:tun0:
18:vethd43cac2c@if3:
```
*To get network traffic in and out of the container, the eth0 interface in
the container is linked in the Linux kernel to a corresponding veth interface in the
host’s default network namespace.*
