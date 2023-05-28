from PIL import Image
import numpy as np


def linear_mapping(image, a, b, c, d):
    img_array = np.array(image)
    # apply the linear mapping equation to the image array
    img_array = (img_array - a) * ((d - c) / (b - a)) + c
    # convert the array back to a PIL Image object
    return Image.fromarray(np.uint8(img_array))


def nonlinear_mapping(image, gamma):
    img_array = np.array(image)
    # apply the nonlinear mapping equation to the image array
    img_array = 255 * np.power((img_array / 255), gamma)
    # convert the array back to a PIL Image object
    return Image.fromarray(np.uint8(img_array))


def digital_negative(image):
    img_array = np.array(image)
    # invert the image array by subtracting it from 255
    img_array = 255 - img_array
    # convert the array back to a PIL Image object
    return Image.fromarray(np.uint8(img_array))


def histogram_stretch(image, low, high):
    img_array = np.array(image)
    # calculate the minimum and maximum values in the image array
    img_min = np.min(img_array)
    img_max = np.max(img_array)
    # apply the histogram stretch equation to the image array
    img_array = (img_array - img_min) * \
        ((high - low) / (img_max - img_min)) + low
    # clip the pixel values to the range [0, 255]
    img_array = np.clip(img_array, 0, 255)
    # convert the array back to a PIL Image object
    return Image.fromarray(np.uint8(img_array))


def histogram_shrink(image, low, high):
    img_array = np.array(image)
    # calculate the minimum and maximum values in the image array
    img_min = np.min(img_array)
    img_max = np.max(img_array)
    # apply the histogram shrink equation to the image array
    img_array = low + (high - low) * (img_array -
                                      img_min) / (img_max - img_min)
    # clip the pixel values to the range [0, 255]
    img_array = np.clip(img_array, 0, 255)
    # convert the array back to a PIL Image object
    return Image.fromarray(np.uint8(img_array))


filename = "1024x1024.png"
input_image = Image.open(filename)
input_image = input_image.convert("RGB")

a = float(input("Enter the value of a for the linear mapping equation: "))
b = float(input("Enter the value of b for the linear mapping equation: "))
c = float(input("Enter the value of c for the linear mapping equation: "))
d = float(input("Enter the value of d for the linear mapping equation: "))
gamma = float(
    input("Enter the value of gamma for the nonlinear mapping equation: "))
low = float(
    input("Enter the value of the lower end of the stretch/shrink range: "))
high = float(
    input("Enter the value of the upper end of the stretch/shrink range: "))
linear_mapped_image = linear_mapping(input_image, a, b, c, d)
nonlinear_mapped_image = nonlinear_mapping(input_image, gamma)
digital_negative_image = digital_negative(input_image)
histogram_stretched_image = histogram_stretch(input_image, low, high)
histogram_shrunk_image = histogram_shrink(input_image, low, high)
linear_mapped_image.save("linear_mapped.jpg")
nonlinear_mapped_image.save("nonlinear_mapped.jpg")
digital_negative_image.save("digital_negative.jpg")
histogram_stretched_image.save("histogram_stretched.jpg")
histogram_shrunk_image.save("histogram_shrunk.jpg")

print("All image processing functions have been applied successfully!")
