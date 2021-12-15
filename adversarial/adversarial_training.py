"""Run this on GPU"""
import os

import numpy as np
import tensorflow as tf
from PIL import Image

from app import ROOT_PATH

tf.compat.v1.disable_v2_behavior()

model = tf.keras.models.load_model(os.path.join(ROOT_PATH, "model", "model.h5"))

# Load the image file and convert it to a numpy array
img_path = os.path.join(ROOT_PATH, "data", "car_train_data", "not_car", "parrot_37.jpg")
img = tf.keras.preprocessing.image.load_img(img_path, target_size=(128, 128))
input_image = tf.keras.preprocessing.image.img_to_array(img)

# Scale the image so all pixel intensities are between [0, 1] as the model expects
input_image /= 255.0

# Add a 4th dimension for batch size (as Keras expects)
input_image = np.expand_dims(input_image, axis=0)

# Run the image through the neural network
confidence = model.predict(input_image)[0, 0]
prediction = 1 if confidence > 0.5 else 0

# Convert the predictions into text and print them
CLASS_MAPPING = {0: "car", 1: "not_car"}
predicted_classes = CLASS_MAPPING[prediction]
print(f"This is a {predicted_classes} with {confidence * 100:.4}% confidence!")

# Grab a reference to the first and last layer of the neural net
model_input_layer = model.layers[0].input
model_output_layer = model.layers[-1].output

object_type_to_fake = 0

# Pre-calculate the maximum change we will allow to the image
# We'll make sure our hacked image never goes past this so it doesn't look funny.
# A larger number produces an image faster but risks more distortion.
distortion = 0.3
max_change_above = input_image + distortion
max_change_below = input_image - distortion

# Create a copy of the input image to hack on
hacked_image = np.copy(input_image)

# How much to update the hacked image in each iteration
learning_rate = 0.1

# Define the cost function.
# Our 'cost' will be the likelihood out image is the target class according to the pre-trained model
cost_function = model_output_layer[0, object_type_to_fake]

# We'll ask Keras to calculate the gradient based on the input image and the currently predicted class
# In this case, referring to "model_input_layer" will give us back image we are hacking.
gradient_function = tf.keras.backend.gradients(cost_function, model_input_layer)[0]

# Create a Keras function that we can call to calculate the current cost and gradient
grab_cost_and_gradients_from_model = tf.keras.backend.function(
    [model_input_layer, tf.keras.backend.learning_phase()],
    [cost_function, gradient_function],
)

cost = 1.0
i = 0
while cost > 0.1:
    # Check how close the image is to our target class and grab the gradients we
    # can use to push it one more step in that direction.
    # Note: It's really important to pass in '0' for the Keras learning mode here!
    # Keras layers behave differently in prediction vs. train modes!
    cost, gradients = grab_cost_and_gradients_from_model([hacked_image, 0])

    # Move the hacked image one step further towards fooling the model
    hacked_image -= gradients * learning_rate

    # Ensure that the image doesn't ever change too much to either look funny or to become an invalid image
    hacked_image = np.clip(hacked_image, max_change_below, max_change_above)
    hacked_image = np.clip(hacked_image, 0, 1.0)

    i += 1
    if i % 1000 == 0:
        print(
            f"Model's predicted likelihood that the image is a car: {(1 - cost) * 100:.8}"
        )

# De-scale the image's pixels from [0, 1] back to the [0, 255] range
descaled_input_image = input_image[0] * 255.0
Image.fromarray(descaled_input_image.astype(np.uint8)).save("resized_parrot.png")

descaled_hacked_image = hacked_image[0] * 255.0
Image.fromarray(descaled_hacked_image.astype(np.uint8)).save("hacked_parrot.png")
