import tkinter

from app.base_frame.camera_frame import CameraFrame
from app.base_frame.draw_frame import DrawFrame
from app.response_frame.gif_frame import GifFrame


class ParentFrame(tkinter.Tk):
    DEFAULT_PREDICTED_CLASS = 'car'

    def __init__(self, mode, model, saved_path):
        tkinter.Tk.__init__(self)

        self.predicted_class = self.DEFAULT_PREDICTED_CLASS
        self.container = self._create_container()
        self.frames = self._create_frames(mode, model, saved_path)
        self.show_frame(f'{mode}_frame')

    def _create_container(self):
        container = tkinter.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        return container

    def _create_frames(self, mode, model, saved_path):
        frames = {'gif_frame': GifFrame(self, mode)}

        if mode == 'draw':
            frames['draw_frame'] = DrawFrame(self, model, saved_path)
        if mode == 'camera':
            frames['camera_frame'] = CameraFrame(self, model, saved_path),

        for frame in frames.values():
            frame.grid(row=0, column=0, sticky='nsew')
        return frames

    def show_frame(self, frame):
        self.frames[frame].tkraise()
