import tkinter

from PIL import Image, ImageDraw

from app.base_frame.base_frame import BaseFrame


class DrawFrame(BaseFrame):
    DEFAULT_SECONDS_TO_DRAW = 15
    MAX_PIXEL_INTENSITY = 255
    MIN_PIXEL_INTENSITY = 0
    COUNTER_TEXT = 100

    def __init__(self, parent_frame, model, saved_path):
        super().__init__(parent_frame, model, saved_path)

        self.text_button_start = f'{self.DEFAULT_SECONDS_TO_DRAW} seconds to draw'
        self.button_start = tkinter.Button(self, text=self.text_button_start, command=self.__display_canvas)
        self.button_start.grid()

        self.canvas = tkinter.Canvas(self, width=parent_frame.width, height=parent_frame.height - self.COUNTER_TEXT)
        self.__initialize_draw_image()
        self.canvas.old_coords = None
        self.canvas.event_time = None

        self.draw_timer = self.DEFAULT_SECONDS_TO_DRAW
        self.label.config(text=self.draw_timer)

    def _make_inference(self):
        self.canvas.delete('all')
        self.canvas.grid_forget()

        image = self._resize_and_convert_input_image(self.image)

        self._infer(image)
        self.__initialize_draw_image()

    def __initialize_draw_image(self):
        self.image = Image.new('RGB', (self.parent_frame.width, self.parent_frame.height),
                               (self.MAX_PIXEL_INTENSITY, self.MAX_PIXEL_INTENSITY, self.MAX_PIXEL_INTENSITY))
        self.draw = ImageDraw.Draw(self.image)

    def __display_canvas(self):
        self.button_start.grid_forget()
        self.text.grid_forget()
        self.canvas.grid()
        self.label.grid()
        self.parent_frame.bind('<B1-Motion>', self.__drawing)
        self.__counter_label()

    def __counter_label(self):
        def count():
            self.draw_timer -= 1
            if self.draw_timer != 0:
                self.label.config(text=self.draw_timer)
                self.label.after(1000, count)
            else:
                self.draw_timer = self.DEFAULT_SECONDS_TO_DRAW
                self._make_inference()

        count()

    def __drawing(self, event):
        x, y = event.x, event.y
        event_time = event.time
        if self.canvas.old_coords and (event_time - self.canvas.event_time) < 200:
            x1, y1 = self.canvas.old_coords
            self.canvas.create_line(x, y, x1, y1, width=3)
            self.draw.line([x, y, x1, y1],
                           (self.MIN_PIXEL_INTENSITY, self.MIN_PIXEL_INTENSITY, self.MIN_PIXEL_INTENSITY),
                           5)
        self.canvas.old_coords = x, y
        self.canvas.event_time = event_time
