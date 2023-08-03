import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import randfacts
import pyjokes
import tkinter as tk
from threading import Thread

chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Friday, your assistant")
    speak("How may I help you?")

def listenForCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        processCommand(query.lower())
    except Exception as e:
        print("Say that again please...")
        listenForCommand()

def processCommand(command):
    if 'wikipedia' in command:
        searchWikipedia(command)
    elif 'open youtube' in command:
        openYouTube()
    elif 'open google' in command:
        openGoogle()
    elif 'joke' in command:
        tellJoke()
    elif 'fact' in commnd:
        tellFact()
    elif 'play music' in command or 'play song' in command:
        playMusic()
    elif 'the time' in command:
        getTime()
    elif 'date' in command:
        getDate()
    else:
        speak("Sorry, I didn't understand that.")

def searchWikipedia(command):
    speak('What would you like to search on Wikipedia?')
    query = listenForCommand()
    speak('Searching Wikipedia...')
    results = wikipedia.summary(query, sentences=2)
    speak("According to Wikipedia")
    print(results)
    speak(results)

def openYouTube():
    speak("Opening YouTube...")
    webbrowser.get(chrome_path).open("https://www.youtube.com")

def openGoogle():
    speak("Opening Google...")
    webbrowser.get(chrome_path).open("https://www.google.com")

def tellJoke():
    joke = pyjokes.get_joke()
    speak(joke)
    print(joke)

def tellFact():
    fact=get_fact(False)
    speak(fact)
    print(fact)

def playMusic():
    speak("Playing music...")
    webbrowser.get(chrome_path).open("https://open.spotify.com")

def getTime():
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The time is {strTime}")

def getDate():
    today = datetime.date.today()
    speak(f"Today's date is {today}")

def startListening():
    while True:
        listenForCommand()

# Create the main window
window = tk.Tk()
window.title("Friday Assistant")
bg="violet"

# Create and position the GUI components
label = tk.Label(window, text="Press the 'Speak' button and give a command:",bg="Violet")
label.pack()

speak_button = tk.Button(window, text="Speak", command=lambda: Thread(target=startListening).start())
speak_button.pack()

# Run the GUI main loop
wishMe()
window.mainloop()
