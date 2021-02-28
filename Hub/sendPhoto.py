#!/usr/bin/env python3

#This file sends the photo via telegram

import telegram
from datetime import datetime
import os
import time
auth_ids = []
bot = telegram.Bot("BOT ID")

def fillId():
	auth_f = open("/home/raghav/Documents/Hackathons/HackTU/iOT/Hub/authID.txt")
	ids = auth_f.readlines()
	for id in ids:
		auth_ids.append(int(id))

def takePhoto():
	date = datetime.now()
	file_name = date.strftime("%d_%m_%Y__%H_%M_%S") + ".jpg"
	command = "ffmpeg -y -i rtsp://admin:<CAM PASSWD>@192.168.8.123:8080/h264_ulaw.sdp -q:v 1 -vframes 1 "+'/home/raghav/Documents/Hackathons/HackTU/iOT/Hub/shots/'+file_name

	os.system(command)
	for chat_id in auth_ids:
		bot.send_photo(chat_id, photo=open('/home/raghav/Documents/Hackathons/HackTU/iOT/Hub/shots/' + file_name, 'rb'))
		bot.send_message(chat_id, "Someone is at the door! Please check!!")
		time.sleep(5)


fillId()
takePhoto()
print("MESSAGE SENT   OVER")
