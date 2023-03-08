import sys, cv2, numpy
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

avi1=cv2.VideoCapture(f'0416_cam{cam}_1200-1.avi')
avi0=cv2.VideoWriter(f'0416_cam{cam}_1200-b.avi',cv2.VideoWriter_fourcc(*'XVID'),1.0,(1920,1080))
print(f'0416_cam{cam}_1200-b.avi')
n=0

while True:
    for _ in range(4): avi1.read()
    ok,img=avi1.read()

    try:
        for x in data.box[cam-1][n]:
            cv2.rectangle(img,(x[0],x[1]),(x[0]+x[2],x[1]+x[3]),(0,255,0),2)
    except:
        pass

    try:
        for x1 in data.seat[cam-1]:
            c=(0,0,255)
            for x2 in data.box[cam-1][n]:
                rect = (x2[0],x2[1],x2[0]+x2[2],x2[1]+x2[3])
                if iom(x1[1:],rect)>0.7: c=(0,255,255); break
            cv2.rectangle(img,(x1[1],x1[2]),(x1[3],x1[4]),c,2)
    except:
        pass

    n+=1; print(f'\r{n}',end='')
    if n>=3600: break

    '''
    cv2.imshow('avi',img)
    k=cv2.waitKey(1)
    if k==27: break
    '''
    avi0.write(img)
