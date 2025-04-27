import grpc
from concurrent import futures
import messages_pb2
import messages_pb2_grpc

hash_table = {}

class LoggingService(messages_pb2_grpc.LoggingServiceServicer):

    def GetMessages(self, request, context):
        messages = list(hash_table.values())
        return messages_pb2.GetMessagesResponse(messages=messages)

    def SaveMessage(self, request, context):
        hash_table[request.uuid] = request.message
        return messages_pb2.SendMessageResponse(status =f"Message was saved")

if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    messages_pb2_grpc.add_LoggingServiceServicer_to_server(LoggingService(), server)
    server.add_insecure_port('[::]:8081')
    print("Server started on port 8081")
    server.start()
    server.wait_for_termination()

