import logging
#import picar
import cv2
import datetime
#import RPi.GPIO as GPIO
import pigpio
import time
import readchar
from end_to_end_lane_follower import EndToEndLaneFollower
from hand_coded_lane_follower import HandCodedLaneFollower
from object_processor import ObjectsProcessor
#from objects_on_road_processor import ObjectsOnRoadProcessor
from servo import servo_motor
from sabertooth import motor
s = servo_motor()
m = motor()

_SHOW_IMAGE = True

class DeepPiCar(object):

    __INITIAL_SPEED = 0
    __SCREEN_WIDTH = 320
    __SCREEN_HEIGHT = 240
    #self.car_speed = 40

    def __init__(self):
        """ Init camera and wheels"""
        logging.info('Creating a DeepPiCar...')

       

        logging.debug('Set up camera')
        self.camera = cv2.VideoCapture(0)
        self.camera.set(3, self.__SCREEN_WIDTH)
        self.camera.set(4, self.__SCREEN_HEIGHT)
        self.cap = cv2.VideoCapture(2)
        self.cap.set(3, self.__SCREEN_WIDTH/1.5)
        self.cap.set(4, self.__SCREEN_HEIGHT/1.5)
        

        logging.debug('Set up back wheels')
       

        logging.debug('Set up front wheels')
        s.spin(90)  # Steering Range is 0 (left) - 90 (center) - 180 (right)

        #self.lane_follower = HandCodedLaneFollower(self)
        #self.traffic_sign_processor = ObjectsOnRoadProcessor(self)
        self.object_detector = ObjectsProcessor(self)
        self.lane_follower = EndToEndLaneFollower(self)

        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        datestr = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        self.video_orig = self.create_video_recorder('../data/tmp/car_video%s.avi' % datestr)
        self.video_lane = self.create_video_recorder('../data/tmp/car_video_lane%s.avi' % datestr)
        self.video_objs = self.create_video_recorder('../data/tmp/car_video_objs%s.avi' % datestr)

        logging.info('Created a DeepCar Instance')

    def create_video_recorder(self, path):
        return cv2.VideoWriter(path, self.fourcc, 20.0, (self.__SCREEN_WIDTH, self.__SCREEN_HEIGHT))

    def __enter__(self):
        """ Entering a with statement """
        return self

    def __exit__(self, _type, value, traceback):
        """ Exit a with statement"""
        if traceback is not None:
            # Exception occurred:
            logging.error('Exiting with statement with exception %s' % traceback)

        self.cleanup()

    def cleanup(self):
        """ Reset the hardware"""
        logging.info('Stopping the car, resetting hardware.')
        m.cleanup()
        s.spin(90)
        self.camera.release()
        self.video_orig.release()
        self.video_lane.release()
        self.video_objs.release()
        cv2.destroyAllWindows()
    
    def change_speed(self, speed):
        print("changed speed to ", speed)
        m.move(speed)
        

    def drive(self, speed=__INITIAL_SPEED):
        """ Main entry point of the car, and put it in drive mode

        Keyword arguments:
        speed -- speed of back wheel, range is 0 (stop) - 100 (fastest)
        """

        
        logging.info('Starting to drive forward....')

        #m.move(speed)

        i = 0
        first = 0
        start = time.time()
        while (self.camera.isOpened() and self.cap.isOpened()):
            _, image_lane = self.camera.read()
            image_objs = image_lane.copy()
            i += 1
            self.video_orig.write(image_lane)
            ret, frame = self.camera.read()
            if not (ret):
                break
            cv2_im = frame
            image_lane = self.follow_lane(image_lane)
            self.video_lane.write(image_lane)
           
            if (time.time() - start > 8):
                _, image_obj = self.cap.read()
                if image_obj is not None:
                    image_objects = image_obj.copy()
                    ret2, obj_frame = self.cap.read()
                    if not ret2:
                        break
                    cv2_im_obj = obj_frame  
                    self.object_detector.process_frame(obj_frame)
                if first == 0:
                    m.move(40)
                first+=1


            show_image('Lane Lines', image_lane)
            #show_image('Objects', image_obj)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.cleanup()
                break
            
            

    #def process_objects_on_road(self, image):
     #   image = self.traffic_sign_processor.process_objects_on_road(image)
     #   return image

    def follow_lane(self, image):
        image = self.lane_follower.follow_lane(image)
        return image


############################
# Utility Functions
############################
def show_image(title, frame, show=_SHOW_IMAGE):
    if show:
        cv2.imshow(title, frame)


def main():
    with DeepPiCar() as car:
        car.drive(40)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)-5s:%(asctime)s: %(message)s')
    
    main()
