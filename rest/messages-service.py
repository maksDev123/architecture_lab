import argparse
import threading
import json
from flask import Flask, jsonify
from kafka import KafkaConsumer
from utils import register_service, get_dictionary_info_by_key

app = Flask(__name__)

messages = []
messages_lock = threading.Lock()

@app.route('/health')
def health():
    return 'running', 200


def consumer_function():
    kafka_info = get_dictionary_info_by_key('kafka')

    consumer = KafkaConsumer(
        'my-topic-2partitions',
        bootstrap_servers=[f"{kafka_info['host']}:{port}" for port in json.loads(kafka_info["ports"])],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-consumer-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for msg in consumer:
        with messages_lock:
            print(msg.value)
            messages.append(msg.value)

@app.route("/message-service")
def message_service():
    with messages_lock:
        return jsonify(messages)

def main():
    parser = argparse.ArgumentParser(description="Run Flask Kafka consumer app.")
    parser.add_argument("--port", type=int, default=8082, help="Flask server port")
    
    args = parser.parse_args()

    register_service("127.0.0.1", args.port, "messages-service")

    thread = threading.Thread(target=consumer_function, daemon=True)
    thread.start()

    app.run(debug=True, host="0.0.0.0", port=args.port)

if __name__ == "__main__":
    main()
