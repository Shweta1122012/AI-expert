import cv2
image=cv2.imread(r'C:\Users\Public\AI expert\lesson7\example.jpg')
grey_image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
resized=cv2.resize(grey_image,(224,224))
cv2.imshow('grey image',resized)
key=cv2.waitKey(0)
if key==ord('s'):
    cv2.imwrite(r'C:\Users\Public\AI expert\lesson7\grey_image.jpg',resized)
    print("image saved successfully")
else:
    print("image not saved")
cv2.destroyAllWindows()
print(f"Processed image dimensions: {resized.shape}")