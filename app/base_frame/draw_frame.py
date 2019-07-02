import os
import tkinter

import numpy as np
from PIL import Image, ImageDraw

from app.base_frame.base_frame import BaseFrame


class DrawFrame(BaseFrame):
    DEFAULT_SECONDS_TO_DRAW = 5
    MAX_PIXEL_INTENSITY = 255
    MIN_PIXEL_INTENSITY = 0

    def __init__(self, parent_frame, model, saved_path):
        super().__init__(parent_frame, model, saved_path)

        self.text_button_start = f'{self.DEFAULT_SECONDS_TO_DRAW} seconds to draw'
        self.button_start = tkinter.Button(self, text=self.text_button_start, command=self.display_canvas)
        self.button_start.grid(padx=parent_frame.mid_width)

        self.canvas = tkinter.Canvas(self, width=parent_frame.width, height=parent_frame.height)
        self.image = Image.new('RGB', (parent_frame.width, parent_frame.height),
                               (self.MAX_PIXEL_INTENSITY, self.MAX_PIXEL_INTENSITY, self.MAX_PIXEL_INTENSITY))
        self.draw = ImageDraw.Draw(self.image)
        self.canvas.old_coords = None
        self.canvas.event_time = None

        self.draw_timer = self.DEFAULT_SECONDS_TO_DRAW

        self.label.config(text=self.draw_timer)

    # TODO: abstract this method
    def display_canvas(self):
        self.button_start.grid_forget()
        self.text.grid_forget()
        self.canvas.grid()
        self.label.grid()
        self.parent_frame.bind('<B1-Motion>', self.drawing)
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
            self.draw.line([x, y, x1, y1],
                           (self.MIN_PIXEL_INTENSITY, self.MIN_PIXEL_INTENSITY, self.MIN_PIXEL_INTENSITY),
                           5)
        self.canvas.old_coords = x, y
        self.canvas.event_time = event_time

    # TODO: abstract this method
    def make_inference(self):
        self.canvas.delete('all')
        self.canvas.grid_forget()

        self.label.grid_forget()

        image = self.image.resize((128, 128)).convert('L')
        self.image = Image.new('RGB', (460, 300), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)
        self.text.grid(padx=self.parent_frame.mid_width, pady=self.parent_frame.mid_height)
        self.button_start.grid(padx=30)

        image.save(os.path.join(self.saved_path, 'last_capture.jpg'))
        image = np.array(image.convert('RGB')).reshape((1, 128, 128, 3))

        self.parent_frame.predicted_class = self.CLASS_MAPPING[self.model.predict_classes(image)[0][0]]
        self.parent_frame.frames['gif_frame'].index = 0
        self.parent_frame.show_frame('gif_frame')
