from flask import Flask

app = Flask(__name__)

@app.route("/message-service")
def message_service():
    return "not implemented yet"


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 8082)
