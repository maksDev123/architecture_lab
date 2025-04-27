from flask import Flask, request
from services import LOGGING_SERVICE_URLS, MESSAGES_SERVICE_URLS

app = Flask(__name__)

@app.route("/get-ip-adresses", methods = ["POST"])
def message_service():
    data = request.get_json()
    service = data["service"]
    if service == "messages-service":
        return {"available_ips": MESSAGES_SERVICE_URLS}, 200
    elif service == "logging-service":
        return {"available_ips": LOGGING_SERVICE_URLS}, 200

    return "Unknown service"


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 8085)
