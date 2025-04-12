import argparse
import threading
import json
from flask import Flask, jsonify
from kafka import KafkaConsumer

app = Flask(__name__)

messages = []
messages_lock = threading.Lock()

def consumer_function():
    consumer = KafkaConsumer(
        'my-topic-2partitions',
        bootstrap_servers=['localhost:9092', 'localhost:9093', 'localhost:9094'],
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

    thread = threading.Thread(target=consumer_function, daemon=True)
    thread.start()

    app.run(debug=True, host="0.0.0.0", port=args.port)

if __name__ == "__main__":
    main()
