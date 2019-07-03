import os
import time
import tkinter

from PIL import ImageTk, Image

from app import ROOT_PATH


class GifFrame(tkinter.Frame):

    def __init__(self, parent_frame, mode):
        tkinter.Frame.__init__(self, parent_frame.container)

        self.mode = mode

        self.panel = tkinter.Label(self)
        self.panel.grid(padx=parent_frame.mid_height)

        self.parent_frame = parent_frame

        self.text = tkinter.Label(self, text='Do you agree with the model ?', font='{Comic Sans MS} 16')
        self.text.grid(padx=parent_frame.mid_width)

        button_agree_yes = tkinter.Button(self, text='Yes', command=self.button_agree)
        button_agree_yes.grid()
        button_agree_no = tkinter.Button(self, text='No', command=self.button_disagree)
        button_agree_no.grid()

        self.gif_images = {'car': self._create_tk_image_list('car_gif', 48),
                           'not_car': self._create_tk_image_list('not_car_gif', 89)}
        self.index = 0
        self.animate()

    def _create_tk_image_list(self, gif_name, image_number):
        gif_frames = (f'frame_{str(x + 1).zfill(2)}.jpg' for x in range(image_number))
        gif_paths = (os.path.join(ROOT_PATH, 'data', gif_name, frame) for frame in gif_frames)
        gif_images = (Image.open(path) for path in gif_paths)
        size = self.parent_frame.mid_height, self.parent_frame.mid_width
        return [ImageTk.PhotoImage(image=image.resize(size)) for image in gif_images]

    def button_agree(self):
        self.parent_frame.show_frame(f'{self.mode}_frame')
        picture_name = f'{self.parent_frame.predicted_class}_agree_{int(time.time())}.jpg'
        os.rename(os.path.join(ROOT_PATH, 'data', 'picture', 'last_capture.jpg'),
                  os.path.join(ROOT_PATH, 'data', 'picture', picture_name))

    def button_disagree(self):
        self.parent_frame.show_frame(f'{self.mode}_frame')
        picture_name = f'{self.parent_frame.predicted_class}_disagree_{int(time.time())}.jpg'
        os.rename(os.path.join(ROOT_PATH, 'data', 'picture', 'last_capture.jpg'),
                  os.path.join(ROOT_PATH, 'data', 'picture', picture_name))

    def animate(self):
        image = self.gif_images[self.parent_frame.predicted_class][self.index]
        self.panel.configure(image=image)
        self.panel.image = image
        self.index = (self.index + 1) % len(self.gif_images[self.parent_frame.predicted_class])
        self.panel.after(100, self.animate)
