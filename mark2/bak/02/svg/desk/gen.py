import sys,re
id=None; d=None; a=[]
while True:
    s=sys.stdin.readline()
    if not s: break
    t=re.split(' |,|=',s.strip().replace('"','').replace('\t',''))
    if t[0]=='d' and t[1]=='M':
        d=[t[2],t[3]]
        for i in range(4,len(t),3):
            if t[i]=='Z': break
            elif t[i]=='L': d+=[t[i+1],t[i+2]]
            else: print(f'Error: {t}',file=sys.stderr)
    if t[0]=='id':
        try:
            id=int(t[1][1:])
        except:
            id=None
    if '/>' in t and id and d:
        a.append([id,d])
        id=None; d=None
a.sort()
print('},{ # CAM '+sys.argv[1] if sys.argv[1]!='1' else 'desk=({ # CAM 1')
for b in a:
    x0=2000;y0=2000;x1=0;y1=0;
    for i in range(len(b[1])//2):
        x=int(float(b[1][i*2  ])+0.5); x=1919 if x>1919 else x
        y=int(float(b[1][i*2+1])+0.5); y=1079 if y>1079 else y
        x0=x if x<x0 else x0; y0=y if y<y0 else y0;
        x1=x if x>x1 else x1; y1=y if y>y1 else y1;
    print(f'\t{b[0]}:(({x0},{y0},{x1+1},{y1+1}),',end='')
    for i in range(len(b[1])//2):
        x=int(float(b[1][i*2  ])+0.5); x=1919 if x>1919 else x
        y=int(float(b[1][i*2+1])+0.5); y=1079 if y>1079 else y
        print(f'({x-x0},{y-y0})',end=')' if i==(len(b[1])//2-1) else ',')
    print(',' if b!=a[-1] else '')
if sys.argv[1]=='6': print('})')
