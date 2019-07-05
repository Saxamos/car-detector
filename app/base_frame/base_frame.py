import os
import tkinter
from abc import ABC

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from keras import models


class BaseFrame(ABC, tkinter.Frame):
    WELCOME_MESSAGE = """Welcome to the car drawing detector !
    Click on the button below
    and draw something"""

    CLASS_MAPPING = {0: 'car', 1: 'not_car'}

    MODEL_HEIGHT = 128
    MODEL_WIDTH = 128

    def __init__(self, parent_frame, model, saved_path):
        tkinter.Frame.__init__(self, parent_frame.container)
        self.parent_frame = parent_frame
        self.text = tkinter.Label(self, text=self.WELCOME_MESSAGE, font='{Comic Sans MS} 16')
        self.text.grid(padx=parent_frame.mid_width, pady=parent_frame.mid_height)
        self.label = tkinter.Label(self, fg='green')

        self.model = model
        self.saved_path = saved_path
        self.image = None
        self.button_start = None

    def _infer(self):
        self.label.grid_forget()
        self.text.grid(padx=self.parent_frame.mid_width, pady=self.parent_frame.mid_height)
        self.button_start.grid()

        image = self.image.resize((self.MODEL_HEIGHT, self.MODEL_WIDTH), Image.ANTIALIAS).convert('L')
        image.save(os.path.join(self.saved_path, 'last_capture.jpg'))
        image = np.array(image.convert('RGB')).reshape((1, self.MODEL_HEIGHT, self.MODEL_WIDTH, 3))

        self._interpret_model(image)

        self.parent_frame.predicted_class = self.CLASS_MAPPING[self.model.predict_classes(image)[0][0]]
        self.parent_frame.frames['gif_frame'].index = 0
        self.parent_frame.show_frame('gif_frame')

    def _interpret_model(self, image):
        plt.imshow(image[0])
        plt.show()

        # Extracts the outputs of the top 12 layers
        layer_outputs = [layer.output for layer in self.model.layers[:12]]
        # Creates a model that will return these outputs, given the model input
        activation_model = models.Model(inputs=self.model.input, outputs=layer_outputs)
        # Returns a list of five Numpy arrays: one array per layer activation
        activations = activation_model.predict(image)

        self.model.summary()
        self._plot_activation(activations[0], 4, 8)
        self._plot_activation(activations[1], 4, 8)
        self._plot_activation(activations[2], 4, 5)
        self._plot_activation(activations[3], 4, 5)
        self._plot_activation(activations[4], 3, 4)
        self._plot_activation(activations[5], 3, 4)
        self._plot_activation(activations[6], 2, 4)
        self._plot_activation(activations[7], 2, 4)
        self._plot_neuron(activations[8], 20)  # 288)
        self._plot_neuron(activations[9], 10)  # 128)
        self._plot_neuron(activations[10], 1, vmin=0, vmax=1)

    @staticmethod
    def _plot_activation(activation, plot_height, plot_width):
        ix = 1
        for _ in range(plot_height):
            for _ in range(plot_width):
                # specify subplot and turn of axis
                ax = plt.subplot(plot_height, plot_width, ix)
                ax.set_xticks([])
                ax.set_yticks([])
                # plot filter channel in grayscale
                plt.imshow(activation[0, :, :, ix - 1], cmap='gray')
                ix += 1
        # show the figure
        plt.show()

    @staticmethod
    def _plot_neuron(neuron, number, vmin=None, vmax=None):
        ix = 1
        vmin = vmin or min(neuron[0, :number])
        vmax = vmax or max(neuron[0, :number])
        for _ in range(number):
            # specify subplot and turn of axis
            ax = plt.subplot(1, number, ix)
            ax.set_xticks([])
            ax.set_yticks([])
            # plot filter channel in grayscale
            plt.imshow([neuron[:, ix - 1]], cmap='gray', vmin=vmin, vmax=vmax)
            ix += 1
        plt.show()
