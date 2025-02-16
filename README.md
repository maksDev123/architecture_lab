# Lab 1

### How to run
Install dependencies:
```
pip3 install -r requirements.txt
```

Run service (rest)
```
python3 -m rest.facade-service
python3 -m rest.logging-service
python3 -m rest.messages-service
```

Run service (gRPC)
```
cd grpc
python3 ./facade-service
python3 ./logging-service
python3 ./messages-service
```


Run get and post request:
```
python3 -m client.client_post
python3 -m client.client_get
```

Additional hyperparameters: `MAX_RETRIES = 3, RETRY_DELAY = 2`

### Additional tasks
Implemented 2 additional tasks: retries and gRPC.
