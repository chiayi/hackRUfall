from flask import Flask, request, redirect
from twilio.rest import TwilioRestClient
import twilio.twiml
import thread
import time
from linkedList import ListOfNumbers
from linkedList import Node
from datetime import datetime

account_sid = 'ACfca27f35949a46c224e9b8e750146c2a'
auth_token = '938f8abd15429199a973bb65734d5848'

client = TwilioRestClient(account_sid, auth_token)

app = Flask(__name__)
book = ListOfNumbers()

def validTime(timeString):
	print(timeString)
	if(len(timeString) == 5):
		if(timeString[0:2].isdigit() and timeString[2] == ':' and timeString[3:].isdigit()):
			d = int(timeString[0:2])
			g =int(timeString[3:])
			if((d < 24) and (g < 60)):
				return 1
			
	if(len(timeString) == 4):
		if(timeString[0].isdigit() and timeString[1] == ':'and timeString[2:4].isdigit()):
			if(int(timeString[2:4]) < 60):
				return 1

	return 0


@app.route("/", methods=['GET', 'POST'])
def recievedmsg():
  """Respond to incoming calls with a simple text message.""" 
  resp = twilio.twiml.Response()
  txt = request.form['Body']
  phoneNum = request.form['From']

  lists = txt.split()

  if(validTime(str(lists[0])) != 1):
  	message = client.messages.create(to=phoneNum, from_='+17322534191',body="Reminder must be in form of \'hh:mm Message\' (24 hour clock)")
  	return str(resp)

  todayTime = datetime.today()
  time_ = datetime.strptime(str(todayTime.year) + str(todayTime.month) + str(todayTime.day) + lists[0], '%Y%m%d%H:%M')

  msg = txt[len(lists[0])+1:]
  
  book.add(phoneNum,msg,time_)
  book.printList()
  message = client.messages.create(to=phoneNum, from_='+17322534191',body="Reminder for " + msg + " at " + str(time_) + " has been received")
  return str(resp)

def checkBook(threadName,delay):
	while(True):
		curNode = book.getFirst()
		if(curNode != None):
			curTime = datetime.today()
			firstTime = curNode.timeToText

			difference = firstTime - curTime

			print("Next time: " + str(difference))

			if(difference.seconds < 600 or difference.days < 0):
				reminderMsg = None
				if(difference.days < 0):
					reminderMsg = 'It\'s a little late to be having a remind now'
				else:
					reminderMsg = 'Reminder: ' + curNode.msg + ' at ' + str(curNode.timeToText)
				message = client.messages.create(to=curNode.phoneNum, from_='+17322534191',body=reminderMsg)
				book.removeFirst();

		time.sleep(delay)



#  while app.run:
# schedule.run_pending()
# time.sleep(5)

try:
	thread.start_new_thread(checkBook,("SUP", 5))
except:
	print ("RIP")

if __name__ == "__main__":

	app.run(debug=True)
