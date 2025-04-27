from flask import Flask, request
import hazelcast
import argparse
import consul
from utils import find_service, register_service, get_dictionary_info_by_key

app = Flask(__name__)

my_map = None
client = None

@app.route('/health')
def health():
    return 'running', 200


@app.route("/get_messages")
def get_messages():
    return {"messages": list(my_map.values())}


@app.route("/message", methods=["POST"])
def save_message():

    print("Sending message")
    data = request.get_json()

    if data and 'message' in data and "uuid" in data:
        uuid = data["uuid"]
        message = data["message"]
        print(f"Received message: {message}")
        my_map.put(uuid, message)
        return "Saved message", 200
    else:
        return "Message not provided or invalid data format", 400


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Logging service")
    parser.add_argument("--service_port", type=str, default="8081", help="Port of Microservice.")
    serices = find_service("hazelcast")
    args = parser.parse_args()

    register_service("127.0.0.1", args.service_port, "logging-service")

    hazelcast_info = get_dictionary_info_by_key("hazelcast")

    client = hazelcast.HazelcastClient(
        cluster_name = hazelcast_info.get("cluster_name")
    )

    my_map = client.get_map("my-distributed-map3").blocking()

    app.run(debug = True, host="0.0.0.0", port = args.service_port)