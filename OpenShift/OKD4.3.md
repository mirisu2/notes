[READ THIS](https://docs.openshift.com/container-platform/4.3/installing/installing_vsphere/installing-vsphere.html#installation-requirements-user-infra_installing-vsphere)
## Pre-Requisites
```
apt-get install curl git mercurial make binutils bison gcc build-essential software-properties-common jq
```
## Install go version manager (gvm)
```
bash < <(curl -s -S -L https://raw.githubusercontent.com/moovweb/gvm/master/binscripts/gvm-installer)
```
## Check
```
gvm version
Go Version Manager v1.0.22 installed at /root/.gvm
gvm list
gvm listall
gvm install go1.15.6
gvm use go1.15.6

mkdir $HOME/go
export GOPATH=/home/john/go
```
## GIT
> Clone this repository to `src/github.com/openshift/installer` in your [GOPATH](https://golang.org/cmd/go/#hdr-GOPATH_environment_variable).

```
mkdir -p $GOPATH/src/github.com/openshift
cd $GOPATH/src/github.com/openshift

git clone https://github.com/openshift/installer.git
git branch -a
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/cherry-pick-3159-to-release-4.4
  remotes/origin/cherry-pick-3780-to-release-4.2
  remotes/origin/fcos
  remotes/origin/jim-minter-patch-1
  remotes/origin/master
  remotes/origin/master-4.1
  remotes/origin/master-fcos
  remotes/origin/release-4.0
  remotes/origin/release-4.1
  remotes/origin/release-4.2
  remotes/origin/release-4.3
  remotes/origin/release-4.4
  remotes/origin/release-4.5
  remotes/origin/release-4.6
  remotes/origin/release-4.7
  remotes/origin/release-4.8
  remotes/origin/shared-aws-untagging
  remotes/origin/vsphere
  remotes/origin/vsphere_hostname_resolution

git checkout remotes/origin/release-4.3
```
## Build installer
```
hack/./build.sh
```
## Result
```
pwd
/home/john/go/src/github.com/openshift/installer/bin
ls
openshift-install
sudo cp openshift-install /usr/bin

openshift-install version
openshift-install unreleased-master-2337-g4ce88ba4dc8626056df4525c7e5acbbd83a94c1c
built from commit 4ce88ba4dc8626056df4525c7e5acbbd83a94c1c
release image registry.svc.ci.openshift.org/origin/release:4.3
```
## Install [terraform](https://www.terraform.io/docs/cli/install/apt.html)
```
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=$(dpkg --print-architecture)] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt update
sudo apt install terraform
terraform version
Terraform v0.14.0
```
## Build a Cluster
1. Create an install-config.yaml. The machine CIDR for the dev cluster is 139.178.89.192/26.
```
apiVersion: v1
baseDomain: home.lab
metadata:
  name: co
networking:
  machineNetwork:
  - cidr: "139.178.89.192/26"
platform:
  vsphere:
    vCenter: vcenter.home.lab
    username: administrator@vsphere.local
    password: YOUR_VSPHERE_PASSWORD
    datacenter: Datacenter1
    defaultDatastore: datastore1
pullSecret: YOUR_PULL_SECRET
sshKey: YOUR_SSH_KEY
```
> :warning: перед запуском следующей команды, сделайте бэкап install-config.yaml файла. он удалится!
2. Run `openshift-install create ignition-configs`
> создается несколько файлов. надо [взять](https://github.com/openshift/okd/blob/master/Guides/UPI/vSphere_terraform/terraform.tfvars.example) **terraform.tfvars.example** и заполнить его
```
// ID identifying the cluster to create. Use your username so that resources created can be tracked back to you.
cluster_id = "example-cluster"

// Domain of the cluster. This should be "${cluster_id}.${base_domain}".
cluster_domain = "example-cluster.devcluster.openshift.com"

// Base domain from which the cluster domain is a subdomain.
base_domain = "devcluster.openshift.com"

// Name of the vSphere server. The dev cluster is on "vcsa.vmware.devcluster.openshift.com".
vsphere_server = "vcsa.vmware.devcluster.openshift.com"

// User on the vSphere server.
vsphere_user = "YOUR_USER"

// Password of the user on the vSphere server.
vsphere_password = "YOUR_PASSWORD"

// Name of the vSphere cluster. The dev cluster is "devel".
vsphere_cluster = "devel"

// Name of the vSphere data center. The dev cluster is "dc1".
vsphere_datacenter = "dc1"

// Name of the vSphere data store to use for the VMs. The dev cluster uses "nvme-ds1".
vsphere_datastore = "nvme-ds1"

// Name of the VM template to clone to create VMs for the cluster. The dev cluster has a template named "rhcos-latest".
vm_template = "rhcos-latest"

// his is the name of the publicly accessible network for cluster ingress and access.
vm_network = "VM Network"

// The number of control plane VMs to create. Default is 3.
control_plane_count = 3

// The number of compute VMs to create. Default is 3.
compute_count = 3

// Ignition config for the bootstrap machine. You should change the source, based on your environment.
bootstrap_ignition = <<END_OF_BOOTSTRAP_IGNITION
{"ignition":{"config":{"merge":[{"source":"http://10.20.15.2:80/ignition/bootstrap.ign","verification":{}}],"replace":{"source":null,"verification":{}}},"security":{"tls":{}},"timeouts":{},"version":"3.0.0"},"passwd":{},"storage":{},"systemd":{}}
END_OF_BOOTSTRAP_IGNITION

// Ignition config for the control plane machines. You should copy the contents of the master.ign generated by the installer.
control_plane_ignition = <<END_OF_MASTER_IGNITION
Copy the master ignition generated by the installer here.
END_OF_MASTER_IGNITION

// Ignition config for the compute machines. You should copy the contents of the worker.ign generated by the installer.
compute_ignition = <<END_OF_WORKER_IGNITION
Copy the worker ignition generated by the installer here.
END_OF_WORKER_IGNITION


// Set bootstrap_mac, control_plane_macs, and compute_macs

// The MAC address to assign to the bootstrap VM.
bootstrap_mac = "00:1c:14:00:00:03"

// The MAC addresses to assign to the control plane VMs. The length of this list
// must match the value of control_plane_count.
control_plane_macs = ["00:1c:14:00:00:11", "00:1c:14:00:00:12", "00:1c:14:00:00:13"]

// The MAC addresses to assign to the compute VMs. The length of this list must
// match the value of compute_count.
compute_macs = ["00:1c:14:00:00:41", "00:1c:14:00:00:42", "00:1c:14:00:00:43"]
```
> установил nginx, создал папку **ignition** в **/var/www/html/** и положил туда созданный файл **bootstrap.ign**

#### Required machines
The smallest OpenShift Container Platform clusters require the following hosts:
- One temporary bootstrap machine
- Three control plane, or master, machines
- At least two compute machines, which are also known as worker machines
