from server_pb2_grpc import DetectorServicer


class GrpcDetectorService (DetectorServicer):

    def __init__(self, grpcServer):
        self.grpcServer = grpcServer
        print ("GrpcDetectorService created")


    def detect(self, request, context):
        return self.grpcServer.container.detectOperation.detect (request, context)
