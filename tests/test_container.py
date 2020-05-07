import os
import unittest
import cv2
import numpy
import grpc


from src.container import Container
from server_pb2_grpc import DetectorStub
from server_pb2 import DetectRequest
from .image_reader import ImageReader


class ContainerTest(unittest.TestCase):

    def _numpy_array_to_grpc_request(self, numpy_image):
        # Note, that Width and Height dimensions ARE SWAPPED!!!
        grpc_req_options = DetectRequest.DetectRequestOptionsModel(width=numpy_image.shape[1], height=numpy_image.shape[0])
        grpc_req_content = numpy.ndarray.tobytes(numpy_image)
        grpc_request = DetectRequest(options = grpc_req_options, content = grpc_req_content)

        return grpc_request


    def setUp(self):
        self.container = Container ()
        self.container.start ()


    def tearDown(self):
        self.container.stop ()
        

    def test_detect_right_sample(self):
        with grpc.insecure_channel('127.0.0.1:8081', options=[('grpc.max_receive_message_length', 2048 * 2048 * 3)]) as channel:
            stub = DetectorStub(channel)

            self.image_reader = ImageReader(os.path.join('.', 'tests', 'images'))

            for i in range(0, self.image_reader.sample_number()):
                with self.subTest(sample_id=i):
                    numpy_image = self.image_reader.read_sample(i)
                    grpc_request = self._numpy_array_to_grpc_request(numpy_image)
                    detections = stub.detect(grpc_request)
                    
                    # Assert that at least one person has been detected
                    self.assertGreater(len(detections.boxes), 0)


    def test_detect_wrong_sample(self):
        with grpc.insecure_channel('127.0.0.1:8081', options=[('grpc.max_receive_message_length', 2048 * 2048 * 3)]) as channel:
            stub = DetectorStub(channel)

            self.image_reader = ImageReader(os.path.join('.', 'tests', 'images'), fname_prefix='wrong_sample_')

            for i in range(0, self.image_reader.sample_number()):
                with self.subTest(sample_id=i):
                    numpy_image = self.image_reader.read_sample(i)
                    grpc_request = self._numpy_array_to_grpc_request(numpy_image)
                    detections = stub.detect(grpc_request)
                    
                    # Assert that NO person has been detected
                    self.assertEqual(len(detections.boxes), 0)

