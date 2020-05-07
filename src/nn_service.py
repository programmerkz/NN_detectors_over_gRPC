import os
import cv2

class NNService:

    def __init__(self):
        nn_model_file = os.path.join('.', 'src', 'model', 'MobileNetSSD_deploy.caffemodel') 
        nn_proto_file = os.path.join('.', 'src', 'model', 'MobileNetSSD_deploy.prototxt.txt') 

        self.neural_network = cv2.dnn.readNetFromCaffe(nn_proto_file, nn_model_file)
        print ("NNService created")

    def detect (self, frame):
        print (f"NNService REQUEST PARAMS: frame {frame.shape}")
        frame = cv2.resize(frame, (300, 300))
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
        self.neural_network.setInput(blob)
        detections = self.neural_network.forward()
        print('NNService RESPONSE Success')
        return detections
