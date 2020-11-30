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
