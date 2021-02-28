from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import time
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


from datetime import datetime
import os

authorised_ids = []

def audioGen(message):
	os.system("rm -f message.mp3")
	authenticator = IAMAuthenticator('<IBM WATSON TEXT TO SPEECH API KEY>')
	text_to_speech = TextToSpeechV1(
    		authenticator=authenticator
	)
	text_to_speech.set_service_url('<IBM WATSON TEXT TO SPEECH URL')
	
	with open('message.mp3', 'wb') as audio_file:
		audio_file.write(text_to_speech.synthesize(message,accept='audio/mp3').get_result().content)
	#os.system("ffmpeg -i message.wav -acodec mp3 message.mp3")
	#os.system("rm -f message.wav")
def authorisation(user):
	if user['id'] in authorised_ids:
		print("Access granted")
		return True
	else:
		print("Access denied")
		return False

def start(update, context):
	user = update.message.from_user
	print(user)
	if authorisation(user):
		update.message.reply_text("Welcome {}".format(user['first_name']+' '+'!'))
	else:
		update.message.reply_text("Access denied")
def lightOn(update, context):
	os.system("sshpass -p 'RPI4 PASSWD' ssh pi@test-bench-pi.local 'python3 /home/pi/Pi/lights/light1.py'")
	update.message.reply_text("Light turned on!")
def lightOff(update, context):
	os.system("sshpass -p 'RPI4 PASSWD' ssh pi@test-bench-pi.local 'python3 /home/pi/Pi/lights/light0.py'")
	update.message.reply_text("Light turned off!!")
def message(update, context):
	arguments = context.args
	message = ""
	for word in arguments:
		message = message + word
	
	print(context.args)
	audioGen(message)
	os.system("mpg123 message.mp3")
def dnd(update, context):
	if(len(context.args) == 0):
		update.message.reply_text("Please type on or off")
	else:
		os.system("sshpass -p 'RPI4 PASSWD' ssh pi@test-bench-pi.local 'rm -f /home/raghav/Documents/Hackathons/HackTU/iOT/Pi/DND.txt'")
		file = open("/home/raghav/Documents/Hackathons/HackTU/iOT/Pi/DND.txt", 'w')
		if(context.args[0] == 'on'):
			file.write('on')
			update.message.reply_text("DND mode turned on")
		else:
			update.message.reply_text("DND mode turned off")
			file.write('off')
		file.close()
		os.system("sshpass -p 'RPI4 PASSWD' scp /home/raghav/Documents/Hackathons/HackTU/iOT/Pi/DND.txt pi@test-bench-pi.local:/home/pi/Pi")
		os.system("rm -f /home/raghav/Documents/Hackathons/HackTU/iOT/Pi/DND.txt")
def takePhoto(update, context):
	date = datetime.now()
	file_name = date.strftime("%d_%m_%Y__%H_%M_%S") + ".jpg"
	command = "ffmpeg -y -i rtsp://admin:<IP CAM PASSWD>@192.168.8.123:8080/h264_ulaw.sdp -q:v 1 -vframes 1 "+'shots/'+file_name
	os.system(command)
	context.bot.send_photo(update.message.from_user['id'], photo=open('shots/'+file_name, 'rb'))

def fillAuth():
	auth_file = open("authID.txt")
	ids = auth_file.readlines()
	for id in ids:
		authorised_ids.append(int(id))

	print(authorised_ids)
def flash(update, context):
	os.system("sshpass -p 'RPI4 PASSWD' ssh pi@test-bench-pi.local 'python3 /home/pi/Pi/lights/light0.py'")
	count = 0
	if (len(context.args) == 0):
		update.message.reply_text("Please type the number of times you want the light to flash")
	else:
		number = int(context.args[0])
		os.system("sshpass -p 'RPI4 PASSWD' ssh pi@test-bench-pi.local 'python3 /home/pi/Pi/lights/flash.py '" + str(number))
def main():
	updater = Updater("BOT ID", use_context=True)
	dispatcher = updater.dispatcher

	dispatcher.add_handler(CommandHandler("start", start))
	dispatcher.add_handler(CommandHandler("status", takePhoto))
	dispatcher.add_handler(CommandHandler("message", message))
	dispatcher.add_handler(CommandHandler("dnd", dnd))
	dispatcher.add_handler(CommandHandler("lumos", lightOn))
	dispatcher.add_handler(CommandHandler("nox", lightOff))
	dispatcher.add_handler(CommandHandler("flash", flash))
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	fillAuth()
	main()
