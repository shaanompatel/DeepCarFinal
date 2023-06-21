import cv2

frame0 = cv2.VideoCapture(0)
frame0.set(3,160)
frame0.set(4,120)

frame1 = cv2.VideoCapture(2)
#frame1.set(3,160)
#frame1.set(4,120)

while 1:

   ret0, img1 = frame0.read()
   ret1, img2 = frame1.read()
   #img1 = cv2.resize(img0,(360,240))
   #img2 = cv2.resize(img00,(360,240))
   if (frame0):
       cv2.imshow('img1',img1)
   if (frame1):
       cv2.imshow('img2',img2)

   k = cv2.waitKey(30) & 0xff
   if k == 27:
      break

frame0.release()
#frame1.release()
cv2.destroyAllWindows()