import cv2, sys

if len(sys.argv)<3:
    print('Usage: get cam? mm:ss')
    exit()

try:
    cam=int(sys.argv[1][3])
    mm=int(sys.argv[2][0:2])
    ss=int(sys.argv[2][3:5])
except:
    print('Usage: get cam? mm:ss')
    exit()

avi=cv2.VideoCapture(f'0416/0416_cam{cam}_1200-b.avi')
avi.set(1,mm*60+ss)
ok,img=avi.read()
cv2.imwrite(f'cam{cam}-{mm:02}-{ss:02}.jpg',img)
