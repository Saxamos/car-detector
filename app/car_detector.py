import os
from time import time

import numpy as np
from PIL import Image

from app import ROOT_PATH


class CarDetector:
    CAR_DISPLAY = open(os.path.join(ROOT_PATH, 'ascii_response/car.txt')).read()
    NOT_CAR_DISPLAY = open(os.path.join(ROOT_PATH, 'ascii_response/not_car.txt')).read()
    MODEL_RESOLUTION = 128, 128
    THRESHOLD = 100

    def __init__(self, pi_camera, model, saved_folder, do_processing=False):
        self.pi_camera = pi_camera
        self.model = model
        self.saved_folder = saved_folder
        self.do_processing = do_processing

    def run(self):
        while True:
            image_path = self._take_picture()

            if self.do_processing:
                image_path = self._process_image(image_path)

            prediction = self._predict(image_path)
            self._display_response(prediction)

    def _take_picture(self):
        self.pi_camera.start_preview()
        input('Press Enter to take a picture!')
        image_path = f'{self.saved_folder}/picamera_{int(time())}.jpg'
        self.pi_camera.capture(image_path, resize=self.MODEL_RESOLUTION)
        self.pi_camera.stop_preview()
        return image_path

    def _process_image(self, image_path):
        print('Processing image...')
        image_raw = np.array(Image.open(image_path).resize((128, 128)).convert('L'))
        image_raw[image_raw > self.THRESHOLD] = 255
        image_raw[image_raw <= self.THRESHOLD] = 0
        image_enhanced = Image.fromarray(np.array(Image.fromarray(image_raw).convert('RGB')))
        enhanced_filename = image_path.split('.')[0] + '_enhanced.jpg'
        image_enhanced.save(enhanced_filename)
        return enhanced_filename

    def _predict(self, image_path):
        image = np.array(Image.open(image_path))
        image_reshaped = image.reshape((1, 128, 128, 3))
        prediction = self.model.predict_classes(image_reshaped)
        return prediction[0][0]

    def _display_response(self, prediction):
        if prediction == 0:
            print(self.CAR_DISPLAY)
        else:
            print(self.NOT_CAR_DISPLAY)
