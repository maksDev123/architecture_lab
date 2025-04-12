import requests
from services import MESSAGES_SERVICE_URLS

try:
    for service in MESSAGES_SERVICE_URLS:
        response = requests.get(f"{service}/get_messages")
        if response.status_code == 200:
            print("Response from facade service:")
            print(response.text)
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
            print(response.text)

except requests.exceptions.RequestException as e:
    print(f"Error sending request to facade service: {e}")