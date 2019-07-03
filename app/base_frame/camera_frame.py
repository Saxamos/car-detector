import os
import tkinter

import cv2
import numpy as np
from PIL import ImageTk, Image

from app.base_frame.base_frame import BaseFrame


class CameraFrame(BaseFrame):
    # TODO: resize everything
    def __init__(self, parent_frame, model, saved_path):
        super().__init__(parent_frame, model, saved_path)

        self.text_button_start = 'Start camera'
        self.button_start = tkinter.Button(self, text=self.text_button_start, command=self.display_stream)
        self.button_start.grid(padx=30)

        self.button_snapshot = tkinter.Button(self, text='snapshot', command=self.make_inference)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 160)
        self.cap.set(4, 120)
        self.video_stream()
        self.img = None

    def video_stream(self):
        _, frame = self.cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        self.img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=self.img)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)
        self.label.after(1, self.video_stream)

    def display_stream(self):
        self.button_start.grid_forget()
        self.text.grid_forget()
        self.label.grid(padx=30)
        self.button_snapshot.grid()

    def make_inference(self):
        self.label.grid_forget()
        self.button_snapshot.grid_forget()
        self.text.grid(padx=30, pady=80)
        self.button_start.grid(padx=30)

        # TODO: ilmplem threshold https://github.com/zenr/ippy/blob/master/segmentation/max_entropy.py

        image = self.img.resize((128, 128)).convert('L')
        image.save(os.path.join(self.saved_path, 'last_capture.jpg'))
        image = np.array(Image.fromarray(np.array(image)).convert('RGB')).reshape((1, 128, 128, 3))

        self.parent_frame.predicted_class = self.CLASS_MAPPING[self.model.predict_classes(image)[0][0]]
        self.parent_frame.frames['gif_frame'].index = 0
        self.parent_frame.show_frame('gif_frame')
