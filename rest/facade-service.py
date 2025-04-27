from flask import Flask, request, jsonify
import uuid
import requests
import time
import random
from kafka import KafkaProducer
import json
from utils import find_service, get_dictionary_info_by_key

app = Flask(__name__)

MAX_RETRIES = 3
RETRY_DELAY = 2


kafka_info = get_dictionary_info_by_key('kafka')

print(json.loads(kafka_info["ports"]))
print(type(json.loads(kafka_info["ports"])))
print(json.loads(kafka_info["ports"]))
print(kafka_info['host'])
producer = KafkaProducer(
    bootstrap_servers=[f"{kafka_info['host']}:{port}" for port in json.loads(kafka_info["ports"])],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def http_retry_call(func, *args, **kwargs):
    """
    Retries an HTTP call based on the MAX_RETRIES and RETRY_DELAY parameters.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt} failed: {e} - Retrying in {RETRY_DELAY}s...")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                raise


@app.route("/get_messages", methods=["GET"])
def get_messages():
    try:
        # Get available Logging Services IPs.
        services = find_service('logging-service')
        service = random.choice(services)
        address = f"http://{service['address']}:{service['port']}"
        response = http_retry_call(requests.get, f"{address}/get_messages")

        saved_messages = response.json()["messages"]
        if response.status_code != 200:
            return jsonify({"error": f"Failed to receive saved messages: {response.text}", "status_code": response.status_code}), 500

        # Get available Message Services IPs.
        # response = http_retry_call(requests.post, f"{CONFIG_SERVER_URL}/get-ip-adresses", json={"service": "messages-service"})
        # message_ips = response.json()["available_ips"]
        services = find_service('messages-service')
        service = random.choice(services)
        address = f"http://{service['address']}:{service['port']}"

        response = http_retry_call(requests.get, f"{address}/message-service")
        text = response.text

        if response.status_code != 200:
            return jsonify({"error": f"Failed to receive messages: {response.text}", "status_code": response.status_code}), 500

        return f"{saved_messages}: {text}", 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Logging service not available: {e}"}), 503


@app.route("/send_message", methods=["POST"])
def receive_message():
    data = request.get_json()
    if data and 'message' in data:
        message = data['message']

        unique_id = str(uuid.uuid4())

        message_data = {
            'uuid': unique_id,
            'message': message
        }

        try:
            producer.send('my-topic-2partitions', message_data)

            # response = http_retry_call(requests.post, f"{CONFIG_SERVER_URL}/get-ip-adresses", json={"service": "logging-service"})
            # loggin_ips = response.json()["available_ips"]
            services = find_service('logging-service')
            service = random.choice(services)
            address = f"http://{service['address']}:{service['port']}"


            response = http_retry_call(requests.post, f"{address}/message", json=message_data)
            
            if response.status_code == 200:
                return "Message was saved.", 200
            else:
                return jsonify({"error": "Failed to log message", "status_code": response.status_code}), 500

        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"Logging service not available: {e}"}), 503

    else:
        return "Message not provided or invalid data format", 400

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 8080)