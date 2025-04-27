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

Install Consul:
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
Setup Consul
```
python3.12 -m setup_consul
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

<img width="852" alt="Screenshot 2025-04-27 at 14 32 51" src="https://github.com/user-attachments/assets/2283aa74-cf44-4b58-81ce-b0da074553e8" />
<img width="749" alt="Screenshot 2025-04-27 at 14 32 59" src="https://github.com/user-attachments/assets/1bfaf5a4-4d7a-40cd-b9ca-d56bbb7d8aad" />

Additiona l hyperparameters: `MAX_RETRIES = 3, RETRY_DELAY = 2`

After starting services all of the were working, well accepting at least one message each.
<img width="870" alt="Screenshot 2025-04-27 at 14 32 39" src="https://github.com/user-attachments/assets/b4959cc3-cb5e-42fb-b5df-53a099cfc9b3" />
<img width="1259" alt="Screenshot 2025-04-27 at 14 27 33" src="https://github.com/user-attachments/assets/5ca323b2-fb4f-49c3-a056-f4a513dd25db" />

When I shutted down 2 services all of the messages went to last one service. Allowing everything to work correctly even when some services are unexpected
<img width="1255" alt="Screenshot 2025-04-27 at 14 29 03" src="https://github.com/user-attachments/assets/303ebf5a-a5bd-4680-b030-a3b78dee27cd" />
<img width="839" alt="Screenshot 2025-04-27 at 14 29 59" src="https://github.com/user-attachments/assets/37dd1cdb-c5c2-44e4-9aa3-976d0ee4f318" />
<img width="796" alt="Screenshot 2025-04-27 at 14 30 12" src="https://github.com/user-attachments/assets/afaf6d73-a044-42bc-81da-6cda29f5e7bc" />
