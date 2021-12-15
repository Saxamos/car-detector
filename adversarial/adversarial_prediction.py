import os

import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

from app import ROOT_PATH

model = load_model(os.path.join(ROOT_PATH, "model", "model.h5"))
CLASS_MAPPING = {0: "car", 1: "not_car"}


def load_image_and_predict_class(img_path):
    img = image.load_img(img_path, target_size=(128, 128))
    input_image = image.img_to_array(img)
    input_image /= 255.0
    input_image = np.expand_dims(input_image, axis=0)
    confidence = model.predict(input_image)[0, 0]
    prediction = 1 if confidence > 0.5 else 0
    predicted_classes = CLASS_MAPPING[prediction]
    print(f"This is a {predicted_classes}")
    print(f"Probability to belong to class car: {1 - confidence:.3}")


print("\nHack:")
load_image_and_predict_class(
    os.path.join(ROOT_PATH, "adversarial", "hacked_parrot.png")
)

print("\nOriginal:")
load_image_and_predict_class(
    os.path.join(ROOT_PATH, "adversarial", "resized_parrot.png")
)
