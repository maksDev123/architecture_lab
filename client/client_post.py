import requests
import json
from services import FACADE_SERVICE_URL

message = "Hello, this is a test message."

payload = {
    "message": message
}

headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(f"{FACADE_SERVICE_URL}/send_message", data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        print("Response from facade service:")
        print(response.text)
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"Error sending request to facade service: {e}")
