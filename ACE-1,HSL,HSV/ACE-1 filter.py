import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np


def apply_filter():
    global photo
    global image_path
    try:
        # Get the slider values
        K1 = slider1.get()
        K2 = slider2.get()
        N = slider3.get()
        
        # Open the image and convert it to grayscale
        img = np.array(Image.open(image_path).convert('L'))

        # Apply the ACE1 filter to the image
        filtered_img = ace1_filter(img, N, K1, K2)

        # Convert the filtered image to a PIL Image object
        filtered_img = (filtered_img * 255).astype(np.uint8)
        filtered_image = Image.fromarray(filtered_img)

        # Create a new PhotoImage object from the filtered image
        photo = ImageTk.PhotoImage(filtered_image)

        # Close the existing window if it is open
        if 'new_window' in globals():
            new_window.destroy()

        # Create a new window to display the modified image
        new_window = tk.Toplevel(root)
        new_window.geometry('{}x{}'.format(
            filtered_image.width, filtered_image.height))
        new_window.title("Filtered Image")

        # Add a label widget to display the modified image
        label = tk.Label(new_window, image=photo)
        label.pack(fill=tk.BOTH, expand=True)
    except AttributeError:
        # Show an error message if an image has not been selected
        messagebox.showerror("Error", "Please select an image first.")
    except Exception as e:
        # Show an error message if an unexpected error occurs
        messagebox.showerror("Error", str(e))

def select_image():
    global photo
    global image_path
    # Open file dialog to select an image file
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            # If there is a previously opened image window, close it
            new_window.destroy()
        except NameError:
            pass
        # Save the path of the selected image
        image_path = file_path
        # Open the image using PIL.Image
        image = Image.open(image_path)
        # Resize the image if its maximum dimension is larger than 1000 pixels
        if max(image.size) > 1000:
            ratio = max(image.size) / 1000
            image = image.resize(
                (int(image.size[0]/ratio), int(image.size[1]/ratio)), resample=Image.LANCZOS)
        # Convert the image to a PhotoImage object using ImageTk.PhotoImage
        photo = ImageTk.PhotoImage(image)
        # Create a new window to display the image
        new_window = tk.Toplevel(root)
        new_window.geometry('{}x{}'.format(image.size[0], image.size[1]))
        new_window.title("Orignal Image")
        # Add a Label widget to the new window to display the image
        label = tk.Label(new_window, image=photo)
        label.image = photo
        label.pack(fill=tk.BOTH, expand=True)
        message_label.config(text=" ")
        button1.config(state=tk.NORMAL)

def ace1_filter(img, N, K1, K2):
    rows, cols = img.shape
    filtered_img = np.zeros((rows, cols))
    progress_interval = rows // 10  # Print progress every 10% of rows processed
    for i in range(N//2, rows-N//2):
        for j in range(N//2, cols-N//2):
            window = img[i-N//2:i+N//2+1, j-N//2:j+N//2+1]
            mean = np.mean(window)
            variance = np.var(window)
            filtered_img[i, j] = (img[i, j] - mean + K1 *
                                  variance) / (1 + K2 * variance)
        # Print progress at intervals
        if i % progress_interval == 0:
            progress = int(i * 100 / rows)
            print(f'Filtering image: {progress}%')

    print('Filtering complete.')
    message_label.config(text="Filtering complete.")
    return filtered_img

root = tk.Tk()

slider1 = tk.Scale(root, from_=0, to=1, resolution=0.01,
                   orient=tk.HORIZONTAL, label="K1", length=300)
slider1.pack()
slider2 = tk.Scale(root, from_=0, to=1, resolution=0.01,
                   orient=tk.HORIZONTAL, label="K2", length=300)
slider2.pack()
slider3 = tk.Scale(root, from_=3, to=1000, orient=tk.HORIZONTAL,
                   label="Window Size (NxN)", length=300)
slider3.pack()
button2 = tk.Button(root, text="Select Image", command=select_image)
button2.pack()
button1 = tk.Button(root, text="Apply Filter",
                    command=apply_filter, state=tk.DISABLED)
button1.pack()
message_label = tk.Label(root, text=" ",state=tk.DISABLED)
message_label.pack()

root.title("ACE-1 Filter")
root.mainloop()