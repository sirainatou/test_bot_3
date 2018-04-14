#Python libraries that we need to import for our bot
import random
import requests
import sys
import json
from flask import Flask, request
from pymessenger.bot import Bot
#from pymessenger import Button

app = Flask(__name__)
ACCESS_TOKEN = 'EAAFVAFt33ZAsBAG9zLlkMehDcX29SaYL8lcnVSydGr5RzGAtfKYZBRmRO8eX3PSRJpLKfJgDl3I2y9V9MdZBlnLj24rEzTx9T01GMW6P83UQkFEUK0KGrczDkgth7XW1ZB8ZBJxObV0WJSu6l38yzHGQ0hZAvhfq2a44Y9ZCERghwZDZD'
VERIFY_TOKEN = 'siwine'
headers = {
        'Content-Type': 'application/json',
          }

bot=Bot(ACCESS_TOKEN)


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
               messaging = event['messaging']
               for message in messaging:
                   recipient_id=message ['sender']['id']
                   if 'message' in message:
                       if message['message'].get('text'):
			    if message['message'].get('text')=="-2"
			    	send_message(recipient_id, "mmmm ok")
			    else 
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
                   elif 'postback' in message:
                       if message['postback']['payload']=="GET_STARTED":
                           send_message(recipient_id, "welcome")
                           send_quick_replies(recipient_id)

           elif 'standby' in event: 
               pass
                    
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
def send_quick_replies(recipient_id):
    payload={
            "recipient":{
                    "id":recipient_id
                        },
            "message":{
                    "text": "Here is a quick reply!",
                    "quick_replies":[
                            {
                            "content_type":"text",
                            "title":"Search",
                            "payload":"<POSTBACK_PAYLOAD>",
                            "image_url":"http://example.com/img/red.png"
                            },
                            {
                            "content_type":"location"
                            }
                    ]
            }
    }
    request_endpoint="https://graph.facebook.com/v2.6/me/messages?access_token="+ACCESS_TOKEN
    response = requests.post(request_endpoint,headers=headers,
                             data=json.dumps(payload))
    result = response.json()
    return result
	
def send_image(recipient_id, image_url):
	bot.send_image_url(recipient_id, image_url)
	return "sucess"
  
def get_started():

    payload={
            #"get_started": {"payload": "<postback_payload>"}
            'message': json.dumps( {"postback": {"payload": "GET_STARTED"}})
            }
    request_endpoint="https://graph.facebook.com/v2.6/me/messenger_profile?access_token="+ACCESS_TOKEN
    response = requests.post(request_endpoint,headers=headers,
                             data=json.dumps(payload))
    result = response.json()
    return result

def greetings():
    payload={
      "greeting": [
        {
          "locale":"default",
          "text":"Hello :) {{user_first_name}} <3 " 
        }, {
          "locale":"en_US",
          "text":"Timeless apparel for the masses."
        }
      ]
    }
    request_endpoint="https://graph.facebook.com/v2.6/me/messenger_profile?access_token="+ACCESS_TOKEN

    response = requests.post(request_endpoint, headers=headers,
                             data=json.dumps(payload))
    print(response)
    response.raise_for_status()
    return response.json() 


def log(message):
	print(message)
	sys.stdout.flush()

if __name__ == "__main__":
    app.run()
