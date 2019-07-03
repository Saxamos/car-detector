import tkinter

import cv2
from PIL import ImageTk, Image

from app.base_frame.base_frame import BaseFrame


class CameraFrame(BaseFrame):
    def __init__(self, parent_frame, model, saved_path):
        super().__init__(parent_frame, model, saved_path)

        self.text_button_start = 'Start camera'
        self.button_start = tkinter.Button(self, text=self.text_button_start, command=self.display_stream)
        self.button_start.grid()

        self.button_snapshot = tkinter.Button(self, text='Snapshot', command=self.make_inference)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 160)
        self.cap.set(4, 120)
        self.video_stream()

    def display_stream(self):
        self.button_start.grid_forget()
        self.text.grid_forget()
        self.label.grid()
        self.button_snapshot.grid()

    def video_stream(self):
        _, frame = self.cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        self.image = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=self.image)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)
        self.label.after(1, self.video_stream)

    def make_inference(self):
        self.button_snapshot.grid_forget()
        # TODO: implement threshold https://github.com/zenr/ippy/blob/master/segmentation/max_entropy.py on self.image
        self._infer()
