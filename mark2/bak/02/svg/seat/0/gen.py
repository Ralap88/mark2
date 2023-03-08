import sys,data
for s in data.cam_seat[int(sys.argv[1])-1]:
    print('<rect style="fill:none;stroke:#000000;stroke-width:1;stroke-opacity:1;stroke-miterlimit:4;stroke-dasharray:none"')
    print(f'id="r{s[0]}" ',end='')
    print(f'x="{s[1]}" ',end='')
    print(f'y="{s[2]}" ',end='')
    print(f'width="{s[3]-s[1]}" ',end='')
    print(f'height="{s[4]-s[2]}" />')
print('</g></svg>')
