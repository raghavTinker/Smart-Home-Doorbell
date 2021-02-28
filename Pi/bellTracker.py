import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import os
import time

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering

GPIO.setup(23, GPIO.IN)
#GPIO.setup(11, GPIO.OUT)

while True:
	file = open("DND.txt")
	if (GPIO.input(23) == 0):
		print("the bell was pressed")
		nu = file.read()
		print(nu)
		if(nu == 'off'):
			file.seek(0)
			os.system("sshpass -p '<hub paswd>' ssh <user>@<hostname> 'DISPLAY=:0 mpg123 /home/raghav/Documents/Hackathons/HackTU/iOT/Hub/bell.mp3'")
			os.system("sshpass -p '<hub paswd>' ssh <user>@<hostname> 'DISPLAY=:0 mpg123 /home/raghav/Documents/Hackathons/HackTU/iOT/Pi/hello.mp3'")
			os.system("sshpass -p '<hub paswd>' ssh <user>@<hostname> 'python3 /home/raghav/Documents/Hackathons/HackTU/iOT/Hub/sendPhoto.py'")
		else:
			file.seek(0)
			
			print("dont play")
			os.system("sshpass -p '<hub paswd>' ssh <user>@<hostname> 'DISPLAY=:0 mpg123 /home/raghav/Documents/Hackathons/HackTU/iOT/Pi/unavailable.mp3'")
			os.system("sshpass -p '<hub paswd>' ssh <user>@<hostname> 'python3 /home/raghav/Documents/Hackathons/HackTU/iOT/Hub/sendPhoto.py'")
		file.close()
	else:
		time.sleep(2)
		file.close()
		continue
