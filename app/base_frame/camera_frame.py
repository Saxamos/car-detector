import tkinter

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageTk, Image

from app.base_frame.base_frame import BaseFrame


class CameraFrame(BaseFrame):
    def __init__(self, parent_frame, model, saved_path):
        super().__init__(parent_frame, model, saved_path)

        self.text_button_start = 'Start camera'
        self.button_start = tkinter.Button(self, text=self.text_button_start, command=self.__display_stream)
        self.button_start.grid()

        self.button_snapshot = tkinter.Button(self, text='Snapshot', command=self._make_inference)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 160)
        self.cap.set(4, 120)
        self.__video_stream()

    def _make_inference(self):
        # TODO: take pic with same width and height to not deform when resize
        self.button_snapshot.grid_forget()
        image = self._resize_and_convert_input_image(self.image)
        image = self.__binarize_image(np.array(image))
        self._infer(image)

    def __display_stream(self):
        self.button_start.grid_forget()
        self.text.grid_forget()
        self.label.grid()
        self.button_snapshot.grid()

    def __video_stream(self):
        _, frame = self.cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        self.image = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=self.image)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)
        self.label.after(1, self.__video_stream)

    def __binarize_image(self, image):
        threshold = self.__get_threshold(image)
        image[image < threshold] = 0
        image[image >= threshold] = 255
        return Image.fromarray(image)

    def __get_threshold(self, image):
        hist = np.histogram(image, bins=256, range=(0, 256))[0]
        threshold = CameraFrame.__max_entropy(hist)

        if self.parent_frame.viz_entropy:
            plt.plot(hist)
            plt.axvline(x=threshold, color='r')
            plt.show()
        return threshold

    @staticmethod
    def __max_entropy(data):
        """
        Implements Kapur-Sahoo-Wong (Maximum Entropy) thresholding method
        "A New Method for Gray-Level Picture Thresholding Using the Entropy of the Histogram"
        Kapur J.N., Sahoo P.K., and Wong A.K.C. (1985)
        https://github.com/zenr/ippy/blob/master/segmentation/max_entropy.py
        :param data: Sequence representing the histogram of the image
        :return threshold: Resulting maximum entropy threshold
        """
        cdf = data.astype(np.float).cumsum()  # calculate CDF (cumulative density function)
        valid_idx = np.nonzero(data)[0]  # find histogram's nonzero area
        first_bin, last_bin = valid_idx[0], valid_idx[-1]
        max_ent, threshold = 0, 0  # initialize search for maximum
        for pix_intensity in range(first_bin, last_bin + 1):
            # Background (dark)
            hist_range = data[:pix_intensity + 1]
            hist_range = hist_range[hist_range != 0] / cdf[pix_intensity]  # normalize within range & remove zeros
            tot_ent = -np.sum(hist_range * np.log(hist_range))  # background entropy
            # Foreground/Object (bright)
            hist_range = data[pix_intensity + 1:]
            hist_range = hist_range[hist_range != 0] / (cdf[last_bin] - cdf[pix_intensity])
            tot_ent -= np.sum(hist_range * np.log(hist_range))  # accumulate object entropy
            # find max
            if tot_ent > max_ent:
                max_ent, threshold = tot_ent, pix_intensity
        return threshold
