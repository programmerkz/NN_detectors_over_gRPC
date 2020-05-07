import numpy

from server_pb2 import DetectResponse


class DetectOperation:

    def __init__(self, container):
        self.container = container


    def _decode_grpc_request_to_numpy(self, grpc_request):
        numpy_buffer = numpy.frombuffer(grpc_request.content, dtype=numpy.uint8)
        # Note that numpy dimensions Width and Height are SWAPPED!!!
        return numpy.reshape(numpy_buffer, (grpc_request.options.height, grpc_request.options.width, 3))
    

    def _encode_numpy_detections_to_grpc_response(self, numpy_detections, frame_width, frame_height, filter_class_id, filter_min_confidence):
        grpc_response = DetectResponse()

        for i in numpy.arange(0, numpy_detections.shape[2]):
            confidence = numpy_detections[0, 0, i, 2]
            class_id = int(numpy_detections[0, 0, i, 1])

            if class_id == filter_class_id and confidence > filter_min_confidence:
                box = numpy_detections[0, 0, i, 3:7] * numpy.array([frame_width, frame_height, frame_width, frame_height])
                (left, top, right, bottom) = box.astype("int")
                
                bbox = DetectResponse.DetectResponseBoxModel(top=top, left=left, bottom=bottom, right=right)
                grpc_response.boxes.append(bbox)

        return grpc_response


    def detect(self, grpc_request, grpc_context, min_confidence = 0.3):
        numpy_frame = self._decode_grpc_request_to_numpy(grpc_request)
        numpy_detections = self.container.nnService.detect (numpy_frame)
        grpc_response = self._encode_numpy_detections_to_grpc_response(numpy_detections = numpy_detections, 
                                                                        frame_width = grpc_request.options.width, 
                                                                        frame_height = grpc_request.options.height, 
                                                                        filter_class_id = 15, 
                                                                        filter_min_confidence = min_confidence)

        return grpc_response
