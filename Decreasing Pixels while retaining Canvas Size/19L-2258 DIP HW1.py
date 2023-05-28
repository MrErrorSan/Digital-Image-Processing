from PIL import Image
import numpy as np
from statistics import mean

def reduce1024IMG(img,N):
     #triversing the image size to pixel size
     MaxSize=1024
     n=0
     divider=1
     if N ==512:
         n=2
         divider=4
     elif N==256:
          n=4
          divider=16
     elif N==128:
          n=8
          divider = 64
     elif N==64:
          n=16
          divider = 256
     elif N==32:
          n=32
          divider = 1024
     else:
          n=0
     if n!=0:
        #nested loops to triverse the image
        for i in range(0, MaxSize, n):
            for j in range(0, MaxSize, n):
                sum=0
                avg=0
                #nested loops to take average
                for x in range(0,n,1):
                        for y in range(0,n,1):
                            sum=sum+img[i+x][j+y]
                avg=sum/divider
                # nested loops to insert average in img
                for x in range(0, n, 1):
                    for y in range(0, n, 1):
                        img[i+x][j+y]=avg
     else:
         print("No Change is Done by Reduce Function")
     return img

# Load the image
#Enter image path here(Replace 1024x1024.png with the path of image)
image = Image.open('1024x1024.png').convert('L')
# Convert the image to a 2D array
img = np.array(image)
# Show the array
print("Orignal IMAGE of size 1024x1024\n")
print(img)

print("\nAfter Reduction To 512x512\n")
print(reduce1024IMG(img, 512))
img1 = Image.fromarray(reduce1024IMG(img, 512), 'L')
img1.save(f'512x512.png')

print("\nAfter Reduction To 256x256\n")
print(reduce1024IMG(img,256))
img1 = Image.fromarray(reduce1024IMG(img,256), 'L')
img1.save(f'256x256.png')

print("\nAfter Reduction To 128x128\n")
print(reduce1024IMG(img, 128))
img2 = Image.fromarray(reduce1024IMG(img, 128), 'L')
img2.save(f'128x128.png')

print("\nAfter Reduction To 64x64\n")
print(reduce1024IMG(img, 64))
img3 = Image.fromarray(reduce1024IMG(img, 64), 'L')
img3.save(f'64x64.png')

print("\nAfter Reduction To 32x32\n")
print(reduce1024IMG(img, 32))
img3 = Image.fromarray(reduce1024IMG(img, 32), 'L')
img3.save(f'32x32.png')
