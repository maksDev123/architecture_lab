import grpc
import uuid
from flask import Flask, request, jsonify
import messages_pb2
import messages_pb2_grpc

app = Flask(__name__)

channel = grpc.insecure_channel('localhost:8081')
logging_stub = messages_pb2_grpc.LoggingServiceStub(channel)

channel1 = grpc.insecure_channel('localhost:8082')
message_stub = messages_pb2_grpc.MessageServiceStub(channel1)

@app.route("/get_messages", methods=["GET"])
def get_messages():
    try:
        response_logging = logging_stub.GetMessages(messages_pb2.GetMessagesRequest())
        
        response_message = message_stub.GetMessage(messages_pb2.MessagesServiceRequest())

        return f"{str(list(response_logging.messages))}: {response_message.response}" , 200
    except grpc.RpcError as e:
        return jsonify({"error": f"Error fetching messages: {str(e)}"}), 500

@app.route("/send_message", methods=["POST"])
def receive_message():
    data = request.get_json()
    if data and 'message' in data:
        request_message = messages_pb2.SendMessageRequest(uuid = str(uuid.uuid4()), message = data['message'])
        try:
            response = logging_stub.SaveMessage(request_message)
            return response.status, 200
        except grpc.RpcError as e:
            return jsonify({"error": f"Error saving message: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid data format or message not provided"}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
