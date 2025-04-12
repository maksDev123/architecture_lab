# Lab 3

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



Additional hyperparameters: `MAX_RETRIES = 3, RETRY_DELAY = 2`

After running got the following results: messages splitted amoung 2 message-services:
![Image 12 04 2025 at 18 55 (2)](https://github.com/user-attachments/assets/3d8750c4-7ae4-4fc5-b5ba-47259e233975)
![Image 12 04 2025 at 18 55 (1)](https://github.com/user-attachments/assets/1a4546a3-3937-45f1-9c79-c62878fb1762)

Get request to facade services chouses random message service and depicts saved messages:
![Image 12 04 2025 at 18 56](https://github.com/user-attachments/assets/a810e558-27ac-4675-b726-e3c1d75558a5)



Replication
1) Firstly I stoped message services to make messages save in queue.
2) Stopped main broker (`broker1`) with `docker stop broker1`. Logs of stopped broker:
![Image 12 04 2025 at 19 35](https://github.com/user-attachments/assets/e79318d9-3a54-4b35-b3b2-36ad9cfd4704)

3) Started message services and successfully read messages because of replication. Part of back-up logs (work of ReplicationFetcher):
![Image 12 04 2025 at 19 36](https://github.com/user-attachments/assets/72e21603-b46a-4856-b2b2-ce1395175f9f)

Thus replication works
