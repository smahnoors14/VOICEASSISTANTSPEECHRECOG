import speech_recognition as sr # recognise speech
import playsound # to play an audio file
from gtts import gTTS # google text to speech
import random
from time import ctime # get time details
import webbrowser # open browser
import time
import os # to remove created audio files
import subprocess 
import bs4 as bs
import urllib.request #urllib
import requests
import datetime
from datetime import date
#from datetime import datetime

class person:
    name = ''
    def setName(self, name):
        self.name = name

class assist:
    name = ''
    def setName(self, name):
        self.name = name

def keyword(terms):
    for term in terms:
        if term in voice_data:
            return True


r = sr.Recognizer() # r = recogniser
#audio to text:
def record_audio(ask=""):
    with sr.Microphone() as source: #when microphone is our source
        if ask:
            sam_speak(ask)
        audio = r.listen(source, 5, 5)  #listen for the audio via microphone(src)
        voice_data = '' #user input so empty
        try:
            voice_data = r.recognize_google(audio)  #convert audio to text
        except sr.UnknownValueError: # error: recognizer does not get audio clearlyy
            sam_speak('I did not get that, please repeat')
        except sr.RequestError:
            sam_speak('Sorry, the service is down')
        return voice_data.lower() #will return in lowercase

#from string, make an audio file to be played by SAM
def sam_speak(audio_string):
    audio_string = str(audio_string)
    tts = gTTS(text=audio_string, lang='en') #text to voice //english
    r = random.randint(1,20000000) #random val for file name
    audio_file = 'audio' + str(r) + '.mp3'  #audio_file as mp3
    tts.save(audio_file) #save
    playsound.playsound(audio_file) #play the audio file
    print(assist_obj.name + ":", audio_string) # print what assistant said
    os.remove(audio_file) # remove audio file
    
def greeting():
    hour = int(datetime.datetime.now().hour)
    if hour>= 0 and hour<12:
        sam_speak("Good Morning!")
  
    elif hour>= 12 and hour<18:
        sam_speak("Good Afternoon!")   
    else:
        sam_speak("Good Evening!")  
    sam_speak("I am your Voice Assistant")
    sam_speak(assist_obj.name)

