import argparse

from keras.models import load_model
from picamera import PiCamera

from app.car_detector import CarDetector

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument('-m', '--model', help='Path to the model', default='model_qui_dechire.h5')
argument_parser.add_argument('-s', '--saved', help='Folder to save images', default='/home/pi/picamera_pictures')
argument_parser.add_argument('-p', '--processing', help='Use processing', action='store_true')
args = argument_parser.parse_args()

pi_camera = PiCamera(resolution=(256,256))
print('Loading {} model'.format(args.model))
model = load_model(args.model)

car_detector = CarDetector(pi_camera, model, args.saved, args.processing)
car_detector.run()
