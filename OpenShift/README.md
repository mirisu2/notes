
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







