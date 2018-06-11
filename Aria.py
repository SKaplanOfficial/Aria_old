#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
 
import speech_recognition as sr
from time import ctime
import time
import os
from os.path import join
import webbrowser
import geopy
from geopy import geocoders
import calendar
import pytz
from datetime import datetime
from gtts import gTTS
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import random
import numbers

ranInt = 0
guesses = 0
exitQ = 0
storedData = ""

sessionTimer = 2

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    #tts.save("audioPlayer.mp3")
    #os.system("mpg321 audioPlayer.mp3")
    os.system("say '"+audioString+"'")
 
def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
 
    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
 
    return data
 
def jarvis(data):
    global streakType
    
    global ranInt
    global guesses
    global exitQ
    global sessionTimer
    global storedData

    data = data.lower()

    if "aria" in data:
        data = data[5:]

    if "oriya" in data:
        data = data[6:]
    
    elif "how are you" in data:
        speak("I am fine")
        streakType = "HowAre"
        sessionTimer = 5

    elif "what time is it in" in data:
        data = data.split(" ")
        location = data[5]
        print(location)
        g = geocoders.GoogleV3(scheme='http')
        location = g.geocode("175 5th Avenue NYC")
        print((location.latitude, location.longitude))
        tz = g.timezone((lat, long))
        now = datetime.now(pytz.timezone(tz)) # you could pass `timezone` object here
        speak("Using a 24-hour clock, the time in "+location+" is currently "+ calendar.day_name[now.weekday()]+", "+now.strftime("%H:%M:%S"))
        streakType = "TimeIn"
        sessionTimer = 5
 
    elif "what time is it" in data:
        speak(ctime())
        streakType = "Time"
        sessionTimer = 5
 
    elif "where is" in data:
        data = data.split(" ")
        location = data[2]
        if streakType != "Where":
            speak("Hold on, I will show you where " + location + " is.")
            streakType = "Where"
        webbrowser.open("https://www.google.com/maps/place/" + location + "/&amp;", new=0, autoraise=True)
        streakType = "Where"
        sessionTimer = 5

    elif streakType == "GuessingGame" and "" in data:
        sessionTimer = 5
        data1 = data.split(" ")
        if is_number(data1[0]):
            guess = int(data1[0])
            exitQ = 0
            if guess<ranInt:
                guesses = guesses+1
                if guesses==1:
                    speak("Your guess was too low. You have now used "+str(guesses)+" guess.")
                else:
                    speak("Your guess was too low. You have now used "+str(guesses)+" guesses.")
            elif guess>ranInt:
                guesses = guesses+1
                if guesses==1:
                    speak("Your guess was too high. You have now used "+str(guesses)+" guess.")
                else:
                    speak("Your guess was too high. You have now used "+str(guesses)+" guesses.")
            elif guess==ranInt:
                guesses = guesses+1
                if guesses==1:
                    speak("Congratulations, you won the game in "+str(guesses)+" guess.")
                else:
                    speak("Congratulations, you won the game in "+str(guesses)+" guesses.")
                guesses = 0
                streakType = "FinishedGuessGame"
        elif exitQ == 1:
            streakType = ""
            exitQ = 0
            jarvis(data)
        else:
            speak("I was expecting a number. To end the game, repeat your command, or continue by guessing a number.")
            exitQ = 1;

    elif streakType == "FinishedGuessGame" and ("again" in data) or ("rematch" in data):
        speak("Starting a new game. I have selected a number between 1 and 100. What is your first guess?")
        streakType = "GuessingGame"
        ranInt = random.randint(1, 100)
        sessionTimer = 5

    elif "show me pictures of" in data:
        data = data.split(" ")
        i = 0
        item = ""
        while i < len(data):    
            if (i>4):
                item = item+" "+data[i]
            if (i==4):
                item = item+data[i]
            i += 1

        if streak==0:
            speak("Searching online for "+item+"...")
        webbrowser.open("https://www.bing.com/images/search?q="+item, new=0, autoraise=True)
        streakType = "Image"
        sessionTimer = 5

    elif "show me videos of" in data:
        data = data.split(" ")
        i = 0
        item = ""
        while i < len(data):    
            if (i>=4):
                item = item +"+"+data[i]
            i += 1

        if streak==0:
            speak("Searching online for "+item+"...")
        webbrowser.open("https://www.youtube.com/results?search_query="+item, new=0, autoraise=True)
        streakType = "Video"
        sessionTimer = 5

    elif "show me a calendar for" in data:
        data = data.split(" ")
        year = int(data[5])
        if streakType != "Calendar":
            streakType = "Calendar"
            speak("Coming right up...")
        print(calendar.calendar(year, 2, 1, 10))
        sessionTimer = 5

    elif "show me calendar for" in data:
        data = data.split(" ")
        year = int(data[4])
        if streakType != "Calendar":
            streakType = "Calendar"
            speak("Coming right up...")
        print(calendar.calendar(year, 2, 1, 10))
        sessionTimer = 5

    elif "show me" in data:
        data = data.split(" ")
        i = 0
        item = ""
        while i < len(data):
            if (i>2):
                item = item+" "+data[i]
            if (i==2):
                item = item+data[i]
            i += 1
        if streakType != "Image":
            speak("Searching online for "+item+"...")
            streakType = "Image"
        webbrowser.open("https://www.bing.com/images/search?q="+item, new=0, autoraise=True)
        sessionTimer = 5

    elif ("thank you" in data) or ("thanks" in data):
        speak("My pleasure!")
        sessionTimer = 5

    elif ("neat" in data) or ("cool" in data) or  ("awesome" in data) or ("you're good at this" in data):
        speak("Thanks.")
        sessionTimer = 5

    elif ("play music" in data) or ("play a song" in data) or ("play song" in data):
        speak("Playing music.")
        os.system("open -a iTunes")
        os.system("osascript -e 'tell application \"iTunes\" to play'")
        sessionTimer = 5

    elif "next song" in data:
        speak("Playing next song.")
        os.system("osascript -e 'tell application \"iTunes\" to next track'")
        sessionTimer = 5

    elif "find" in data:
        data = data.split(" ")
        i = 0
        item = ""
        while i < len(data):
            if (i>1):
                item = item+data[i]
            if (i==1):
                item = item+data[i]
            i += 1
        if streakType != "File":
            speak("Searching locally for "+item+"...")
            streakType = "File"
        for root, dirs, files in os.walk('/Users/stevekaplan/'):
            if item in [x.lower() for x in files]:
                speak("The file is located at: %s" % join(root, item))
                speak("Would you like me to open it?")
                storedData = join(root,item)
                break
        sessionTimer = 5

    elif streakType=="File" and "yes" in data:
        speak("Opening...")
        os.system("open "+storedData)

    elif streakType=="Image" and "" in data:
        sessionTimer = 5
        data = data.split(" ")
        i = 0
        item = ""
        while i < len(data):
            if (i>0):
                item = item+" "+data[i]
            if (i==0):
                item = item+data[i]
            i += 1

        if item != "" and item != " ":
            webbrowser.open("https://www.bing.com/images/search?q="+item, new=0, autoraise=True)


    elif streakType=="Calendar" and "" in data:
        data = data.split(" ")
        year = int(data[0])
        print(calendar.calendar(year, 2, 1, 10))
        sessionTimer = 5

    elif "open" in data:
        data = data.split(" ")
        sessionTimer = 5
        i = 0
        item = ""
        while i < len(data):
            if (i>=1):
                item = item+""+data[i]
            i += 1
        speak("Opening "+item+"...")
        os.system("open -a "+item)
        streakType = "Open"

    elif streakType=="Open" and "and" in data:
        sessionTimer = 5
        data = data.split(" ")
        i = 0
        item = ""
        while i < len(data):
            if (i>=1):
                item = item+""+data[i]
            i += 1
        os.system("open -a "+item)

    elif streakType=="Open" and "" in data:
        sessionTimer = 5
        data = data.split(" ")
        i = 0
        item = ""
        while i < len(data):
            if (i>=0):
                item = item+""+data[i]
            i += 1
        os.system("open -a "+item)

    elif "give me a random number" in data:
        speak(str(random.randint(0,100)))
        streakType = "Random"
        sessionTimer = 5

    elif streakType == "Random" and "again" in data:
        speak(str(random.randint(0,100)))
        streakType = "Random"
        sessionTimer = 5

    elif "guessing game" in data:
        speak("Okay. I have selected a number between 1 and 100. What is your first guess?")
        streakType = "GuessingGame"
        ranInt = random.randint(1, 100)
        sessionTimer = 5

    elif "give me lyrics for" in data:
        data = data.split(" ")
        pos1 = data.index("by")

        song = ""
        i = 0
        while i < pos1:
            if (i>4):
                song = song+"_"+data[i]
            if (i==4):
                song = song+data[i]
            i += 1

        artist = ""
        i = pos1
        while i < len(data):
            if (i>pos1+1):
                artist = artist+"_"+data[i]
            if (i==pos1+1):
                artist = artist+data[i]
            i += 1
        
        speak("Finding lyrics...")
        webbrowser.open("http://lyrics.wikia.com/wiki/"+artist+":"+song, new=0, autoraise=True)
        streakType = "Lyrics"
        sessionTimer = 5
 
# initialization
time.sleep(1)
speak("Hello, my name is Aria.") #Aria is awesome sounding
speak("What may I help you with...?")
streak=0
streakType=""
while 1:
              
    if sessionTimer>0:
        sessionTimer = sessionTimer-1
        
    data = recordAudio()
    
    if ("Aria" in data or "Oriya" in data or sessionTimer > 0):
        jarvis(data)
