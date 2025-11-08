import cv2
import matplotlib.pyplot as plt

image=cv2.imread(r"c:\Users\Public\AI expert\lesson8\AIEPCM2L2 Activities Boilerplate code\example.jpg")
rgb_image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
plt.imshow(rgb_image)
plt.title("RGB IMAGE")
plt.show()
grey_image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
plt.imshow(grey_image,cmap='gray')
plt.title("GREY IMAGE")
plt.show()
cropped_image=image[100:300,200:400]
cropped_rgb=cv2.cvtColor(cropped_image,cv2.COLOR_BGR2RGB)
plt.imshow(cropped_rgb)
plt.title("CROPPED IMAGE")
plt.show()




