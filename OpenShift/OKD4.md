## OKD4 instalation:
1. Open [url](https://cloud.redhat.com/openshift/install)
2. Select provider (I selected vmware this time)

- 2.1 Copy [openshift-installer](https://mirror.openshift.com/pub/openshift-v4/clients/ocp/latest/openshift-install-linux.tar.gz)
- 2.2 Untar and move to /usr/bin/
```
# wget https://mirror.openshift.com/pub/openshift-v4/clients/ocp/latest/openshift-install-linux.tar.gz
# tar -xzf openshift-install-linux.tar.gz
# mv openshift-install /usr/bin/
# rm openshift-install*
```
- 2.3 Check
```
$ openshift-install version
openshift-install 4.6.6
built from commit db0f93089a64c5fd459d226fc224a2584e8cfb7e
release image quay.io/openshift-release-dev/ocp-release@sha256:c7e8f18e8116356701bd23ae3a23fb9892dd5ea66c8300662ef30563d7104f39
```
3. Now some preparation
- 3.1 Download certs from vmware vcenter server
```
# wget --no-check-certificate https://vcenter.home.lab/certs/download.zip
# unzip download.zip
# mv certs/lin/* /usr/local/share/ca-certificates/
# cd /usr/local/share/ca-certificates/
```
> :exclamation: The result is a .certs folder that contains two types of files. Files with a number extension (.0, .1, and so on) are root certificates. Change the extension to .crt. Files with a extension that starts with an r (.r0,. r1, and so on) are CRL files associated with a certificate. Change the extension to .crl.
```
# mv e20e602b.0 e20e602b.crt
# mv e20e602b.r0 e20e602b.crl

# update-ca-certificates
Updating certificates in /etc/ssl/certs...
1 added, 0 removed; done.
Running hooks in /etc/ca-certificates/update.d...
done.
```
Ready!
4. It's time to install
```
# openshift-install create cluster
? Platform vsphere
? vCenter vcenter.home.lab
? Username administrator@vsphere.local
? Password [? for help] ************
INFO Connecting to vCenter vcenter.home.lab
INFO Defaulting to only available datacenter: Datacenter1
INFO Defaulting to only available cluster: Cluster1
INFO Defaulting to only available datastore: datastore1
INFO Defaulting to only available network: VM Network
? Virtual IP Address for API 172.16.16.141
? Virtual IP Address for Ingress 172.16.16.142
? Base Domain home.lab
? Cluster Name firtst
? Pull Secret [? for help] **************
INFO Obtaining RHCOS image file from 'https://releases-art-rhcos.svc.ci.openshift.org/art/storage/releases/rhcos-4.6/46.82.202010011740-0/x86_64/rhcos-46.82.202010011740-0-vmware.x86_64.ova?sha256=935164c1b85e603a5bea5c50960613a5c24fd43106948abab9213550efcbad95'
INFO Creating infrastructure resources...
...
```
