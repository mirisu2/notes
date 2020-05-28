# Logstash
#### Prerequisites
Java 8
#### Установка [Logstash](https://www.elastic.co/downloads/logstash-oss)
```
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
sudo apt-get install apt-transport-https
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
sudo apt-get update && sudo apt-get install logstash
sudo systemctl start logstash.service
```
#### config file
```
/etc/logstash/logstash.yml
```
#### параметры
```
node.name: ls-node-1
path.data: /var/lib/logstash
http.host: "127.0.0.1"
path.logs: /var/log/logstash
```
#### Working with [plugins](https://www.elastic.co/guide/en/logstash/current/working-with-plugins.html)
```
# /bin/logstash-plugin list
bash: /bin/logstash-plugin: No such file or directory
# cd /usr/share/logstash
root@elastic:/usr/share/logstash# bin/logstash-plugin list
logstash-codec-avro
logstash-codec-cef
logstash-codec-collectd
...

bin/logstash-plugin list 
bin/logstash-plugin list --verbose 
bin/logstash-plugin list '*namefragment*' 
bin/logstash-plugin list --group (input|filter|output) 
```
#### /etc/logstash/conf.d/
* 10-syslog-input.conf
```
input {
    syslog {
        host => "0.0.0.0"
        port => 5514
        locale => "en_US"
        syslog_field => "message"
        timezone => "Europe/Moscow"
        use_labels => true
        type => "syslog"
    }
}
```
* 50-filter.conf
```
filter {

    if [type] == "syslog" {
        if [program] == "sshd" {
            mutate {
                add_field => { "[@metadata][source]" => "sshd" }
            }
            grok {
                match => { "message" => "Accepted %{WORD:method} for %{WORD:UserName} from %{IP:FromHost}" }
            }
        }
    }

}
```
* 99-output.conf
```
output {

    if [@metadata][source] == "sshd" {
        elasticsearch {
            hosts => ["http://192.168.198.99:9200"]
            index => "syslog_sshd_%{+YYYY.MM.dd}"
        }
    }

}
```
> Теперь на нужном сервере в /etc/rsyslog.conf
```
auth,authpriv.*    @192.168.198.99:5514
```
