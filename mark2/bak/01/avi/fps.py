import os,sys,cv2

f1=cv2.VideoCapture('0416_1200.avi')
f0=cv2.VideoWriter('new.avi',cv2.VideoWriter_fourcc(*'XVID'),1.0,(1920,180))

n=0
while f1.isOpened():
    ok,img=f1.read()
    if not ok: break
    img=img[0:180,0:1920]
    f0.write(img)
    n+=1
    print(f'{n}\r',end='',flush=True)
f0.release()
f1.release()
