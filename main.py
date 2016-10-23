from flask import Flask, request, redirect
import twilio.twiml
from linkedList import ListOfNumbers
from datetime import datetime

app = Flask(__name__)
book = ListOfNumbers()

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
  """Respond to incoming calls with a simple text message.""" 
  resp = twilio.twiml.Response()
  txt = request.form['Body']
  phoneNum = request.form['From']
  lists = txt.split()

  time = datetime.strptime(lists[0], '%H:%M')
  msg = txt[len(lists[0])+1:]
  
  book.add(phoneNum,msg,time)
  book.printList()
  return str(resp)

if __name__ == "__main__":
   app.run(debug=True)
