[link](https://developer.gnome.org/NetworkManager/stable/nm-settings-ifcfg-rh.html)  
cat /etc/sysconfig/network-scropts/ifcfg-ens192
```
# Allowed values: Ethernet, Wireless, InfiniBand, Bridge, Bond, Vlan, Team, TeamPort
TYPE="Ethernet"
HWADDR="00:50:56:01:a8:48"
MTU="1500"

# User friendly name for the connection profile.
NAME="ens192"
# Interface name of the device this profile is bound to.
DEVICE="ens192"

# List of DNS search domains.
DOMAIN="3cp0.ru"


# Уникальный идентификатор сетевого интерфейса. Его можно сгенерировать самостоятельно командой uuidgen.
# Строка из 32-х символов в формате 8-4-4-4-12.
UUID="826c390e-a74d-4b2b-9fc0-612aa89b7f52"

# make the connection available only to the users listed:
USERS="joe bob alice"

# none: No boot-time protocol is used.
# bootp: Use BOOTP (bootstrap protocol).
# dhcp: Use DHCP (Dynamic Host Configuration Protocol).
# Allowed values: none, dhcp (bootp), static, ibft, autoip, shared
BOOTPROTO="none"

# This interface is set as the default route for IPv4|IPv6 traffic.
# yes / no
DEFROUTE="yes"
IPV6_DEFROUTE="yes"

# If IPV6INIT=yes, the following parameters could also be set in this file:
# no: Disable IPv6 on this interface.
IPV6INIT="yes"
IPV6ADDR=IPv6 address
IPV6_DEFAULTGW=The default route through the specified gateway

# yes: This interface is activated at boot time.
# : This interface is not activated at boot time.
ONBOOT="yes"

# Если задать тут DNS сервера и включить PEERDNS=yes то /etc/resolv.conf будет перезаписан этими DNS
PEERDNS=yes
DNS1="192.168.90.1"
DNS1="192.168.90.2"

IPADDR1=1.1.1.2 
PREFIX1=16

IPADDR="192.168.51.3"
PREFIX="24"
OR
NETMASK="255.255.255.0"
GATEWAY="192.168.51.254"

# Отключение сетевого интерфейса, если IP-адрес (v4/6) имеет неверную конфигурацию
IPV4_FAILURE_FATAL="no"
IPV6_FAILURE_FATAL="no"

# Упрпвляется ли через NetworkManager
NM_CONTROLLED="yes"/"no"

# Разрешает или запрещает автоконфигурирование IPv6 с помощью протокола Neighbor Discovery
IPV6_AUTOCONF="yes"/"no"

# Configure IPv6 Stable Privacy addressing for SLAAC
IPV6_ADDR_GEN_MODE="stable-privacy"/"eui64"

# Configure IPv6 Privacy Extensions for SLAAC (RFC4941). Example: IPV6_PRIVACY=rfc3041 IPV6_PRIVACY_PREFER_PUBLIC_IP=yes 
# Allowed values: IPV6_PRIVACY: no, yes (rfc3041 or rfc4941); 
IPV6_PRIVACY="yes"/"no"
IPV6_PRIVACY_PREFER_PUBLIC_IP="yes"/"no"
```
vi /etc/sysconfig/network-scripts/ifcfg-ens192:1
```
DEVICE=ens192:1
BOOTPROTO=static
IPADDR=192.168.0.100
NETMASK=255.255.255.0
GATEWAY=192.168.0.1
DNS1=1.1.1.1
DNS2=8.8.8.8
ONBOOT=yes
```
wifi
```
ESSID="mywifi"
MODE=Managed
KEY_MGMT=WPA-PSK
TYPE=Wireless
BOOTPROTO=none
NAME=mywifi
ONBOOT=yes
IPADDR=192.168.10.100
NETMASK=255.255.255.0
GATEWAY=192.168.10.1
DNS1=192.168.1.1
DNS2=1.1.1.1
```
/etc/nsswitch.conf
```
...
hosts:      files dns myhostname
...
```
