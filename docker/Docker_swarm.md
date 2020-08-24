## https://docs.docker.com/engine/swarm/
```
user@ne:~$ docker swarm init --advertise-addr 192.168.0.1
Swarm initialized: current node (izs4yqp39a6yepsfs0449z8zu) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-182fx6cut33614ots1d5bls8x5ktvslegea5u91dexi0ucvh3g-2ded6pr941ktuuaropgg0i4vj 192.168.0.1:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.


user@mnt:~$ docker swarm join --token SWMTKN-1-182fx6cut33614ots1d5bls8x5ktvslegea5u91dexi0ucvh3g-2ded6pr941ktuuaropgg0i4vj 192.168.0.1:2377
This node joined a swarm as a worker.
```

#### Listing nodes
```
user@ne:~$ docker node ls
ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS      ENGINE VERSION
jji479tk392qbqdyah1gv903j     io                  Ready               Active                                  19.03.8
o6vei6fn2889x2c4ew2el5b79     mnt                 Ready               Active                                  19.03.12
izs4yqp39a6yepsfs0449z8zu *   ne                  Ready               Active              Leader              19.03.12
```

#### Inspecting a node
```
docker node inspect [NODE_NAME]
```
#### Promoting a worker to a manager
```
docker node promote [NODE_NAME]
```
#### Demoting a manager to a worker
```
docker node demote [NODE_NAME]
```
#### Removing a node from the swarm 
```
docker node demote [NODE_NAME] #(выполняем на мастере) понизить manager до worker
docker node rm -f  [NODE_NAME] #(выполняем на мастере) удалить из swarm
docker swarm leave #(выполняем на удаленной машине) покинуть swarm
```
#### Вспоминаем токен
```
docker swarm join-token [worker|manager] #(выполняем на мастере)
```
