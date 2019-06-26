import os
import tkinter

import cv2
import numpy as np
from PIL import ImageTk, Image


class CameraFrame(tkinter.Frame):
    WELCOME_MESSAGE = """Welcome to the car drawing detector !
    Click on the button below
    and draw something"""
    DEFAULT_SECONDS_TO_DRAW = 5

    def __init__(self, tk_parent_frame, model, saved_path):
        tkinter.Frame.__init__(self, tk_parent_frame.container)

        self.tk_parent_frame = tk_parent_frame
        self.text = tkinter.Label(self, text=self.WELCOME_MESSAGE, font='{Comic Sans MS} 16')
        self.text.grid(padx=30, pady=80)

        self.button_start = tkinter.Button(self, text='Start camera', command=self.display_stream)
        self.button_start.grid(padx=30)

        self.button_snapshot = tkinter.Button(self, text='snapshot', command=self.make_inference)
        self.panel = tkinter.Label(self)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 160)
        self.cap.set(4, 120)
        self.video_stream()
        self.model = model
        self.saved_path = saved_path
        self.img = None

    def video_stream(self):
        _, frame = self.cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        self.img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=self.img)
        self.panel.imgtk = imgtk
        self.panel.configure(image=imgtk)
        self.panel.after(1, self.video_stream)

    def display_stream(self):
        self.button_start.grid_forget()
        self.text.grid_forget()
        self.panel.grid(padx=30)
        self.button_snapshot.grid()

    def make_inference(self):
        self.panel.grid_forget()
        self.button_snapshot.grid_forget()
        self.text.grid(padx=30, pady=80)
        self.button_start.grid(padx=30)

        image = self.img.resize((128, 128)).convert('L')
        image.save(os.path.join(self.saved_path, 'last_capture.jpg'))
        image = np.array(Image.fromarray(np.array(image)).convert('RGB')).reshape((1, 128, 128, 3))

        prediction = self.model.predict_classes(image)[0][0]
        self.tk_parent_frame.predicted_class = prediction
        self.tk_parent_frame.frames['gif_frame'].index = 0
        self.tk_parent_frame.show_frame('gif_frame')
