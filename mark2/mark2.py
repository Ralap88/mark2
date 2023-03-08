
import cv2, math, os, sys, time
import numpy as np
import data

# ----------------------------------------------------------------
# globals

desk_limit  = 30        # 15 minutes (15*60/30fps)
dx          = 210       # jpg position on the frame
dy          = 280
start_time  = 12*60*60  # in seconds

# null desk images input
null = []
null_cap = cv2.VideoCapture('avi/null.avi')
for i in range(6):
    ok,img = null_cap.read()
    null.append(cv2.cvtColor(img,cv2.COLOR_BGR2GRAY))
null_cap.release()

# input videos (-180 and -30s) and jpg
cap = []
cap.append(cv2.VideoCapture('avi/0416_1200-b.avi'))
for i in range(6): cap.append(cv2.VideoCapture(f'avi/0416_cam{i+1}_1200-30s.avi'))
jpg = cv2.imread('avi/library.jpg')

# output frame
frame_cnt = 0
frame = np.ones((1080,1920,3),dtype=np.uint8)*255

# work variables
seat_timer = [0]*103
desk_timer = [0]*103
seat_empty = [True]*103
desk_empty = [True]*103
seat_counter = [0]*103

# ----------------------------------------------------------------
# seat

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

# return the seat that has max iom (>0.7) with rect, return -1 if none
def check_seat(cam, rect):
    try: rect = (rect[0],rect[1],rect[0]+rect[2],rect[1]+rect[3])
    except: return -1
    v = [0,0]
    for s in data.seat[cam]:
        u = iom(rect, s[1:5])
        if u > v[0]: v = [u,s[0]-1]
    return v[1] if v[0]>0.7 else -1

# ----------------------------------------------------------------
# desk

# return true if desk does not touch all boxes
def check_desk_free(cam,n):
    global frame_cnt
    x1 = data.desk[cam][n+1][0]
    for x in data.box[cam][frame_cnt]:
        x2 = (x[0],x[1],x[0]+x[2],x[1]+x[3])
        if iom(x1,x2)> 0.25: return False
    return True

# return true if desk similar to null desk
def check_desk_empty(img1,img2,cut):
    x0,y0,x1,y1=cut[0];

    img1=img1[y0:y1,x0:x1]
    img2=img2[y0:y1,x0:x1]

    mask=np.zeros(img1.shape,dtype=np.uint8)
    cv2.fillPoly(mask,np.array([cut[1:]]),[255])

    img1=cv2.bitwise_and(img1,mask)
    img2=cv2.bitwise_and(img2,mask)
    
    img1=cv2.Canny(img1,100,300)
    img2=cv2.Canny(img2,100,300)

    img = cv2.absdiff(img1,img2)

    ret,th = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY )
    dilated = cv2.dilate(th, None, iterations=1)
    contours,_ = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    for c in contours:
        area= cv2.contourArea(c)
        if area>1000: return False
    return True

# ----------------------------------------------------------------
# generate frame

def gen_frame():
    global frame_cnt
    frame_cnt += 1

    # setup frame
    ok,frame_top = cap[0].read()
    if not ok:
        for i in range(7): cap[i].set(1,0) # rewind all
        frame_cnt = 0
        return 

    frame[40:220,0:1920]=frame_top
    frame[dy:dy+800,dx:dx+1510]=jpg

    # time display
    frame[984:1020,1740:1848]=256-32
    n=start_time+frame_cnt
    s = f'{n//3600:2}:{n%3600//60:02}:{n%3600%60:02}'
    cv2.putText(frame, s, (1750,1010), cv2.FONT_HERSHEY_SIMPLEX,
        0.6, (255,255,255), 1, cv2.LINE_AA)

    # check seat
    try:
        for cam in range(6):
            for x in data.box[cam][frame_cnt]:
                i = check_seat(cam,x)
                if i>=0: seat_counter[i] += 1
    except:
        for i in range(7): cap[i].set(1,0) # rewind all
        frame_cnt = 0
        return 

    # update_30
    if frame_cnt%30==0:
        update_30()
        print(f'\r{frame_cnt}',end='',flush=True)

# ----------------------------------------------------------------
# update jpg every 30 seconds

def update_30():
    # seat empty check
    for n in range(103):
        seat_empty[n] = seat_counter[n] < 15
        seat_counter[n] = 0

    # desk empty check
    for cam in range(6):
        img1 = null[cam]
        ok,img2 = cap[cam+1].read()
        img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
        for n in range(103):
            if not seat_empty[n]: desk_empty[n] = True; continue
            if not desk_empty[n]: continue
            if n+1 not in data.desk[cam]: continue
            if not check_desk_free(cam,n): continue
            desk_empty[n] = check_desk_empty(img1,img2,data.desk[cam][n+1])

    # timers
    for n in range(103):
        if seat_empty: seat_timer[n]=0
        else: seat_timer[n]+=1
        if not seat_empty[n] or desk_empty[n]: desk_timer[n]=0
        else: desk_timer[n]+=1

    # update status on jpg
    for n in range(103):
        p1=(data.fill[n][0], data.fill[n][1]+1);
        p2=(data.fill[n][2], data.fill[n][3]-1)

        if not seat_empty[n]:
            cv2.rectangle(jpg, p1,p2, (255,192,160),-1)
        elif not desk_empty[n]:
            if desk_timer[n]>desk_limit:
                cv2.rectangle(jpg, p1,p2, (0,0,255),-1)
            else:
                cv2.rectangle(jpg, p1,p2, (192,160,255),-1)
        else:
            cv2.rectangle(jpg, p1,p2, (255,255,255),-1)

        x = (p1[0]+p2[0])//2-5
        x = x-14 if n>=99 else x-7 if n>=9 else x
        cv2.putText(jpg, str(n+1), (x,(p1[1]+p2[1])//2+7), cv2.FONT_HERSHEY_SIMPLEX,
            0.6, (0,0,0), 1, cv2.LINE_AA)

    # text value display
    s=['','','']
    for n in range(103):
        if not seat_empty[n]:
            if s[0]: s[0]+=', '
            s[0]+=str(n+1)
        elif not desk_empty[n]:
            if desk_timer[n]>desk_limit:
                if s[2]: s[2]+=', '
                s[2]+=str(n+1)
            else:
                if s[1]: s[1]+=', '
                s[1]+=str(n+1)
    for i in range(3):
        jpg[630+i*37:666+i*37,180:1455]=255
        cv2.putText(jpg, s[i], (185,642+i*37), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,0), 1, cv2.LINE_AA)

# ----------------------------------------------------------------
# flask mode

from flask import Flask, render_template, Response
import time, cv2

app = Flask(__name__)
def flask_frame():
    while True:
        gen_frame()
        ret, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        if frame_cnt%30!=0: time.sleep(1)

@app.route('/video_feed')
def video_feed():
    return Response(flask_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

if len(sys.argv)>1:
    app.run(host='0.0.0.0')

if len(sys.argv)>1:
    exit()

# ----------------------------------------------------------------
# movie maker mode

avi = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc(*'XVID'),1.0,(1920,1080))
cv2.namedWindow('mark2_frame',cv2.WINDOW_NORMAL)
cv2.setWindowProperty('mark2_frame',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

while True:
    gen_frame()
    if frame_cnt==0: break
    avi.write(frame)
    cv2.imshow('mark2_frame',frame)
    k=cv2.waitKey(1)
    if k==27: break
    elif k==32:
        while cv2.waitKey(200)!=32: pass

