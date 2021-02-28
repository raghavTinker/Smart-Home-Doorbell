import sys
import time
import os
number = int(sys.argv[1])


count = 0

while count < number:
	os.system("python3 /home/pi/Pi/lights/light1.py")
	time.sleep(1)
	os.system("python3 /home/pi/Pi/lights/light0.py")
	time.sleep(1)
	count = count + 1
