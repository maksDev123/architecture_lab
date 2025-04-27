# Lab 5

### How to run
Install dependencies:
```
pip3 install -r requirements.txt
```

Setup Kafka
```
docker-compose up -d
docker exec broker1 kafka-topics \
  --create \
  --bootstrap-server broker1:19092 \
  --replication-factor 3 \
  --partitions 2 \
  --topic my-topic-2partitions
```

Setup Consul:
```
docker pull consul
docker run \
    -d \
    -p 8500:8500 \
    -p 8600:8600/udp \
    --name=badger \
    consul agent -server -ui -node=server-1 -bootstrap-expect=1 -client=0.0.0.0

docker run \
   --name=discovery \
   consul agent -node=client-1 -retry-join=172.17.0.2
```

Run service (rest)
```
python3.12 -m rest.facade-service
python3.12 ./rest/logging-service.py --service_port 8081 --hazelcast_port 5701
python3.12 ./rest/logging-service.py --service_port 8083 --hazelcast_port 5702
python3.12 ./rest/logging-service.py --service_port 8084 --hazelcast_port 5703
python3.12 -m rest.messages-service
python3.12 -m rest.messages-service --port=8086
python3.12 -m rest.config-server
```


Run get and post request:
```
python3 -m client.client_post
python3 -m client.client_get
```


Additiona l hyperparameters: `MAX_RETRIES = 3, RETRY_DELAY = 2`



After starting services c