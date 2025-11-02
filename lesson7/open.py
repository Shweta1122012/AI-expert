import cv2
image=cv2.imread(r'C:\Users\Public\AI expert\lesson7\example.jpg')
cv2.namedWindow('Image Window',cv2.WINDOW_NORMAL)
cv2.resizeWindow('Image Window',600,400)
cv2.imshow('Image Window',image)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(f"Image dimensions: {image.shape}")