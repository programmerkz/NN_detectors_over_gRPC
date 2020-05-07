from .grpc_server import GrpcServer
from .detect_operation import DetectOperation
from .nn_service import NNService


class Container:

    def __init__(self):
        self.nnService = NNService ()
        self.detectOperation = DetectOperation (self)
        self.grpcServer = GrpcServer (self)
        print ("GrpcDetectorService created")

    def start (self):
        self.grpcServer.start()
        print ("Container started")
    
    def stop (self):
        self.grpcServer.stop ()
        print ("Container stopped")        
