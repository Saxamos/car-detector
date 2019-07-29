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
        pixel_intensity_histogram = np.histogram(image, bins=256, range=(0, 256))[0]
        threshold = self.__max_entropy(pixel_intensity_histogram)

        if self.parent_frame.viz_entropy:
            plt.plot(pixel_intensity_histogram)
            plt.axvline(x=threshold, color='r')
            plt.show()
        return threshold

    def __max_entropy(self, histogram):
        """
        "A New Method for Gray-Level Picture Thresholding Using the Entropy of the Histogram"
        Kapur J.N., Sahoo P.K., and Wong A.K.C. (1985)
        https://github.com/zenr/ippy/blob/master/segmentation/max_entropy.py
        :param histogram: Sequence representing the histogram of the image
        :return threshold: Resulting maximum entropy threshold
        """
        cdf = histogram.astype(np.float).cumsum()
        non_null_bin_indexes = np.nonzero(histogram)[0]

        max_entropy, best_threshold = 0, 0
        for i in range(len(non_null_bin_indexes)):
            dark_histogram = histogram[non_null_bin_indexes[:i + 1]]
            number_of_pixel_in_dark_histogram = cdf[non_null_bin_indexes[i]]
            dark_entropy = self.__compute_entropy(dark_histogram, number_of_pixel_in_dark_histogram)

            bright_histogram = histogram[non_null_bin_indexes[i + 1:]]
            number_of_pixel_in_bright_histogram = cdf[-1] - cdf[non_null_bin_indexes[i]]
            bright_entropy = self.__compute_entropy(bright_histogram, number_of_pixel_in_bright_histogram)

            entropy = dark_entropy + bright_entropy
            if entropy > max_entropy:
                max_entropy, best_threshold = entropy, i + 1
        return best_threshold

    @staticmethod
    def __compute_entropy(histogram, number_of_pixel_in_histogram):
        probability_density_function = histogram / number_of_pixel_in_histogram
        return -np.sum(probability_density_function * np.log(probability_density_function))


"""
for multiclass grey level segmentation
"""
# def __binarize_image(self, image):
#     threshold = self.__get_threshold(image)
#     image[image < threshold[0]] = 0
#     image[image >= threshold[1]] = 255
#     image[(image != 0) & (image != 255)] = 120
#     return Image.fromarray(image)
#
# def __get_threshold(self, image):
#     pixel_intensity_histogram = np.histogram(image, bins=256, range=(0, 256))[0]
#     threshold = self.__max_entropy(pixel_intensity_histogram)
#
#     if self.parent_frame.viz_entropy:
#         plt.plot(pixel_intensity_histogram)
#         plt.axvline(x=threshold[0], color='r')
#         plt.axvline(x=threshold[1], color='r')
#         plt.show()
#     return threshold
#
# def __max_entropy(self, histogram):
#     cdf = histogram.astype(np.float).cumsum()
#     non_null_bin_indexes = np.nonzero(histogram)[0]
#
#     max_entropy, best_threshold = 0, (0, 0)
#     for i in range(len(non_null_bin_indexes)):
#         for j in range(i, len(non_null_bin_indexes)):
#             dark_histogram = histogram[non_null_bin_indexes[:i + 1]]
#             number_of_pixel_in_dark_histogram = cdf[non_null_bin_indexes[i]]
#             dark_entropy = self.__compute_entropy(dark_histogram, number_of_pixel_in_dark_histogram)
#
#             mid_histogram = histogram[non_null_bin_indexes[i + 1:j + 1]]
#             number_of_pixel_in_mid_histogram = cdf[non_null_bin_indexes[j]] - cdf[non_null_bin_indexes[i]]
#             mid_entropy = self.__compute_entropy(mid_histogram, number_of_pixel_in_mid_histogram)
#
#             bright_histogram = histogram[non_null_bin_indexes[j + 1:]]
#             number_of_pixel_in_bright_histogram = cdf[-1] - cdf[non_null_bin_indexes[j]]
#             bright_entropy = self.__compute_entropy(bright_histogram, number_of_pixel_in_bright_histogram)
#
#             entropy = dark_entropy + bright_entropy + mid_entropy
#             if entropy > max_entropy:
#                 max_entropy, best_threshold = entropy, (i + 1, j + 1)
#     return best_threshold
