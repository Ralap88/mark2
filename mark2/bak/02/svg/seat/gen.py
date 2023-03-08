import sys,re
id=None; d=None; a=[]; rect=False
XMAX=1920-1; YMAX=1080-1
while True:
    s=sys.stdin.readline()
    if not s: break
    t=re.split(' |,|=',s.strip().replace('"','').replace('\t',''))
    if t[0]=='<rect': rect=True
    elif rect:
        if t[0]=='x': x=int(float(t[1])+0.5)
        if t[0]=='y': y=int(float(t[1])+0.5)
        if t[0]=='width': w=int(float(t[1])+0.5)
        if t[0]=='height': h=int(float(t[1])+0.5)
        if t[0]=='id': id=int(t[1][1:])
        if '/>' in t:
            xx=XMAX if (x+w)>XMAX else x+w
            yy=YMAX if (y+h)>YMAX else y+h
            if x<0: x=0
            if y<0: y=0
            a.append([id,x,y,xx,yy])
            rect=False
a.sort()
print('),( # CAM '+sys.argv[1] if sys.argv[1]!='1' else 'seat=(( # CAM 1')
for b in a:
    print(f'{"":4}(',end='')
    for c in b:
        print(f'{c}',end=',' if c!=b[-1] else '')
    print(')',end=',\n' if b!=a[-1] else '\n')
if sys.argv[1]=='6': print('))')
