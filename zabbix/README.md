Развернул zabbix-agent через ansible. Ansible установил последнюю версию zabbix-agent'а:
```
Package: zabbix-agent
Version: 1:4.0.4+dfsg-1
```
Zabbix-server версии `Zabbix 3.4.1` не увидел агента и выдал такой лог:
```
Received empty response from Zabbix Agent at [ip addr]. Assuming that agent dropped connection because of access permissions
```
Zabbix-agent, в свою очередь, выдал:
```
6917:20200515:201814.388 Message from <ip addr> is missing header. Message ignored.
```
Выяснил, что новая версия агента не работает со старой версией сервера. Блин. [Тут](https://www.zabbix.com/ru/download_agents) скачал нужную версию агента.
> Установка: поставить новую версию, и заменить файлы из архива. 
> Ещё попросил скопировать файл из /etc/zabbix/zabbix_agentd.conf в /usr/local/etc/zabbix_agentd.conf.
> Рестарт сервиса
```
root@db2:~# zabbix_agentd -V
zabbix_agentd (daemon) (Zabbix) 3.0.31
```
#
