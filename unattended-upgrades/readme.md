### install packages what we need
```
apt-get install unattended-upgrades mailutils ssmtp
```

#### /etc/apt/apt.conf.d/50unattended-upgrades
```
Unattended-Upgrade::Origins-Pattern {
  "origin=Debian,codename=${distro_codename},label=Debian-Security";
};

Unattended-Upgrade::Package-Blacklist {
};

Unattended-Upgrade::Mail "receiver@mydomain.ru";
Unattended-Upgrade::Automatic-Reboot "true";
Unattended-Upgrade::Automatic-Reboot-WithUsers "false";
Unattended-Upgrade::Automatic-Reboot-Time "02:00";
Acquire::http::Dl-Limit "100";
Unattended-Upgrade::SyslogEnable "true";
Unattended-Upgrade::SyslogFacility "daemon";
```

### check
```
unattended-upgrade -v -d --dry-run
```

#### /etc/ssmtp/ssmtp.conf
```
Root=no-reply@mydomain.ru
mailhub=relay.mydomain.ru:587
hostname=host.mydomain.ru
AuthUser=no-reply@mydomain.ru
AuthPass=yhpL11U8r2
UseTLS=YES
UseSTARTTLS=YES
FromLineOverride=YES
```

### test it
```
echo "Test" | mail -s "Test" receiver@mydomain.ru
```
