###### Centos7 (client)
```
yum install nfs-utils
systemctl start rpcbind
systemctl enable rpcbind
mkdir /mnt/nfs-share
echo "172.16.16.254:/mnt/nfs /mnt/nfs-share nfs defaults 0 0" >> /etc/fstab
mount -a
```
