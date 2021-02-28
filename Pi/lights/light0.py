import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(15, GPIO.OUT)

GPIO.output(15, GPIO.LOW)
print("Light turned off!!!")


print("Light turned on!!")
file = open("lstat.txt", "w")
file.write("off")
file.close()
#os.system("sshpass -p 'itunesfansbyapple' ssh raghav@thinkpad.local 'rm -f /home/raghav/Hackathons/HackTU/iOT/Hub/lstat.txt'")
#os.system("sshpass -p 'itunesfansbyapple' scp /home/pi/Pi/lights/lstat.txt raghav@thinkpad.local:/home/raghav/Hackathons/HackTU/iOT/Hub/ ")


