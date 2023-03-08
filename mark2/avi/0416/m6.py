import sys, cv2, numpy
import numpy as np

sys.path.append('..')
import data

cam=1
if len(sys.argv)>1:
    cam=int(sys.argv[1])

# intersection over min
def iom(rec1, rec2):
    # find the each edge of intersect rectangle
    left_line = max(rec1[1], rec2[1])
    right_line = min(rec1[3], rec2[3])
    top_line = max(rec1[0], rec2[0])
    bottom_line = min(rec1[2], rec2[2])
 
    # judge if there is an intersect
    if left_line >= right_line or top_line >= bottom_line: return 0
    else:
        # computing area of each rectangles
        s1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
        s2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])
 
        intersect = (right_line - left_line) * (bottom_line - top_line)
        # return intersect / (s1 + s2 - intersect) # iou
        return intersect / min(s1,s2) # iom

frame_cnt=0
frame=np.ones((180,1920,3),np.uint8)*255

avi=[]
for cam in range(1,7):
    avi.append(cv2.VideoCapture(f'0416_cam{cam}_1200-1.avi'))
avi.append(cv2.VideoWriter('0416_1200-b.avi',cv2.VideoWriter_fourcc(*'XVID'),1.0,(1920,180)))

while True:
    for cam in range(6):
        for _ in range(4): avi[cam].read()
        ok,img=avi[cam].read()
        img=cv2.resize(img,(304,171), interpolation=cv2.INTER_AREA)

        try:
            for x in data.box[cam][frame_cnt]:
                r=[x[0],x[1],x[0]+x[2],x[1]+x[3]]
                for i in range(0,4,2):
                    r[i  ]=r[i  ]*304//1920
                    r[i+1]=r[i+1]*171//1080
                cv2.rectangle(img,(r[0],r[1]),(r[2],r[3]),(0,255,0),1)
        except:
            pass

        try:
            for x1 in data.seat[cam]:
                c=(0,0,255)
                for x2 in data.box[cam][frame_cnt]:
                    r = (x2[0],x2[1],x2[0]+x2[2],x2[1]+x2[3])
                    if iom(x1[1:],r)>0.7: c=(0,255,255); break
                r=[0,0,0,0]
                for i in range(0,4,2):
                    r[i  ]=x1[i+1]*304//1920
                    r[i+1]=x1[i+2]*171//1080
                cv2.rectangle(img,(r[0],r[1]),(r[2],r[3]),c,1)
        except:
            pass

        frame[4:175,38+308*cam:38+308*(cam+1)-4]=img

    '''
    cv2.imshow('avi',frame)
    k=cv2.waitKey(1)
    if k==27: break
    '''
    avi[6].write(frame)

    frame_cnt+=1; print(f'\r{frame_cnt}  ',end='')
    if frame_cnt>3600: break

