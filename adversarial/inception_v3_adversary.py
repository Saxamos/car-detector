"""
Credits:
https://medium.com/@ageitgey/machine-learning-is-fun-part-8-how-to-intentionally-trick-neural-networks-b55da32b7196
"""
import os

import numpy as np
from PIL import Image
from keras import backend as K
from keras.applications import inception_v3
from keras.preprocessing import image

from app import ROOT_PATH

model = inception_v3.InceptionV3()

# Load the image file and convert it to a numpy array
img_path = os.path.join(ROOT_PATH, 'adversarial', 'sax.png')
img = image.load_img(img_path, target_size=(299, 299))
input_image = image.img_to_array(img)

# Scale the image so all pixel intensities are between [-1, 1] as the model expects
input_image /= 255.
input_image -= 0.5
input_image *= 2.

# Add a 4th dimension for batch size (as Keras expects)
input_image = np.expand_dims(input_image, axis=0)

# Run the image through the neural network
predictions = model.predict(input_image)

# Convert the predictions into text and print them
predicted_classes = inception_v3.decode_predictions(predictions, top=1)
imagenet_id, name, confidence = predicted_classes[0][0]
print(f'This is a {name} with {confidence * 100:.4}% confidence!')

# Grab a reference to the first and last layer of the neural net
model_input_layer = model.layers[0].input
model_output_layer = model.layers[-1].output

# Choose an ImageNet object to fake
# The list of classes is available here: https://gist.github.com/ageitgey/4e1342c10a71981d0b491e1b8227328b
# Class #966 is "red_wine"
object_type_to_fake = 966

# Pre-calculate the maximum change we will allow to the image
# We'll make sure our hacked image never goes past this so it doesn't look funny.
# A larger number produces an image faster but risks more distortion.
distortion = 0.3
max_change_above = input_image + distortion
max_change_below = input_image - distortion

# Create a copy of the input image to hack on and give crop of image that we want to modify
hacked_image = np.copy(input_image)
hacked_image_crop = hacked_image[:, 200:, 200:, :]

# How much to update the hacked image in each iteration
learning_rate = 10

# Define the cost function.
# Our 'cost' will be the likelihood out image is the target class according to the pre-trained model
cost_function = model_output_layer[0, object_type_to_fake]

# We'll ask Keras to calculate the gradient based on the input image and the currently predicted class
# In this case, referring to "model_input_layer" will give us back image we are hacking.
gradient_function = K.gradients(cost_function, model_input_layer)[0]

# Create a Keras function that we can call to calculate the current cost and gradient
grab_cost_and_gradients_from_model = K.function([model_input_layer, K.learning_phase()],
                                                [cost_function, gradient_function])

cost = 0.0

# In a loop, keep adjusting the hacked image slightly so that it tricks the model more and more
# until it gets to at least 80% confidence
while cost < 0.80:
    # Check how close the image is to our target class and grab the gradients we
    # can use to push it one more step in that direction.
    # Note: It's really important to pass in '0' for the Keras learning mode here!
    # Keras layers behave differently in prediction vs. train modes!
    cost, gradients = grab_cost_and_gradients_from_model([hacked_image_crop, 0])
    cost_global, _ = grab_cost_and_gradients_from_model([hacked_image, 0])

    # Move the hacked image one step further towards fooling the model
    hacked_image_crop += gradients * learning_rate
    hacked_image[:, 200:, 200:, :] += gradients * learning_rate

    # Ensure that the image doesn't ever change too much to either look funny or to become an invalid image
    # hacked_image = np.clip(hacked_image, max_change_below, max_change_above)
    hacked_image = np.clip(hacked_image, -1.0, 1.0)
    hacked_image_crop = np.clip(hacked_image_crop, -1.0, 1.0)

    print(f'Model\'s predicted likelihood that the crop is a red_wine: {cost * 100:.8}')
    print(f'Model\'s predicted likelihood that the image is a red_wine: {cost_global * 100:.8}')

# De-scale the image's pixels from [-1, 1] back to the [0, 255] range
img = hacked_image[0]
img /= 2.
img += 0.5
img *= 255.

# Save the hacked image!
im = Image.fromarray(img.astype(np.uint8))
im.save('toto.png')
