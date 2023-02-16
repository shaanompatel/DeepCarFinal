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

class ObjectsProcessor(object):
    def __init__(self,
                 car=None,
                 speed_limit=40,
                 model='/home/pi/deepcar/pi/models/efficientdet-lite-vehicle_edgetpu.tflite',
                 labels='/home/pi/deepcar/pi/models/vehicle-labels.txt',
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
        self.current_time = 0

    
    def run_detector(self):
        cap = cv2.VideoCapture(0)
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
        objs = get_objects(self.interpreter, 0.8)[:3]
        cv2_im = self.append_objs_to_img(cv2_im, self.inference_size, objs, self.labels)
        #cv2.imshow('frame', cv2_im)
        
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
                    print("Detected Object Is Too Small: ", area_percent)

                cv2_im = cv2.rectangle(cv2_im, (x0, y0), (x1, y1), (0, 255, 0), 2)
                cv2_im = cv2.putText(cv2_im, label, (x0, y0+30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)
        else:
            self.control_car(100, "Clear")
            
        return cv2_im
    
    # Ambulance --> speed limit
    # Motorcycle -> person
    # Bus -> stop sign
    # Truck -> slow
    def control_car(self, confidence, label):
        print("INFO: Detected", label, "with", str(confidence) +"%", "Confidence")     
        if (time.time() - self.current_time > 3):
            if (label == "Bus"):
                if (time.time() - self.current_time > 8):
                    self.speed_limit = 0
                    self.current_time = time.time()
                else:
                    self.speed_limit = 40
                    print("Stop Sign Timer Not Finished")
            elif (label == "Truck"):
                if (time.time() - self.current_time > 10):
                    self.speed_limit = 20
                    self.current_time = time.time() 
                else:
                    self.speed_limit = 40
                    print("Slow Timer Not Finished")
            elif (label == "Motorcycle"):
                self.speed_limit = 0
            elif (label == "Ambulance"):
                self.speed_limit = 20
            elif (label == "Clear"):
                self.speed_limit = 40
            
            if (self.current_speed != self.speed_limit):
                print("Changing speed from", self.current_speed, "to", self.speed_limit)
                self.current_speed = self.speed_limit
                if self.car is not None:    
                    self.car.change_speed(self.current_speed)
                else:
                    print("Car does not exist")
        else:
            print("Waiting for stop sign")
               
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
        
        

    
