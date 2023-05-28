import random
import cv2
import tkinter as tk
from tkinter import filedialog
import numpy as np

class SaltAndPepperNoise:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Salt and Pepper Noise")
        self.filename = ""
        self.img = None
        # Creating a menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        # Creating a file menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        # Creating a frame to hold the display and buttons
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack()
        # Creating a label to display the selected image
        self.display = tk.Label(frame, text="No Image Selected", padx=10, pady=10)
        self.display.pack()
        # Creating a button to add salt and pepper noise
        self.add_noise_button = tk.Button(frame, text="Add Noise", state='disabled', command=self.add_noise)
        self.add_noise_button.pack()
        # Creating a button to apply filter
        self.apply_filter_button = tk.Button(frame, text="Apply Filter", state='disabled', command=self.apply_filter)
        self.apply_filter_button.pack()
        self.root.mainloop()
    def open_file(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select an image",
                                                   filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png"),
                                                              ("all files", "*.*")))
        if self.filename:
            self.img = cv2.imread(self.filename, cv2.IMREAD_COLOR)
            #self.img = cv2.imread(self.filename, cv2.IMREAD_GRAYSCALE)
            self.img = cv2.resize(self.img, (512, 512))
            self.display.configure(text="Image selected")
            self.add_noise_button.configure(state='normal')
            self.apply_filter_button.configure(state='normal')
    def adaptive_median_filter(image, max_filter_size):
        if len(image.shape) != 2:
            raise ValueError("Input image should be grayscale")

        if max_filter_size % 2 != 1:
            raise ValueError("max_filter_size should be an odd number")

        height, width = image.shape
        filtered_image = np.zeros_like(image)

        for y in range(height):
            for x in range(width):
                window_size = 3
                while window_size <= max_filter_size:
                    offset = window_size // 2
                    window = image[max(0, y - offset):min(height, y + offset + 1), max(0, x - offset):min(width, x + offset + 1)]

                    median = np.median(window)
                    min_val = np.min(window)
                    max_val = np.max(window)

                    if min_val < median < max_val:
                        if min_val < image[y, x] < max_val:
                            filtered_image[y, x] = image[y, x]
                        else:
                            filtered_image[y, x] = median
                        break
                    else:
                        window_size += 2

                if window_size > max_filter_size:
                    filtered_image[y, x] = median

        return filtered_image
    def add_noise(self):
        noisy_img = self.add_salt_and_pepper_noise(self.img, 0.05)
        cv2.imshow("Noisy Image", noisy_img)
    def apply_filter(self):
        #build in
        median = cv2.medianBlur(self.img, 5)
        #implemented
        #median = self.adaptive_median_filter(self.img,5)
        #compare = np.concatenate((self.img, median), axis=1) #side by side comparison
        cv2.imshow('img', median)
        cv2.waitKey(0)
        cv2.destroyAllWindows
    def add_salt_and_pepper_noise(self, img, probability):
        # Getting the dimensions of the image
        row, col, channels = img.shape
        # Randomly pick some pixels in the
        # image for coloring them white and black
        for i in range(row):
            for j in range(col):
                # Adding salt-and-pepper noise to each channel
                rand_num = random.random()
                if rand_num < probability/2:
                    img[i][j] = [0, 0, 0]  # black
                elif rand_num > 1 - probability/2:
                    img[i][j] = [255, 255, 255]  # white
        return img
SaltAndPepperNoise()