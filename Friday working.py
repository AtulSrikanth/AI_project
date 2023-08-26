import mysql.connector as sql
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import randfacts
import pyjokes
import pyowm
import os
import tkinter as tk
import tkinter.scrolledtext as st
from AppOpener import open, close
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
from threading import Thread

def relative_to_assets(path: str):
    return ASSETS_PATH / Path(path)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def cons(message):
    text_area.configure(state = 'normal')
    text_area.insert(tk.INSERT, message+'\n')
    text_area.see("end")
    text_area.configure(state='disabled')

def startListening():
    while True:
        listenForCommand("loop")

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

def listenForCommand(modl):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        cons("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        cons("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        cons(f"User said: {query}")
        if modl=="wiki":
            return query
        elif modl=="report":
            processReport(query.lower())
        else:
            processCommand(query.lower())
    except Exception as e:
        cons("Say that again please...")
        speak("Say that again please...")
        listenForCommand("loop")

def processCommand(command):
    if 'wikipedia' in command:
        searchWikipedia(command)
    elif 'open app' in command:
        openApp()
    elif 'close app' in command:
        closeApp()
    elif 'open youtube' in command:
        openYouTube()
    elif 'open google' in command:
        openGoogle()
    elif 'what is' in command:
        openspGoogle()
    elif 'weather' in command:
        weather()
    elif 'play music' in command or 'play song' in command:
        playMusic()
    elif 'the time' in command:
        getTime()
    elif 'date' in command:
        getDate()
    elif 'report' in command:
        showReport()
    elif 'joke' in command:
        tellJoke()
    elif 'fact' in command:
        tellFact()
    elif 'exit' in command:
        cur.close()
        con.close()
        exit()
    elif 'thank you' in command:
        thankExit()
    else:
        speak("Sorry, I didn't understand that.")

def insrt_table(cmd):
    update_command='INSERT INTO COMMAND_CENTRE VALUES(%d,"%s",NULL);'%(datetime.datetime.now().timestamp(),cmd)
    cons(update_command)
    cur.execute(update_command)
    cur.execute('commit')

def searchWikipedia(command):
    speak('What would you like to search on Wikipedia?')
    query = listenForCommand("wiki")
    speak('Searching Wikipedia...')
    results = wikipedia.summary(query, sentences=2)
    speak("According to Wikipedia")
    cons(results)
    speak(results)
    update_command='INSERT INTO COMMAND_CENTRE VALUES(%d,"%s","%s");'%(datetime.datetime.now().timestamp(),command,query.lower())
    cons(update_command)
    cur.execute(update_command)
    cur.execute('commit')

def openYouTube():
    speak("Opening YouTube...")
    webbrowser.get(chrome_path).open("https://www.youtube.com")
    insrt_table("youtube")

def openGoogle():
    speak("Opening Google...")
    webbrowser.get(chrome_path).open("https://www.google.com")
    insrt_table("google")

def openspGoogle(search):
    search = search.replace(' ', '+')
    webbrowser.get(chrome_path).open(
        "https://www.google.co.in/search?q="+search)
    insrt_table("google:", search)

def openApp():
    speak("Which app would you like to open")
    search = listenForCommand("re")
    search = search.lower()
    open(search, match_closest=True)
    speak("Opening", search)
    cons("Opening", search)
    insrt_table("open",search)


def closeApp():
    speak("Which app would you like to close")
    search = listenForCommand("re")
    search = search.lower()
    close(search, match_closest=True)
    speak("Closing", search)
    cons("Closing", search)
    insrt_table("close", search)

def tellJoke():
    joke = pyjokes.get_joke()
    speak(joke)
    cons(joke)
    insrt_table("joke")

def tellFact():
    fact1 = randfacts.get_fact()
    speak(fact1)
    cons(fact1)
    insrt_table("fact")

def playMusic():
    speak("Playing music...")
    webbrowser.get(chrome_path).open("https://open.spotify.com")
    insrt_table("music")

def getTime():
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The time is {strTime}")
    cons(f"The time is {strTime}")
    insrt_table("time")

def getDate():
    today = datetime.date.today()
    speak(f"Today's date is {today}")
    cons(f"Today's date is {today}")
    insrt_table("date")

def thankExit():
    speak("Welcome. Have a nice day. Bye")
    cons("Welcome. Have a nice day. Bye")
    cur.close()
    con.close()
    exit()

def weather():
    owm = pyowm.OWM('6cf345bdb3238dcc59d4d0878b3ad803')  # Replace 'your_api_key' with your actual API key

    while True:
        # Ask the user for the city
        speak("Which city's weather do you want to know?")
        city = listenForCommand("re")

        try:
            observation = owm.weather_at_place(city)
            weather_data = observation.get_weather()
            temperature = weather_data.get_temperature(unit='celsius')['temp']
            status = weather_data.get_status()

            # cons and speak the weather information
            speak(f"Temperature in {city} is {temperature} degrees Celsius.")
            speak(f"The weather in {city} is {status}.")
            cons(f"Temperature in {city} is {temperature} degrees Celsius.")
            cons(f"The weather in {city} is {status}.")
            insrt_table("Weather")
            break  # Exit the loop since weather information was found

        except pyowm.exceptions.not_found_error.NotFoundError:
            # Retry or exit
            speak("Weather information not found for that city. Would you like to try another city?")
            retry = listenForCommand("re")
            if "no" in retry.lower():
                speak("Alright, no weather information retrieved.")
                break  # Exit the loop if the user doesn't want to try again

    insrt_table('Weather')   


def showReport():
    speak('Choose report you would like to see from the following options')
    cons('Choose report you would like to see from the following options:')
    speak('full data, command frequency, topic frequency')
    cons('1. FULL DATA (TELL "FULL DATA")')
    cons('2. FREQUENCY OF COMMANDS USED (TELL "COMMAND")')
    cons('3. FREQUENCY OF TOPICS USED (TELL "TOPIC")')
    listenForCommand("report")

def processReport(query):
    if any(ext in query for ext in ['full data','command','topic']):
        update_command='INSERT INTO COMMAND_CENTRE VALUES(%d,"report","%s");'%(datetime.datetime.now().timestamp(),command)
        cons(update_command)
        cur.execute(update_command)
        cur.execute('commit')

    if 'full data' in query:
        cur.execute('SELECT * FROM COMMAND_CENTRE;')
        cur_details=cur.fetchall()
        cons("Time".center(30),"Command".center(30),"Subcommand".center(40))
        for i in cur_details:
            if i[2]=='NULL' or i[2] is None:
                cons(datetime.datetime.fromtimestamp(i[0]).strftime('%d/%m/%Y %H:%M:%S').ljust(30),i[1].ljust(30))
            else:
                cons(datetime.datetime.fromtimestamp(i[0]).strftime('%d/%m/%Y %H:%M:%S').ljust(30),i[1].ljust(30),i[2].ljust(30))
    elif 'command' in query:
        cur.execute('SELECT COMMAND_NAME, COUNT(*) FROM COMMAND_CENTRE GROUP BY COMMAND_NAME;')
        cur_details=cur.fetchall()
        cons("Command".center(30),"Frequency".center(10))
        for i in cur_details:
            cons(i[0].ljust(30),i[1])
    elif 'topic' in query:
        cur.execute('SELECT SUBCOMMAND, COUNT(*) FROM COMMAND_CENTRE WHERE COMMAND_NAME="WIKIPEDIA" GROUP BY SUBCOMMAND;')
        cur_details=cur.fetchall()
        cons("Subcommand".center(30),"Frequency".center(10))
        for i in cur_details:
            cons(i[0].ljust(30),i[1])
    else:
        speak("Sorry, I didn't understand that.")
        cons("Sorry, I didn't understand that.")




chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(os.getcwd()) #enter your file path
        


#TK!
window = Tk()
        
window.geometry("600x400")
window.configure(bg="#404040")
window.title("Friday Assistant")

canvas = Canvas(
    window,
    bg = "#404040",
    height = 400,
    width = 600,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    300.0,
    200.0,
    image=image_image_1
)

text_image = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    299.5,
    332.5,
    image=text_image
)
text_area = st.ScrolledText(
    bd=0,
    bg="#292929",
    fg="#ffffff",
    highlightthickness=0,
    font=("Times New Roman", 10)
)
text_area.place(
    x=12.0,
    y=272.0,
    width=575.0,
    height=119.0
)
text_area.configure(state = 'disabled')