def respond(voice_data):
    # 1: hello
    if keyword(['hey','hi','hello']):
        greetings = ["hey, hope you're having a great day" + person_obj.name, "hey, what's up?" + person_obj.name, "I'm listening" + person_obj.name, "how can I help you?" + person_obj.name, "hello" + person_obj.name]
        greet = greetings[random.randint(0,len(greetings)-1)] #random reply from above options
        sam_speak(greet)

    # 2: name
    if keyword(["what is your name","what's your name","tell me your name"]):

        if person_obj.name:
            sam_speak(f"My name is {assist_obj.name}, {person_obj.name}") #if we(user) have given our name
        else:
            sam_speak(f"My name is {assist_obj.name}. what's your name?") #if we haven't provided our name.

    if keyword(["my name is"]):
        person_name = voice_data.split("is")[-1].strip() #split to get our name saved 
        sam_speak("Okay, I will remember your name " + person_name) 
        person_obj.setName(person_name) #save name in person object
    
    if keyword(["what is my name"]):
        sam_speak("Your name must be " + person_obj.name)
    
    if keyword(["your name should be"]):
        assist_name = voice_data.split("be")[-1].strip()
        sam_speak("Okay, I will remember that my name is " + assist_name)
        assist_obj.setName(assist_name) #save name in assist object

    # 3: greeting
    if keyword(["how are you","how are you doing"]):
        sam_speak("I'm good, hope you're fine too" + person_obj.name)
    
    # 4: Date 
    if keyword(["date", "whats the date today"]):
        date = datetime.date.today()
        sam_speak("Its " + str(date) + "." + "Have a nice day!")

    # 5: time
    if keyword(["time","what's the time","tell me the time","what time is it","what is the time"]):
        now = datetime.datetime.now()
        meridiem = ''
        if now.hour >= 12:
            meridiem = 'p.m' #Post Meridiem (PM)
            hour = now.hour - 12
        else:
            meridiem = 'a.m'#Ante Meridiem (AM)
            hour = now.hour
        if now.minute < 10:
            minute = '0'+str(now.minute)
        else:
            minute = str(now.minute)
            sam_speak('It is '+ str(hour)+ ':'+minute+' '+meridiem+' .')

    # 6: search google
    if keyword(["search for", "search"]) and 'youtube' not in voice_data:
        search_term = voice_data.split("for")[-1]
        url = "https://google.com/search?q=" + search_term
        webbrowser.get().open(url)
        sam_speak("Here is what I found for" + search_term + "on google")


    # 7: search youtube
    if keyword(["youtube"]):
        search_term = voice_data.split("for")[-1]
        search_term = search_term.replace("on youtube","").replace("search","")
        url = "https://www.youtube.com/results?search_query=" + search_term
        webbrowser.get().open(url)
        sam_speak("Here is what I found for " + search_term + "on youtube")

    
    # 8:  weather
    if keyword(["weather"]):
        search_term = voice_data.split("for")[-1]
        url = "https://www.google.com/search?sxsrf=ACYBGNSQwMLDByBwdVFIUCbQqya-ET7AAA%3A1578847393212&ei=oUwbXtbXDN-C4-EP-5u82AE&q=weather&oq=weather&gs_l=psy-ab.3..35i39i285i70i256j0i67l4j0i131i67j0i131j0i67l2j0.1630.4591..5475...1.2..2.322.1659.9j5j0j1......0....1..gws-wiz.....10..0i71j35i39j35i362i39._5eSPD47bv8&ved=0ahUKEwiWrJvwwP7mAhVfwTgGHfsNDxsQ4dUDCAs&uact=5"
        webbrowser.get().open(url)
        sam_speak("Here is what I found for weather of your local area on google")
    # 9: stackoverflow
    if keyword(["open stack overflow"]):
        url = "https://stackoverflow.com/"
        webbrowser.get().open(url)
        sam_speak("Here you go to Stack Over flow. Happy Coding!")
    # 10: song , music
    if keyword(['play music','play song' ,"song" , 'music' ]):
        url = "https://www.youtube.com/channel/UC-9-kyTW8ZkZNDHQJ6FgpwQ"
        webbrowser.get().open(url)
        sam_speak("Select songs from youtube music")    
          
     # 11: calc
    if keyword(["plus","minus","multiply","into","divide","power","+","-","*","/"]):
        opr = voice_data.split()[1]

        if opr == "+":
            sam_speak(int(voice_data.split()[0]) + int(voice_data.split()[2]))
        elif opr == "-":
            sam_speak(int(voice_data.split()[0]) - int(voice_data.split()[2]))
        elif opr == "into":
            sam_speak(int(voice_data.split()[0]) * int(voice_data.split()[2]))
        elif opr == 'divide':
            sam_speak(int(voice_data.split()[0]) / int(voice_data.split()[2]))
        elif opr == 'power' :
            sam_speak(int(voice_data.split()[0]) ** int(voice_data.split()[2]))
        else:
            sam_speak("Wrong Operator")

        
    # 12: Current location Google maps
    if keyword(["what is my exact location" , "where am i", "find my location"]):
        url = "https://www.google.com/maps/search/Where+am+I+?/"
        webbrowser.get().open(url)
        sam_speak("According to Google map, you must be somewhere near here")
    
    # 13: make a note / open notepad
    if keyword(["make a note","notepad" ,"make notes"]):
        search_term=voice_data.split("for")[-1]
        url="https://keep.google.com/#home"
        webbrowser.get().open(url)
        sam_speak("Go ahead and make notes.")

    #14 : Coronavirus update
    if keyword(["Coronavirus update", "coronavirus","what's the corona virus update"]):
        url = "https://www.worldometers.info/coronavirus/"
        webbrowser.get().open(url)
        sam_speak("Here you can get the coronavirus latest update")

    #16: open my project report
    if keyword(['project report']):
        sam_speak("opening Your Project Report")
        power = r"C:\Users\Aresha Afzal\Desktop\report.docx"
        os.startfile(power)

    # : Log off
    if keyword(["exit", "quit", "goodbye"]):
        sam_speak("Bye, See you soon.")
        exit()   
   
    



time.sleep(1)
person_obj = person()
assist_obj = assist()
assist_obj.name = 'SAM'
person_obj.name = ""
greeting()



while(1):
    voice_data = record_audio("How may I help you.") #get voice/speech
    print("You:", voice_data)
    respond(voice_data) 
