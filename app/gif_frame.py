import os
import tkinter

from PIL import ImageTk, Image

from app import ROOT_PATH


class GifFrame(tkinter.Frame):

    def __init__(self, tk_parent_frame, mode):
        tkinter.Frame.__init__(self, tk_parent_frame.container)

        self.mode = mode

        self.panel = tkinter.Label(self)
        self.panel.grid(padx=80)

        self.tk_parent_frame = tk_parent_frame

        self.text = tkinter.Label(self, text='Do you agree with the model ?')
        self.text.grid()

        button_agree_yes = tkinter.Button(self, text='Yes', command=self.button_agree)
        button_agree_yes.grid()
        button_agree_no = tkinter.Button(self, text='No', command=self.button_disagree)
        button_agree_no.grid()

        self.gif_images = {
            0: [ImageTk.PhotoImage(
                image=Image.open(os.path.join(ROOT_PATH, 'data', 'car_gif', f'frame_{str(x + 1).zfill(2)}.jpg')).resize(
                    (200, 240))) for x in
                range(48)],

            1: [ImageTk.PhotoImage(
                image=Image.open(
                    os.path.join(ROOT_PATH, 'data', 'not_car_gif', f'frame_{str(x + 1).zfill(2)}.jpg')).resize(
                    (200, 240))) for x
                in range(89)]

        }
        self.index = 0
        self.animate()

    def button_agree(self):
        self.tk_parent_frame.show_frame(f'{self.mode}_frame')
        # TODO: add real response
        os.rename(os.path.join(ROOT_PATH, 'data', 'picture', 'last_capture.jpg'),
                  os.path.join(ROOT_PATH, 'data', 'picture', 'agree.jpg'))

    def button_disagree(self):
        self.tk_parent_frame.show_frame(f'{self.mode}_frame')
        os.rename(os.path.join(ROOT_PATH, 'data', 'picture', 'last_capture.jpg'),
                  os.path.join(ROOT_PATH, 'data', 'picture', 'disagree.jpg'))

    def animate(self):
        image = self.gif_images[self.tk_parent_frame.predicted_class][self.index]
        self.panel.configure(image=image)
        self.panel.image = image
        self.index = (self.index + 1) % len(self.gif_images[self.tk_parent_frame.predicted_class])
        self.panel.after(100, self.animate)
