## Install dependencies
```
apt-get install curl git mercurial make binutils bison gcc build-essential
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
