import requests
from services import FACADE_SERVICE_URL

try:
    response = requests.get(f"{FACADE_SERVICE_URL}/get_messages")
    if response.status_code == 200:
        print("Response from facade service:")
        print(response.text)
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"Error sending request to facade service: {e}")