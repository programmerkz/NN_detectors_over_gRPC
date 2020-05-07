from concurrent import futures

import grpc

import server_pb2_grpc
from .grpc_detector_service import GrpcDetectorService


class GrpcServer:
    PORT = "0.0.0.0:8081"
    MAX_RECEIVE_LEN = 2048 * 2048 * 3

    def __init__(self, container):
        self.container = container
        self.grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=[('grpc.max_receive_message_length', GrpcServer.MAX_RECEIVE_LEN)])
        server_pb2_grpc.add_DetectorServicer_to_server(GrpcDetectorService (self), self.grpcServer)
        self.grpcServer.add_insecure_port(GrpcServer.PORT)
        print ("GrpcServer created")

    def start (self):
        self.grpcServer.start()
        print ("GrpcServer started")
    
    def stop (self):
        self.grpcServer.stop (0)
        print ("GrpcServer stopped")        
