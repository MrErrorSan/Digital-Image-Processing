import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


# Define a function called "enhance_contrast_hsv" that takes in an image
def enhance_contrast_hsv(image):
    # Convert to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv_image)
    # Apply histogram equalization to S channel
    s_equalized = cv2.equalizeHist(s)
    # Apply stretching to V channel
    v_stretched = cv2.normalize(v, None, 0, 255, cv2.NORM_MINMAX)
    # Merge the processed HSV channels
    hsv_enhanced = cv2.merge((h, s_equalized, v_stretched))
    # Convert to the RGB
    enhanced_image = cv2.cvtColor(hsv_enhanced, cv2.COLOR_HSV2BGR)
    return enhanced_image

# Define a function to perform contrast enhancement using HSL color space
def enhance_contrast_hsl(image):
    # Convert to HSL
    hsl_image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    h, s, l = cv2.split(hsl_image)
    # Apply histogram equalization to S channel
    s_equalized = cv2.equalizeHist(l)
    # Apply stretching to L channel
    l_stretched = cv2.normalize(s, None, 0, 255, cv2.NORM_MINMAX)
    hsl_enhanced = cv2.merge((h, s_equalized, l_stretched))
    # Convert to the RGB
    enhanced_image = cv2.cvtColor(hsl_enhanced, cv2.COLOR_HLS2BGR)
    return enhanced_image

def select_image():
    # Declare the "image" variable as global, so it can be accessed and modified from within the function
    global image
    # Open a file dialog and get the file path of the selected image
    file_path = filedialog.askopenfilename()
    # If a file path was selected
    if file_path:
        image = cv2.imread(file_path)
        # Convert the image to a PIL Image object and resize it to maximum size of (700, 700)
        original_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        max_size = (700, 700)
        original_pil.thumbnail(max_size, Image.LANCZOS)
        # Convert the resized image to a Tkinter-compatible format and set it as the image for a label widget called "original_label"
        original_tk = ImageTk.PhotoImage(original_pil)
        original_label.config(image=original_tk, bg='#333', fg='#ddd')
        original_label.image = original_tk
        # Enable buttons ("hsl_button" and "hsv_button")
        hsl_button.config(state=tk.NORMAL)
        hsv_button.config(state=tk.NORMAL)

def open_enhanced_image(image):
    enhanced_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    max_size = (700, 700)
    enhanced_pil.thumbnail(max_size, Image.LANCZOS)
    enhanced_tk = ImageTk.PhotoImage(enhanced_pil)
    enhanced_window = tk.Toplevel(root)
    enhanced_label = tk.Label(enhanced_window, image=enhanced_tk)
    enhanced_label.image = enhanced_tk
    enhanced_label.pack()

def hsl_enhancement():
    enhanced_image_hsl = enhance_contrast_hsl(image)
    open_enhanced_image(enhanced_image_hsl)

def hsv_enhancement():
    enhanced_image_hsv = enhance_contrast_hsv(image)
    open_enhanced_image(enhanced_image_hsv)

# Create the main window
root = tk.Tk()
root.title('Color Contrast Enhancement')
# Create a label to select an image
message_label = tk.Label(
    root, text='Please select an image to enhance', fg='#333')
message_label.pack(pady=5)
# Create a button to select an image
select_button = tk.Button(root, text='Select Image', command=select_image)
select_button.pack(pady=10)
# Create two buttons for enhancing the image using HSL and HSV respectively
hsl_button = tk.Button(root, text='HSL Enhancement',
                       command=hsl_enhancement, state=tk.DISABLED)
hsl_button.pack(side=tk.TOP, padx=2)
hsv_button = tk.Button(root, text='HSV Enhancement',
                       command=hsv_enhancement, state=tk.DISABLED)
hsv_button.pack(side=tk.TOP, padx=2)
# Create a label to display the original image
original_label = tk.Label(root)
original_label.pack(side=tk.BOTTOM, padx=2)
# Event loop to display the GUI
root.mainloop()