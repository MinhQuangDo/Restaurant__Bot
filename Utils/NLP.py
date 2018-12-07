import time, string, random, re
import nltk
import json
from pattern.search import search
from yelp.client import Client

from yelpapi import YelpAPI
import spacy

spacy.prefer_gpu()
nlp = spacy.load('en_core_web_sm')


MY_API_KEY = "F7e2qnuOw-oNAD-ygIhScfzLjiuqmXX3_de76ztQSxUZRbzDiLmD0NrHom8JcZDTFt3IB5IobbDDxFglllPougjfuricDH1f2fVbPpf9IW9g8EUZByHAmOwbNlHeW3Yx"

yelp_api = YelpAPI(MY_API_KEY)


def isAskingBotInformation(sentence):
    print(sentence)
    m = re.search(r'your name', sentence, re.IGNORECASE)
    if m:
        return True

    m = re.search(r'your creator|dad|mom|father|mother|papa|mama|daddy|mommy', sentence, re.IGNORECASE)
    if m:
        return True

    m = re.search(r'who are you', sentence, re.IGNORECASE)
    if m:
        return True

    m = re.search(r'who .* made|created|wrote|built|gave birth .* you', sentence, re.IGNORECASE)
    if m:
        return True

    m = re.search(r'call you|a name', sentence, re.IGNORECASE)
    if m:
        return True

    return False

def isAskingRestaurant(sentence, message_text):
    verbs = findVerb(sentence)
    noun_phrases = findNounPhrase(sentence)
    # If match key verbs
    yelpVerbs = ['eat', 'drink', 'find', 'display', 'get']
    for verb in verbs:
        if verb.lower() in yelpVerbs:
            return True

    yelpNouns = ['restaurant', 'food', 'drink', 'shop', 'store', 'bar', 'pub']
    for noun in yelpNouns:
        if noun in noun_phrases:
            return True

    # If match question/command structure
    # "is there" + noun phrase
    if "is there" in sentence.string \
        or "are there" in sentence.string \
        and noun_phrases != "":

        return True

    m = re.search(r'get|find|show|search', message_text, re.IGNORECASE)
    if m:
        return True

    return False


def isGreetings(inp_str):
    if "good morning" in inp_str.lower() or "good afternoon" in inp_str.lower() or "good evening" in inp_str.lower():
        return True
    string = inp_str.lower().split(" ")
    if len(string) > 3:
        return False
    greetings = ['hi','hey','hello', 'greetings', 'good morning', 'good afternoon', 'good evening']
    for word in greetings:
        if word in string[:3]:
            return True
    return False

def isGoodbye(inp_str):
    m = re.search(r'see you|ya', inp_str, re.IGNORECASE)
    if m:
        return True

    string = inp_str.lower().split(" ")
    if "bye" in string:
        return True
    return False

def handleBotInfo(sentence):
    name = ["I wish I had one :(", "Even I don't know", "Can you give me one? B-)"]
    creator = ["It's a mystery :O", "You are among the few who I tell: All I know about my creator is the initial M :))", "It remains a mystery to me even :(", "It was erased from my memory from the start :("]

    # m = search('what *+ your name', sentence)
    m = re.search(r'your name', sentence, re.IGNORECASE)
    if m:
        return oneOf(name)

    m = re.search(r'your creator|dad|mom|father|mother|papa|mama|daddy|mommy', sentence, re.IGNORECASE)
    if m:
        return oneOf(creator)

    m = re.search(r'who .* made|created|wrote|built|gave birth|are .* you', sentence, re.IGNORECASE)
    if m:
        return oneOf(creator)

    m = re.search(r'call you', sentence, re.IGNORECASE)
    if m:
        return "Anything you want to <3"

    return "Can you guess? ;)"

def handle_find_rest(sentence):
    noun_phrases = findNounPhrase(sentence)
    if nearBy(sentence):
        return None, noun_phrases

    doc = nlp(noun_phrases.decode('utf8'))
    location = ""
    for ent in doc.ents:
       if ent.label_ == "GPE":
           location = ent.text

    print(location)
    if location == "":
        return None, noun_phrases

    response = yelp_api.search_query(term = noun_phrases, location = location, sort_by = "review_count", limit = 5)

    return response, noun_phrases

def handle_location(np, loc):
    response = yelp_api.search_query(term = np, longitude = loc[1], latitude = loc[0], sort_by = "distance", limit = 5)
    return response

def findVerb(sentence):
    result = []
    for chunk in sentence.chunks:
        if chunk.type in ['VP']:
            strings = [w.string for w in chunk.words if w.type in ['VB','VBP']]
            result.extend(strings)
    return result

# input: pattern.en sentence object
def findNounPhrase(sentence):
    res = ""
    for chunk in sentence.chunks:
        if chunk.type == 'NP':
            res += " ".join([w.string for w in chunk.words if w.type not in ['PRP', 'DT']])
            res += " "
    for verb in ['find','get','show','search']:
        res = res.replace(verb, "")
    return res

def findNounPhrase(sentence):
    res = ""
    for chunk in sentence.chunks:
        if chunk.type == 'NP':
            res += " ".join([w.string for w in chunk.words if w.type not in ['PRP', 'DT']])
            res += " "
    for verb in ['find','get','show','search']:
        res = res.replace(verb, "")
    return res

def nearBy(sentence):
    res = ""
    for chunk in sentence.chunks:
        if chunk.type in ['PP', 'ADVP']:
            res += " ".join([w.string for w in chunk.words if w.type in ['RB', 'PRP', 'IN']])
            res += " "
    res = res.strip()
    if res in ['near me', 'around here', 'around', 'near here', 'nearby', 'near by', 'close by', 'close']:
        return True
    return False



def oneOf(arr):
    rand_idx = random.randint(0,len(arr) - 1)
    return arr[rand_idx]
