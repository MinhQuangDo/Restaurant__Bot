Facebook Restaurant Bot
======

This is a Facebook Messenger Bot that supports Natural Language Processing and features such as: search restaurants based on location and food preferences. transcribe and save memos to the cloud. It can provide customized greetings (acknowledging user's time in any time zone, i.e. Good morning/Good evening) and entertaining responses, etc.


**Table of Contents**


- [Features](#features)
- [Usage](#usage)
  - [Dependencies, Database and API keys](#dependencies-database-and-api-keys)
  - [Deploying to the cloud](#deploying-to-the-cloud)
  - [Voice Recognition](#voice-recognition)
  - [Natural Language Processing](#natural-language-processing)
  - [Custom features](#custom-features)
    - [1. Business/Restaurant Search](#1-businessrestaurant-search)
    - [2. Trending News Search](#2-trending-news-search)
    - [3. Memo](#3-memo)
- [Appendix](#appendix)
  - [Facebook Messenger API](#facebook-messenger-api)
  - [Sample Facebook Messenger API Messages](#sample-facebook-messenger-api-messages)
    - [1. Text](#1-text)
    - [2. Audio](#2-audio)
    - [3. Location](#3-location)
  - [Discussion](#discussion)
    - [The nitty-gritty detail of implementing voice recognition & scalability](#the-nitty-gritty-detail-of-implementing-voice-recognition-&-scalability)


#### Features:
- Understanding commands with Natural Language Processing and contextual follow-up
- Restaurant Search
- Conversational chit-chat


## Usage

#### Dependencies, Database and API keys

In order to build your own bot with all features of Optimist Prime, you'll need a few set-ups:

0. Install dependencies: `pip install -r requirements.txt` (preferably getting into your virtual environment `virtualenv`/`venv` - read all about `pip` and `venv` [here](https://packaging.python.org/installing/))
1. [Create a Facebook Page](https://www.facebook.com/pages/create/): A bare-bone Page to "assign" the Bot to will do. The Bot will actually be this page, i.e. you'll be "talking" to the page
2. [Create a Facebook App](https://developers.facebook.com/docs/apps/register), get its Page Access Token (details at Facebook's [Quick Start](https://developers.facebook.com/docs/messenger-platform/quickstart/))


Then a few configurations in `config.py`:

1. Yelp API key (Business/Restaurant Search feature): [Get one here](https://www.yelp.com/developers/manage_api_keys) (More details below, as Yelp now has a stable v2 API and a developer preview v3)
2. Define your own local config: create a folder called `instance`, and create another `config.py` file in it. ([More on Flask configurations](http://flask.pocoo.org/docs/0.11/config/))

To run locally, as simple as:
```bash
python facebookbot.py 3000
```

Now that you've got the bot running, you'll need to set up a webhook for Facebook to send messages the bot receives to. This could be done with `ngrok`, which will set up a secure tunnel to your localhost server:
```bash
./ngrok http 3000
```
![ngrok](https://monosnap.com/file/HJckHGSorOuoEqm6kBNFb7MQWdNeHf.png)

Get the `https` URL (Facebook requires `https` secured webhooks) and subscribe your Facebook App to this webhook. The verification token is your own token defined in `OWN_VERIFICATION_TOKEN` in `config.py`.

![webhook](https://monosnap.com/file/LJITuhaxURs7MXpDQrvDKBk7yIrBER.png)

## Natural Language Processing

The Bot receives commands from users and understands commands in natural language. This is done by using the `pattern` NLP [library](http://www.clips.ua.ac.be/pages/pattern-en), which allows the bot to deconstruct the user's text input and recognize parts of speech. 

The command system allows users to use the following features, all of which are under the `Utils` folder.

## Custom features

### 1. Business/Restaurant Search

Example commands:
```
		irish bar near by.
		find chinese restaurants.
		find me a good coffee shop around here.
		show me Chinese food close by.
		find mexican restaurants near here.
		I want to have vietnamese food tonight.
		is there a korean bbq nearby?
		what are some cambodian grill close by?
		find an ethiopian restaurant.
		I want mediterranean food.
		find a Target.
		find me a KFC around.
		I'd like to eat at McDonalds.
		find me some fast food places in ohio city.
		find me a brewery near downtown san francisco.
```

After receiving the command, it would ask for your location. You can input either a text/voice-based **location name** or send your **exact GPS location** (with Facebook Messenger on mobile devices). 

![Smart Location Search](https://monosnap.com/file/5ox1ff0xx1l6r2cjTD7o7Gcb8aqgKF.png)

Optimist Prime leverage Yelp's API. Included in the code is both the APIv2 (stable) and APIv3 (developer preview). Both require you to acquire their API key.

[Get API key for v2](https://www.yelp.com/developers/manage_api_keys)

[Get API key for v3](https://www.yelp.com/developers/v3/preview)

After you've got your API key, put them into `config.py`

To switch between v2 and v3, change the `import` statement in `facebookbot.py` between `yelp_search_v2` and `yelp_search_v3`

```python
from Utils.Yelp import yelp_search_v3 as yelp_search
```

### 2. Trending News Search

Example commands:
```
	get me news about Harvard.
    find news about Zika.
    get me some news about the US presidential elections.
    Get trending news about the US in the Olympics.
    look for latest news on the Olympics.
```
![News Search](https://monosnap.com/file/wTn8lqcV1mgryNs5bMEG2LFcCQb1ff.png)

The Trending News Search leverages [Webhose.io API](https://webhose.io/SDK). The service crawls the web for news along with its social strength (Facebook likes, Shares, Twitter posts). In case of user searching for not-so-trending or niche topics, Optimist Prime lowers its "trending" criteria as well as search time frame to get the best results.

### 3. Memo

Example commands:
```
	memorize this for me: [continue speaking your memo]
	memorize this: [continue speaking your memo]
	memorize this (stop talking, Optimist Prime will prompt you to start your memo)
	can you memorize this for me?
```
![Memo](https://monosnap.com/file/cYHCLLXhdSTPeQi0qtTl3dhF7S209k.png)

This feature is still in its infancy/concept. After the user saves a memo, s/he can access it on the web with the link provided by the bot.

The unfortunate catch I found was that Facebook uses different user_ids for Facebook Profile (which is used for login) and Messenger. A same account would have 2 different user_ids, and the bot only receives the Messenger user_id from the Messenger API, thus making the implementation of a secured Facebook Login feature impossible. My current solution is to allow users to access their own memo inside the bot chat using user_ids as URL paths for querying. Future: We might use Account Linking for this.

## License 
* MIT License, see `LICENSE.txt`

## Version 
* Version 1.0


## Contact
#### Hung Tran
* e-mail: hung@traan.vn


## APPENDIX

#### Facebook Messenger API
https://developers.facebook.com/docs/messenger-platform/product-overview


#### Sample Facebook Messenger API Messages

##### 1. Text
```json
{
    "object": "page",
    "entry": [
        {
            "id": "1384358948246110",
            "time": 1473197313689,
            "messaging": [
                {
                    "sender": {
                        "id": "1389166911110336"
                    },
                    "recipient": {
                        "id": "1384358948246110"
                    },
                    "timestamp": 1473197313651,
                    "message": {
                        "mid": "mid.1473197313635:0a67934dfc4f04a629",
                        "seq": 7651,
                        "text": "Hey"
                    }
                }
            ]
        }
    ]
}
```

##### 2. Audio
```json
{
    "object": "page",
    "entry": [
        {
            "id": "1384358948246110",
            "time": 1473197300200,
            "messaging": [
                {
                    "sender": {
                        "id": "1389166911110336"
                    },
                    "recipient": {
                        "id": "1384358948246110"
                    },
                    "timestamp": 1473197300143,
                    "message": {
                        "mid": "mid.1473197298861:d6cf1fae1ad44ff234",
                        "seq": 7650,
                        "attachments": [
                            {
                                "type": "audio",
                                "payload": {
                                    "url": "https://cdn.fbsbx.com/v/t59.3654-21/14109832_10209906561878191_940661414_n.mp4/audioclip-1473197298000-2056.mp4?oh=85e027f68e17fa0b1c189c3d7f3164bf&oe=57D0B0F3"
                                }
                            }
                        ]
                    }
                }
            ]
        }
    ]
}
```

##### 3. Location
```json
{
    "object": "page",
    "entry": [
        {
            "id": "1384358948246110",
            "time": 1473197244135,
            "messaging": [
                {
                    "sender": {
                        "id": "1389166911110336"
                    },
                    "recipient": {
                        "id": "1384358948246110"
                    },
                    "timestamp": 1473197244008,
                    "message": {
                        "mid": "mid.1473197243814:3803076c5438a13036",
                        "seq": 7646,
                        "attachments": [
                            {
                                "title": "Hung's Location",
                                "url": "https://www.facebook.com/l.php?u=https%3A%2F%2Fwww.bing.com%2Fmaps%2Fdefault.aspx%3Fv%3D2%26pc%3DFACEBK%26mid%3D8100%26where1%3D40.070706608101%252C%2B-82.525680894134%26FORM%3DFBKPL1%26mkt%3Den-US&h=mAQE9bbu3&s=1&enc=AZPC_QlKfUFl7dehzlPuSpsio7LMKtRwyM58oaqUtt89CfKBofXVoW48cYrASUdCm-MYSpFMI2ejgmTR90taFN4wyv0aCYNH_GG3MR5sEe62NQ",
                                "type": "location",
                                "payload": {
                                    "coordinates": {
                                        "lat": 40.070706608101,
                                        "long": -82.525680894134
                                    }
                                }
                            }
                        ]
                    }
                }
            ]
        }
    ]
}
```

There are also other useful types of message (also implemented in this bot), including Quick Reply, Postback at [Facebook Messenger API documentation](https://developers.facebook.com/docs/messenger-platform/webhook-reference/message-received).


## Discussion

#### The nitty-gritty detail of implementing voice recognition & scalability

The catch for processing voice messages from the Facebook Messenger API is **converting Facebook's compressed mp3 to a valid input format** for the Speech-to-Text API. Both IBM and Google do not support mp3, and their input format include principle audio formats like WAV, FLAC, OGG, etc. Therefore, Optimist Prime actually has to download the mp3 audio, convert it to WAV, and upload it to the Speech API, which is a round trip that significantly increases response time for each audio command. In this project, I used `ffmpeg` and call it with Python's `subprocess` to convert the audio.

> `subprocess` is a Python tool that allows you to trigger command line-like commands, so what the program does is equivalent to it calling another program "by typing this command into the command line"

![ffmpeg in subprocess](https://monosnap.com/file/LWCiJmkZsTRcgeEBXRr5xGBU4gzIpi.png)

Under the hood, the bot does the following:
- Receive json of the user's audio command
- Download this audio file
- Use `ffmpeg` to convert:
	+ Use Python `subprocess` to initiate a native ffmpeg command (just as you would do in the command shell)
	+ Get the converted audio output into a pipe as a file blob
	+ Return this file blob
- Upload the converted audio file blob to the Speech API

This approach takes the output of `ffmpeg` directly from the pipe and upload it without saving it to a temp file and then uploading the file. 

The story behind it was a learning experience on Heroku: Everything works perfectly on local, but when deployed to Heroku, Python keeps saying the file previously downloaded is not found. I ssh-ed into the Heroku dyno, and fascinatingly nothing was ever downloaded. I suspect this has to do with either: Heroku ephemeral file system (which does not allow program to save file due to the fact that it is a distributed system - but I highly doubt this hypothesis), or that I needed to use absolute path for any read/write operation on Heroku. I'm leaning more to the latter, as the same problem happened for `subprocess` to call `ffmpeg`, as I had to explicitly declare the path to ffmpeg (pictured above).

This poses a questions of scalability (on theory): multiple concurrent conversions could max out the memory as this is done in the pipe. However, I believe this would not be the bottle-neck at scale, as most audio files tend to be less than 1MB, so for multiple users, the bottle-neck would lie in the connection to download/upload files, instead of the memory to convert all these files. Files would be done with conversion before another file is done downloading. This hypothesis has to be tested.

When a user sends an audio to the bot, the bot will "receive" an URL to the file, as processed in the code below in the main bot file `facebookbot.py`:
![Code to process different incoming message types](https://monosnap.com/file/rsb20Cxn5WUKFZ7hDLhjHBagMbk0rF.png)