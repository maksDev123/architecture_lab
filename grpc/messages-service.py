import grpc
from concurrent import futures
import messages_pb2
import messages_pb2_grpc


class MessageService(messages_pb2_grpc.MessageServiceServicer):

    def GetMessage(self, request, context):
        return messages_pb2.MessagesServiceResponse(response = "not implemented yet.")


if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    messages_pb2_grpc.add_MessageServiceServicer_to_server(MessageService(), server)
    server.add_insecure_port('[::]:8082')
    print("Server started on port 8082")
    server.start()
    server.wait_for_termination()
