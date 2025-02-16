from flask import Flask, request

app = Flask(__name__)

hash_table = {}

@app.route("/get_messages")
def get_messages():
    return {"messages": list(hash_table.values())}


@app.route("/message", methods=["POST"])
def save_message():
    data = request.get_json()

    if data and 'message' in data and "uuid" in data:
        if data["uuid"] not in hash_table:
            hash_table[data["uuid"]] = data["message"]
        else:
            return "Message already logged", 409

        return f"Saved: {data["message"]}", 200
    else:
        return "Message not provided or invalid data format", 400

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 8081)