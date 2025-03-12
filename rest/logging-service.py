from flask import Flask, request
import hazelcast
import argparse

app = Flask(__name__)

my_map = None
client = None


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
    parser.add_argument("--hazelcast_host", type=str, default="127.0.0.1", help="Host of Hazelcast.")
    parser.add_argument("--hazelcast_port", type=str, default="5701", help="Port of Hazelcast.")

    args = parser.parse_args()

    client = hazelcast.HazelcastClient(
        cluster_members=[f"{args.hazelcast_host}:{args.hazelcast_port}"]
    )

    my_map = client.get_map("my-distributed-map3").blocking()

    app.run(debug = True, port = args.service_port)