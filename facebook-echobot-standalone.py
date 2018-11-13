"""
Simple Facebook Echo bot: Respond with exactly what it receives
Standalone version
"""
from __future__ import unicode_literals
import sys, json, traceback, requests
from flask import Flask, request
from Utils import NLP
from pattern.en import parsetree, singularize


noun_phrases_remember = ""
application = Flask(__name__)
app = application
PAT = 'EAADfGuSGJJEBAEBhc9sXjkGZArKohFKUpfWXwMQxgU7NeLZBEm5ZBDJfnkIVWQHuXv5mkLfJpZB1aIye1ZB3kjTu0ZCdOqzZA0w98fZAHwicsppfAeTwDZBZCa9o6MzL0tE2TcwfG25JqJZA6Bbdj9eMv8K33NSea4W7FDjaWWUNmq7WgZDZD'
VERIFICATION_TOKEN = '3012'

@app.route('/', methods=['GET'])
def handle_verification():
    print "Handling Verification."
    if request.args.get('hub.verify_token', '') == VERIFICATION_TOKEN:
        print "Webhook verified!"
        return request.args.get('hub.challenge', '')
    else:
        return "Wrong verification token!"

# ======================= Bot processing ===========================
@app.route('/', methods=['POST'])
def handle_messages():
    payload = request.get_data()

    # Handle messages
    for sender_id, message in messaging_events(payload):
        # Start processing valid requests
        try:
            response = processIncoming(sender_id, message)
            if response != "send alr":
                if response is not None:
                    send_message(PAT, sender_id, response)
                else:
                    send_message(PAT, sender_id, "Sorry I don't understand that")

        except Exception, e:
            print e
            traceback.print_exc()
    return "ok"

def processIncoming(user_id, message):
    global noun_phrases_remember
    if message['type'] == 'text':
        message_text = message['data']
        if message_text[-1] != ".": # help separate sentence for parsetree
            dotted_message = message_text + "."
        s = parsetree(dotted_message, relations=True, lemmata=True)
        sentence = s[0]

        if NLP.isGreetings(message_text):
            return "Hey whassup? How can I help you?"

        elif NLP.isAskingBotInformation(message_text):
            return NLP.handleBotInfo(message_text)

        elif NLP.isAskingRestaurant(sentence, message_text):
            rest_data, noun_phrases_remember = NLP.handle_find_rest(sentence)
            if rest_data == None:
                return "Can you send me your location? :D"
            elif len(rest_data) == 0:
                return "No result found, sorry :("
            else:
                send_yelp_results(PAT, user_id, rest_data['businesses'])
                return 'send alr'

        elif NLP.isGoodbye(message_text):
            noun_phrases_remember = ""
            return "Goodbye!!!"

        return "I don't understand this ._."

    elif message['type'] == 'location':

        rest_data = NLP.handle_location(noun_phrases_remember, message['data'])
        if len(rest_data) == 0:
            return "No result found, sorry :("
        else:
            send_yelp_results(PAT, user_id, rest_data['businesses'])
            noun_phrases_remember = ""
            return 'send alr'

        return "Hmm..."

    # Unrecognizable incoming, remove context and reset all data to start afresh
    else:
        noun_phrases_remember = ""
        return "*scratch my head*"


def send_message(token, user_id, text):
    """Send the message text to recipient with id recipient.
    """
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=json.dumps({
                          "recipient": {"id": user_id},
                          "message": {"text": text.decode('unicode_escape')}
                      }),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text


def send_yelp_results(token, user_id, businesses):
    options = []

    for business in businesses:
        subtitle = ""
        if 'price' in business and business['price'] != "":
            subtitle += business['price'] + " - "
        subtitle += business['location']['address1']
        if 'distance' in business:
            subtitle += " (" + str(round(business['distance'], 1)) + " meters)"
        if 'is_open_now' in business:
            subtitle += "\n" + "Open now - " if business['is_open_now'] else "\n"
        if 'hours_today' in business and len(business['hours_today']) > 0:
            subtitle += "Hours today: %s"%(business['hours_today'])
        subtitle += "\n" + business['categories'][0]['title']

        img_url = business['image_url'] if business['image_url'] != "" else url_for('static', filename='assets/img/empty-placeholder.jpg', _external=True)

        obj = {
                "title": business['name'] + " - " + str(business['rating']) ,
                "image_url": img_url,
                "subtitle": subtitle,
                "buttons":[
                    {
                    "type":"web_url",
                    "url": business['url'],
                    "title":"View details"
                    }

                ]
                }
        options.append(obj)
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=json.dumps({
                            "recipient": {"id": user_id},
                            "message":{
                                "attachment":{
                                    "type":"template",
                                    "payload":{
                                        "template_type":"generic",
                                        "elements": options
                                    }
                                }
                            }
                      }),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text

# Generate tuples of (sender_id, message_text) from the provided payload.
# This part technically clean up received data to pass only meaningful data to processIncoming() function
def messaging_events(payload):

    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"]

    for event in messaging_events:
        sender_id = event["sender"]["id"]

        # Not a message
        if "message" not in event:
            yield sender_id, None

        # Pure text message
        if "message" in event and "text" in event["message"] and "quick_reply" not in event["message"]:
            data = event["message"]["text"].encode('unicode_escape')
            yield sender_id, {'type':'text', 'data': data, 'message_id': event['message']['mid']}

        # Message with attachment (location, audio, photo, file, etc)
        elif "attachments" in event["message"]:

            # Location
            if "location" == event['message']['attachments'][0]["type"]:
                coordinates = event['message']['attachments'][
                    0]['payload']['coordinates']
                latitude = coordinates['lat']
                longitude = coordinates['long']

                yield sender_id, {'type':'location','data':[latitude, longitude],'message_id': event['message']['mid']}

            # Audio
            elif "audio" == event['message']['attachments'][0]["type"]:
                audio_url = event['message'][
                    'attachments'][0]['payload']['url']
                yield sender_id, {'type':'audio','data': audio_url, 'message_id': event['message']['mid']}

            else:
                yield sender_id, {'type':'text','data':"I don't understand this", 'message_id': event['message']['mid']}

        # Quick reply message type
        elif "quick_reply" in event["message"]:
            data = event["message"]["quick_reply"]["payload"]
            yield sender_id, {'type':'quick_reply','data': data, 'message_id': event['message']['mid']}

        else:
            yield sender_id, {'type':'text','data':"I don't understand this", 'message_id': event['message']['mid']}

# Allows running with simple `python <filename> <port>`
if __name__ == '__main__':
    if len(sys.argv) == 2: # Allow running on customized ports
        app.run(port=int(sys.argv[1]))
    else:
        app.run() # Default port 5000
