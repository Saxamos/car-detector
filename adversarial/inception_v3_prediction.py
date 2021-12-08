import os

import numpy as np
from keras.applications import inception_v3
from keras.preprocessing import image

from app import ROOT_PATH

model = inception_v3.InceptionV3()


def load_image_and_predict_class(img_path):
    img = image.load_img(img_path, target_size=(299, 299))
    input_image = image.img_to_array(img)
    input_image /= 255.0
    input_image -= 0.5
    input_image *= 2.0
    input_image = np.expand_dims(input_image, axis=0)
    predictions = model.predict(input_image)
    predicted_classes = inception_v3.decode_predictions(predictions, top=5)
    print(predicted_classes)


print("\nOriginal:")
load_image_and_predict_class(os.path.join(ROOT_PATH, "adversarial", "resized_sax.png"))

print("\nHack:")
load_image_and_predict_class(os.path.join(ROOT_PATH, "adversarial", "hacked_sax.png"))
