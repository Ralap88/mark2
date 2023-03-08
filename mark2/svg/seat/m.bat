python gen.py 1 < cam1.svg > ..\seat.py
python gen.py 2 < cam2.svg >> ..\seat.py
python gen.py 3 < cam3.svg >> ..\seat.py
python gen.py 4 < cam4.svg >> ..\seat.py
python gen.py 5 < cam5.svg >> ..\seat.py
python gen.py 6 < cam6.svg >> ..\seat.py
cd ..
copy desk.txt+desk.py+seat.txt+seat.py+tail.py ..\data.py
echo # >> ..\data.py
cd seat
