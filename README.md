# Lab 3

### How to run
Install dependencies:
```
pip3 install -r requirements.txt
```

Run service (rest)
```
python3.12 -m rest.facade-service
python3.12 ./rest/logging-service.py --service_port 8081 --hazelcast_port 5701
python3.12 ./rest/logging-service.py --service_port 8083 --hazelcast_port 5702
python3.12 ./rest/logging-service.py --service_port 8084 --hazelcast_port 5703
python3.12 -m rest.messages-service
python3.12 -m rest.config-server
```

Run get and post request:
```
python3 -m client.client_post
python3 -m client.client_get
```

Additional hyperparameters: `MAX_RETRIES = 3, RETRY_DELAY = 2`

