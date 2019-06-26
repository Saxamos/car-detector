import os
import unittest
from unittest.mock import MagicMock

from car_detector import CarDetector
from freezegun import freeze_time
from keras.engine.saving import load_model

from app import ROOT_PATH


# TODO: test
class TestCarDetector(unittest.TestCase):
    def setUp(self):
        pi_camera = MagicMock()
        self.current_folder = os.path.join(ROOT_PATH, 'tests/raspberry/data')
        model = load_model(os.path.join(ROOT_PATH, 'model') + '/model.h5')
        self.car_detector = CarDetector(pi_camera, model, saved_folder=self.current_folder)

    def test_display_response_with_car_prediction(self):
        # Given
        prediction = 0

        # When
        self.car_detector._display_response(prediction)

        # Then
        # A car should display

    def test_display_response_with_no_car_prediction(self):
        # Given
        prediction = 1

        # When
        self.car_detector._display_response(prediction)

        # Then
        # Homer simpsons should talk to you

    def test_predict_if_car_return_right_inference(self):
        # Given
        image_path_gen = (os.path.join(ROOT_PATH, 'picture') + f'/{name}.jpg' for name in
                          ('car_1', 'car_2', 'not_in_train_data_scarab', 'to_thin_car', 'sax'))

        # When
        predictions = [self.car_detector._predict(image_path) for image_path in image_path_gen]

        # Then
        expected_predictions = [0, 0, 0, 1, 0]
        self.assertEqual(predictions, expected_predictions)

    @unittest.skip('need keyboard interaction')
    @freeze_time('2019-04-04')
    def test_with_mocked_camera_and_mocked_model(self):
        self.car_detector.run()
