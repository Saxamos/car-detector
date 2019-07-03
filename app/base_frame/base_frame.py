import os
import tkinter
from abc import ABC

import numpy as np
from PIL import Image


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

        self.parent_frame.predicted_class = self.CLASS_MAPPING[self.model.predict_classes(image)[0][0]]
        self.parent_frame.frames['gif_frame'].index = 0
        self.parent_frame.show_frame('gif_frame')
