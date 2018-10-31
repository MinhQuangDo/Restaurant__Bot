import time, string, random, re
import nltk
from pattern.search import search

def isAskingBotInformation(sentence):
    print(sentence)
    print(type(sentence))
    # m = search('what *+ your name', sentence)
    m = re.search(r'your name', sentence, re.IGNORECASE)
    if m:
        return True

    m = re.search(r'your creator|dad|mom|father|mother|papa|mama|daddy|mommy', sentence, re.IGNORECASE)
    if m:
        return True

    m = re.search('who are you', sentence, re.IGNORECASE)
    if m:
        return True

    m = re.search(r'who .* made|created|wrote|built|gave birth .* you', sentence, re.IGNORECASE)
    if m:
        return True

    m = re.search(r'call you', sentence, re.IGNORECASE)
    if m:
        return True

    return False

def isGreetings(inp_str):
    string = inp_str.lower().split(" ")
    if len(string) > 3:
        return False
    greetings = ['hi','hey','hello', 'greetings', 'good morning', 'good afternoon', 'good evening']
    for word in greetings:
        if word in string[:3]:
            return True
    return False

def handleBotInfo(sentence):
    name = ["I wish I had one :(", "Even I don't know", "Can you give me one? B-)"]
    creator = ["It's a mystery :O", "You are among the few who I tell: All I know about my creator is the initial M :)", "It remains a mystery to me even :(", "It was erased from my memory from the start :("]

    # m = search('what *+ your name', sentence)
    m = re.search(r'your name', sentence, re.IGNORECASE)
    if m:
        return oneOf(name)

    m = re.search(r'your creator|dad|mom|father|mother|papa|mama|daddy|mommy', sentence, re.IGNORECASE)
    if m:
        return oneOf(creator)

    m = re.search('who are you', sentence, re.IGNORECASE)
    if m:
        return oneof(name)

    m = re.search(r'who .* made|created|wrote|built|gave birth .* you', sentence, re.IGNORECASE)
    if m:
        return oneOf(creator)

    m = re.search(r'call you', sentence, re.IGNORECASE)
    if m:
        return "Anything you want to <3"

    return "Can you guess? ;)"

def oneOf(arr):
    rand_idx = random.randint(0,len(arr) - 1)
    return arr[rand_idx]
