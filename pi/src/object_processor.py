import argparse
import cv2
import os
import logging
import time

from pycoral.adapters.common import input_size
from pycoral.adapters.detect import get_objects
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.edgetpu import run_inference

SHOW_IMAGE = True

class ObjectsProcessor(object):
    def __init__(self,
                 car=None,
                 speed_limit=40,
                 model='/home/pi/deepcar/pi/models/efficientdet-lite-road_edgetpu.tflite',
                 labels='/home/pi/deepcar/pi/models/road-labels.txt',
                 ):
        
        self.interpreter = make_interpreter(model)
        self.interpreter.allocate_tensors()
        self.labels = read_label_file(labels)
        self.inference_size = input_size(self.interpreter)
        
        logging.info('Initializing Edge TPU with model %s...' % model)

        self.car = car
        self.speed_limit = speed_limit
        self.speed = speed_limit
        self.current_speed = 40
        self.stop_time = 0
        self.slow_time = 0
        self.limit_time = 0
        self.pacer = 0
        cv2.namedWindow("detector2", cv2.WINDOW_NORMAL)

    
    def run_detector(self):
        cap = cv2.VideoCapture(2)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2_im = frame            
            self.process_frame(cv2_im)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        
    def process_frame(self, cv2_im):
        cv2_im_rgb = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
        cv2_im_rgb = cv2.resize(cv2_im_rgb, self.inference_size)
        run_inference(self.interpreter, cv2_im_rgb.tobytes())
        objs = get_objects(self.interpreter, 0.6)[:3]
        cv2_im = self.append_objs_to_img(cv2_im, self.inference_size, objs, self.labels)
        if SHOW_IMAGE:
            cv2.imshow('detector2', cv2_im)
        
    def append_objs_to_img(self, cv2_im, inference_size, objs, labels):
        height, width, channels = cv2_im.shape
        scale_x, scale_y = width / inference_size[0], height / inference_size[1]
        if (len(objs) > 0):
            for obj in objs:
                bbox = obj.bbox.scale(scale_x, scale_y)
                x0, y0 = int(bbox.xmin), int(bbox.ymin)
                x1, y1 = int(bbox.xmax), int(bbox.ymax)
                
                area_percent = ((x1-x0) * (y1-y0))/(height*width)

                percent = int(100 * obj.score)
                label = '{}% {}'.format(percent, labels.get(obj.id, obj.id))
                
                if (area_percent > 0.10):
                    self.control_car(percent, labels.get(obj.id, obj.id))
                else:
                    print("INFO: Detected Object Is Too Small: ", area_percent)

                cv2_im = cv2.rectangle(cv2_im, (x0, y0), (x1, y1), (0, 255, 0), 2)
                cv2_im = cv2.putText(cv2_im, label, (x0, y0+30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)
        else:
            self.control_car(100, "clear")
            
        return cv2_im
    
    # Ambulance --> speed limit
    # Motorcycle -> person
    # Bus -> stop sign
    # Truck -> slow
    def control_car(self, confidence, label):
        print("INFO: Detected", label, "with", str(confidence) +"%", "Confidence")     
        if (time.time() - self.pacer > 1):
            if (label == "stop"):
                if (time.time() - self.stop_time > 8):
                    self.speed_limit = 0
                    self.stop_time = time.time()
                elif (time.time() - self.stop_time > 4):
                    print("INFO: No Longer Waiting at Stop Sign")
                    self.speed_limit = 40
                else:
                    print("INFO: Detected Stop Sign Too Recently")
            elif (label == "slow"):
                if (time.time() - self.slow_time > 8):
                    self.speed_limit = 20
                    self.slow_time = time.time()
                elif (time.time() - self.slow_time > 4):
                    print("INFO: No Longer Driving Slow")
                    self.speed_limit = 40
                else:
                    print("INFO: Detected Slow Too Recently")
            elif (label == "speed limit"):
                if (time.time() - self.limit_time > 8):
                    self.speed_limit = 20
                    self.limit_time = time.time()
                elif (time.time() - self.limit_time > 4):
                    print("INFO: No Longer Driving Slow")
                    self.speed_limit = 40
                else:
                    print("INFO: Detected Speed Limit Too Recently")
            elif (label == "person"):
                self.speed_limit = 0
            elif (label == "clear"):
                self.speed_limit = 40
            
            if (self.current_speed != self.speed_limit):
                print("INFO: Changing Speed From", self.current_speed, "to", self.speed_limit)
                self.current_speed = self.speed_limit
                if self.car is not None:    
                    self.car.change_speed(self.current_speed)
                else:
                    print("DEBUG: Car Does Not Exist")
            self.pacer = time.time()
        else:
            print("INFO: Timer Not Done, Ignoring Detection")
    
               
    def __enter__(self):
        """ Entering a with statement """
        return self

    def __exit__(self, _type, value, traceback):
        """ Exit a with statement"""
        if traceback is not None:
            # Exception occurred:
            logging.error('Exiting with statement with exception %s' % traceback)

if __name__ == '__main__':
    with ObjectsProcessor() as processor:
        processor.run_detector()
        
        

    
