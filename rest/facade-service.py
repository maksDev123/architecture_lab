from flask import Flask, request, jsonify
import uuid
import requests
from services import LOGGING_SERVICE_URL, MESSAGES_SERVICE_URL
import time

app = Flask(__name__)

MAX_RETRIES = 3
RETRY_DELAY = 2

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
        response = http_retry_call(requests.get, f"{LOGGING_SERVICE_URL}/get_messages")
        saved_messages = response.json()["messages"]
        if response.status_code != 200:
            return jsonify({"error": f"Failed to receive saved messages: {response.text}", "status_code": response.status_code}), 500

        response = http_retry_call(requests.get, f"{MESSAGES_SERVICE_URL}/message-service")
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
            response = http_retry_call(requests.post, f"{LOGGING_SERVICE_URL}/message", json=message_data)
            
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