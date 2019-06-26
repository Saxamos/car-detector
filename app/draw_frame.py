import os
import tkinter as tk

import numpy as np
from PIL import Image, ImageDraw


class DrawFrame(tk.Frame):
    WELCOME_MESSAGE = """Welcome to the car drawing detector !
    Click on the button below
    and draw something"""
    DEFAULT_SECONDS_TO_DRAW = 5

    def __init__(self, tk_parent_frame, model, saved_path):
        tk.Frame.__init__(self, tk_parent_frame.container)

        self.tk_parent_frame = tk_parent_frame
        self.text = tk.Label(self, text=self.WELCOME_MESSAGE, font='{Comic Sans MS} 16')
        self.text.grid(padx=30, pady=80)

        self.button_start = tk.Button(self, text=f'{self.DEFAULT_SECONDS_TO_DRAW} seconds to draw',
                                      command=self.display_canvas)
        self.button_start.grid(padx=30)

        self.canvas = tk.Canvas(self, width=460, height=300)
        self.image = Image.new('RGB', (460, 300), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)
        self.canvas.old_coords = None
        self.canvas.event_time = None

        self.draw_timer = self.DEFAULT_SECONDS_TO_DRAW

        self.label = tk.Label(self, fg='green')
        self.label.config(text=self.draw_timer)

        self.model = model
        self.saved_path = saved_path

    def display_canvas(self):
        self.button_start.grid_forget()
        self.text.grid_forget()
        self.canvas.grid(padx=10, pady=10)
        self.label.grid()
        self.tk_parent_frame.bind('<B1-Motion>', self.drawing)
        self.counter_label()

    def counter_label(self):
        # TODO: omagad pls refactome
        def count():
            self.draw_timer -= 1
            if self.draw_timer != 0:
                self.label.config(text=self.draw_timer)
                self.label.after(1000, count)
            else:
                self.draw_timer = self.DEFAULT_SECONDS_TO_DRAW
                self.make_inference()

        count()

    def drawing(self, event):
        x, y = event.x, event.y
        event_time = event.time
        if self.canvas.old_coords and (event_time - self.canvas.event_time) < 200:
            x1, y1 = self.canvas.old_coords
            self.canvas.create_line(x, y, x1, y1)
            self.draw.line([x, y, x1, y1], (0, 0, 0), 5)
        self.canvas.old_coords = x, y
        self.canvas.event_time = event_time

    def make_inference(self):
        self.canvas.delete('all')
        self.canvas.grid_forget()
        self.label.grid_forget()

        image = self.image.resize((128, 128)).convert('L')
        self.image = Image.new('RGB', (460, 300), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)
        self.text.grid(padx=30, pady=80)
        self.button_start.grid(padx=30)

        image.save(os.path.join(self.saved_path, 'last_capture.jpg'))
        image = np.array(image.convert('RGB')).reshape((1, 128, 128, 3))

        prediction = self.model.predict_classes(image)[0][0]
        self.tk_parent_frame.predicted_class = prediction
        self.tk_parent_frame.frames['gif_frame'].index = 0
        self.tk_parent_frame.show_frame('gif_frame')
