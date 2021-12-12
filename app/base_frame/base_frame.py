import logging
import os
import tkinter
from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from tensorflow.keras import models


class BaseFrame(ABC, tkinter.Frame):
    WELCOME_MESSAGE = """Welcome to the car drawing detector !
    Click on the button below
    and draw something"""

    CLASS_MAPPING = {0: "car", 1: "not_car"}

    MODEL_HEIGHT = 128
    MODEL_WIDTH = 128

    def __init__(self, parent_frame, model, saved_path):
        tkinter.Frame.__init__(self, parent_frame.container)
        self.parent_frame = parent_frame
        self.text = tkinter.Label(
            self, text=self.WELCOME_MESSAGE, font="{Comic Sans MS} 16"
        )
        self.text.grid(padx=parent_frame.mid_width, pady=parent_frame.mid_height)
        self.label = tkinter.Label(self, fg="green")

        self.model = model
        self.saved_path = saved_path
        self.image = None
        self.button_start = None

    @abstractmethod
    def _make_inference(self):
        pass

    def _resize_and_convert_input_image(self, image):
        return image.resize(
            (self.MODEL_HEIGHT, self.MODEL_WIDTH), Image.ANTIALIAS
        ).convert("L")

    def _infer(self, image):
        self.label.grid_forget()
        self.text.grid(
            padx=self.parent_frame.mid_width, pady=self.parent_frame.mid_height
        )
        self.button_start.grid()

        image.save(os.path.join(self.saved_path, "last_capture.jpg"))
        image = self.__preprocess_input_image(image)

        if self.parent_frame.viz_activation:
            self.__interpret_model(image, self.model)

        logging.info(f"Probability not being a car: {self.model.predict(image)[0, 0]}")
        self.parent_frame.predicted_class = self.CLASS_MAPPING[int(self.model.predict(image)[0, 0] > 0.5)]
        self.parent_frame.frames["gif_frame"].index = 0
        self.parent_frame.show_frame("gif_frame")

    def __preprocess_input_image(self, image):
        converted_image = image.convert("RGB")
        array_image = np.array(converted_image)
        reshaped_image = array_image.reshape(
            (1, self.MODEL_HEIGHT, self.MODEL_WIDTH, 3)
        )
        normalized_image = reshaped_image * 1 / 255
        return normalized_image

    def __interpret_model(self, image, model):
        plt.imshow(image[0])
        plt.show()

        # Extracts the outputs of the top 12 layers
        layer_outputs = [layer.output for layer in model.layers[:12]]
        # Creates a model that will return these outputs, given the model input
        activation_model = models.Model(inputs=model.input, outputs=layer_outputs)
        # Returns a list of five Numpy arrays: one array per layer activation
        activations = activation_model.predict(image)

        model.summary()
        self.__plot_activation(activations[0], 4, 8)
        self.__plot_activation(activations[1], 4, 8)
        self.__plot_activation(activations[2], 4, 5)
        self.__plot_activation(activations[3], 4, 5)
        self.__plot_activation(activations[4], 3, 4)
        self.__plot_activation(activations[5], 3, 4)
        self.__plot_activation(activations[6], 2, 4)
        self.__plot_activation(activations[7], 2, 4)
        self.__plot_neuron(activations[8], 20)  # 288)
        self.__plot_neuron(activations[9], 10)  # 128)
        self.__plot_neuron(activations[10], 1, vmin=0, vmax=1)

    @staticmethod
    def __plot_activation(activation, plot_height, plot_width):
        ix = 1
        for _ in range(plot_height):
            for _ in range(plot_width):
                # specify subplot and turn of axis
                ax = plt.subplot(plot_height, plot_width, ix)
                ax.set_xticks([])
                ax.set_yticks([])
                # plot filter channel in grayscale
                plt.imshow(activation[0, :, :, ix - 1], cmap="gray")
                ix += 1
        # show the figure
        plt.show()

    @staticmethod
    def __plot_neuron(neuron, number, vmin=None, vmax=None):
        ix = 1
        vmin = min(neuron[0, :number]) if vmin is None else vmin
        vmax = max(neuron[0, :number]) if vmax is None else vmax
        for _ in range(number):
            # specify subplot and turn of axis
            ax = plt.subplot(1, number, ix)
            ax.set_xticks([])
            ax.set_yticks([])
            # plot filter channel in grayscale
            plt.imshow([neuron[:, ix - 1]], cmap="gray", vmin=vmin, vmax=vmax)
            ix += 1
        plt.show()
