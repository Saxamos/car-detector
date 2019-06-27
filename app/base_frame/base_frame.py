import tkinter
from abc import ABC


class BaseFrame(ABC, tkinter.Frame):
    WELCOME_MESSAGE = """Welcome to the car drawing detector !
    Click on the button below
    and draw something"""

    CLASS_MAPPING = {0: 'car', 1: 'not_car'}

    def __init__(self, parent_frame, model, saved_path):
        tkinter.Frame.__init__(self, parent_frame.container)

        self.parent_frame = parent_frame

        self.text = tkinter.Label(self, text=self.WELCOME_MESSAGE, font='{Comic Sans MS} 16')
        self.text.grid(padx=30, pady=80)

        self.label = tkinter.Label(self, fg='green')

        self.model = model
        self.saved_path = saved_path