speak_image = PhotoImage(
    file=relative_to_assets("button_2.png"))
speak_button = Button(
    image=speak_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: Thread(target=startListening).start(),
    relief="flat"
)
speak_button.place(
    x=247.0,
    y=95.0,
    width=105.0,
    height=105.0
)
'''report_image = PhotoImage(
    file=relative_to_assets("button_1.png"))
report_button = Button(
    image=report_image,
    borderwidth=0,
    highlightthickness=0,
    command=showReport(),
    relief="flat"
)
report_button.place(
    x=563.0,
    y=9.0,
    width=25.0,
    height=25.0
)'''
window.resizable(False, False)





 #connecting mySQL
try:
    con = sql.connect(
        host='localhost', user='root', password='1234')
    cons('Connected with mySQL')
except Exception as e:
    cons('Database not connected.... Exiting')
    cons('Error:', e)
    exit()

cur = con.cursor()

try:
    cur.execute('USE SR_SEARCH_HISTORY;')
except:
    cur.execute('CREATE DATABASE SR_SEARCH_HISTORY;')

try:
    cur.execute('SHOW TABLES;')
    data = cur.fetchall()
    # cons(data)
    if ('command_centre',) not in data:
        # cons("created")
        cur.execute(
            "CREATE TABLE COMMAND_CENTRE(EXE_TIME BIGINT PRIMARY KEY, COMMAND_NAME VARCHAR(30), SUBCOMMAND VARCHAR(30));")
except Exception as e:
    cons("Error", e)





# Run the GUI main loop
wishMe()
window.mainloop()
    
