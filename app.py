#Python libraries that we need to import for our bot
import random
import requests
import sys
from flask import Flask, request
from pymessenger.bot import Bot
#from pymessenger import Button

app = Flask(__name__)
ACCESS_TOKEN = 'EAACEdEose0cBAMwOUvSy5SsZCJ6JlMCSsCBSCXPss2bzpfdZCZAX6IBqY8ZBPGckASDZBFZCcpVZBZCITcGzAZAXF1WehE2oLpVJrUQqxlwPrMISmiqg2ydZBSbQHCe0vYZBnvZCV6q9sj9QYYgfyBZA61pR1lYZCT8njB3bNKG17308jcvoplrLsUXAMlZANHDFMxS4E3Er6sGip67SpXgrZChPyivr'
VERIFY_TOKEN = 'siwine'

bot=Bot(ACCESS_TOKEN)
url='https://cdn.pixabay.com/photo/2016/06/18/17/42/image-1465348_960_720.jpg'


#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
       
       
       get_started()
       greetings()
       output = request.get_json()
       log(output)
       for event in output['entry']:
          if 'messaging' in event:
              for message in event['messaging']:
                if 'message' in message:
                    #Facebook Messenger ID for user so we know where to send response back to
                    if message['message'].get('text'):
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
                        #send_buttons_case1(recipient_id)
                        #jbot.send_raw(payload) 
                        print('ok')
                        #if user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        #response_sent_nontext = get_message()
                        #send_message(recipient_id, response_sent_nontext)
                        print('attach')        
          elif 'postback' in event:
              if message['postback']['payload']=="GET STARTED":
                  send_message(recipient_id, 'welcome')
                    
            

    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Hello there'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!","cool", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"
	
def send_image(recipient_id, image_url):
	bot.send_image_url(recipient_id, image_url)
	return "sucess"

def send_quick_replies(recipient_id, image_url):
	#bot.send_image(recipient_id, image_url)
	return "sucess"   
def greetings():
    headers = {
        'Content-Type': 'application/json',
    }
    params = {
        'access_token': ACCESS_TOKEN,
    }
    payload={
      "greeting": [
        {
          "locale":"default",
          "text":"Hello!" 
        }, {
          "locale":"en_US",
          "text":"Timeless apparel for the masses."
        }
      ]
    }
    request_endpoint="https://graph.facebook.com/v2.6/me/messenger_profile?access_token="+ACCESS_TOKEN

    response = requests.post(url, headers=headers, params=params,
                             data=json.dumps(payload))
    response.raise_for_status()
    return response.json() 

def get_started():
    payload={
            "get_started": {"payload": "<postback_payload>"}
            }
    request_endpoint="https://graph.facebook.com/v2.6/me/messenger_profile?access_token="+ACCESS_TOKEN
    response = requests.post(request_endpoint,
                             json=payload)
    result = response.json()
    return result

def log(message):
	print(message)
	sys.stdout.flush()

if __name__ == "__main__":
    app.run()
