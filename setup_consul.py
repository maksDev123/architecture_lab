import consul
import json

KAFKA_PORTS = [9092, 9093, 9094]
HAZELCAST_PORTS = [5701, 5702, 5703]
LOCALHOST = "127.0.0.1"


consul_client = consul.Consul()
consul_client.kv.put('kafka', json.dumps({"ports": json.dumps(KAFKA_PORTS), "host": LOCALHOST}))
consul_client.kv.put('hazelcast', json.dumps({"ports": json.dumps(HAZELCAST_PORTS), "host": LOCALHOST, "cluster_name": "dev"}))