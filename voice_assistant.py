import pyttsx3
import speech_recognition as sr
import sqlite3

# Getting voice from Computer
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
#Use engine.setProperty("voice",voices[0].id) for male voice
#Use engine.setProperty("voice",voices[0].id) for female voice
engine.setProperty("voice",voices[0].id)
engine.setProperty("rate",185)

assistant = sqlite3.connect("voice_assistant.db")
curAssisnat = assistant.cursor()
#TO create table for phone number and mails of friends
curAssisnat.execute( '''CREATE TABLE IF NOT EXISTS friends (name TEXT NOT NULL,mail TEXT,phone INT);''')

"""
if you want to add name, mail and phone number
curAssisnat.execute('''INSERT INTO friends VALUES("Enter_name_here", "Enter_mail_here", Enter_phone_number_here)''')
or you can insert values direct using sqlite studio
"""

# Time for whole program
def timee():
    import time
    """
    Provide time to whole program
    :return time as a dictionary:
    """
    now = time.strftime("%Y:%m:%d:%H:%M:%S")
    now = now.split(":")
    curr_time = {
        "%Y":now[0],
        "%m":now[1],
        "%d":now[2],
        "%H":now[3],
        "%M":now[4],
        "%S":now[5]
    }
    return curr_time

#speak
def speak(speech):
    # time.sleep(0.5)
    print(speech)
    engine.say(speech)
    engine.runAndWait()
    text = reco().lower()
    return text

# For first time start
def start():
    now = timee()
    now = int(now["%H"])
    if now >= 0 and now < 12:
        # time.sleep(2)
        engine.say("Good Morning!")
        engine.runAndWait()

    elif now >=12 and now < 18:
        # time.sleep(2)
        engine.say("Good Afternoon!")
        engine.runAndWait()
    else:
        # time.sleep(2)
        engine.say("Good Evening!")
        engine.runAndWait()
    engine.say("I am JARVIS! how may i help you")
    engine.runAndWait()
    return

# Speech recognation
def reco():
    print("listing...")
    r = sr.Recognizer()
    r.pause_threshold = 1
    r.energy_threshold = 2000
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
    except Exception as e:
        er = "Somthing went wrong! please speak again"
        return "None"
    return text

def youtube(song_name):
    """
    Search video on youtube and play first video in from search list
    :param song_name:
    :return:
    """
    from time import sleep
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    try:
        # Enter your chromefriver path here like "C://Users//PARSHANT//Downloads//chromedriver_win32//chromedriver.exe"
        # but first you have download it

        driver = webdriver.Chrome(executable_path="C://Users//PARSHANT//Downloads//chromedriver_win32//chromedriver.exe")
        driver.maximize_window()

        # open youtube
        driver.get("https://www.youtube.com/")
        wait = WebDriverWait(driver, 3)
        visible = EC.visibility_of_element_located

        # searching for videos
        sleep(1)
        wait.until(visible((By.NAME, "search_query")))
        driver.find_element_by_name("search_query").click()
        driver.find_element_by_name("search_query").send_keys(song_name)
        driver.find_element_by_id("search-icon-legacy").click()

        # playing
        sleep(1)
        wait.until(visible((By.ID, "video-title")))
        sleep(1)
        driver.find_element_by_id("video-title").click()
    except:
        text = speak("somthing went wrong! Please speak again!")
        return text
    return

def wiki(content):
    """
    Search and read first two line of wikipedia article
    :param content:
    :return:
    """
    import wikipedia


    wiki = wikipedia.summary(content, sentences=2)
    engine.say("According to wikipedia")
    engine.runAndWait()
    speak(wiki)
    return

def google(content):
    """
    Search any query on google chrome
    :param content:
    :return:
    """
    import webbrowser
    # Enter your chorme it is same in most of pc but you have check before use
    webbrowser.register("chorme", None, webbrowser.BackgroundBrowser(
        "C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
    webbrowser.get("chorme").open(f"https://www.google.com/search?q={content}")
    return

def googleSites(siteName):
    """
    Open any site on google chrome whose damamin is .com and works on https server only
    :param siteName:
    :return:
    """
    import webbrowser
    # Enter your chorme it is same in most of pc but you have check before use
    webbrowser.register("chorme", None, webbrowser.BackgroundBrowser(
        "C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
    try:
        siteName = "https://www."+siteName+".com"
        webbrowser.get("chorme").open(siteName)
        return
    except:
        engine.say("site is  not found... I am searching on google for you")
        engine.runAndWait()
        siteName = siteName.split("www.")
        siteName = siteName[1].split(".")
        google(siteName[0])
        return

def whatsapp(to,content):
    """
    Send massage to any contact do You have in your contact list.
    First it goes to a dictionary in program where some personal contact you can store for fast word if
    contact is not stored in dictionary then it will ask for contact number and ask to store this number in dictionary
    :param to:
    :param content:
    :return:
    """
    from time import sleep
    """
    Note:-
    Before use pywhatkit you have to make some changes in pywhatkit module, to change follow simple step:
    1. Press CTRL + click pywhatkit next to line it will open direct pywhatkit module
    2. Change number of formal arrguments in sendwhatmsg function. Use three arrguments only(phone_no,message, print_waitTime=True)
    and remove other all
    3. Remove all line from this function and paste these six lines:-
    
    web.open('https://web.whatsapp.com/send?phone='+phone_no+'&text='+message)
    time.sleep(2)
    width,height = pg.size()
    pg.click(width/2,height/2)
    time.sleep(7)
    pg.press('enter')
    
    4. Done, Now you can use this function    
    """
    import pywhatkit as kit

    kit.sendwhatmsg(to,content)
    sleep(5)

    sql = curAssisnat.execute(f"SELECT * FROM friends WHERE name = '{to}'")
    result = sql.fetchall()

    while True:
        more = speak(f"message send! sir, do you want send some message to {result[0][0]}.")
        if "no" in more:
            break
        else:
            try:
                more.replace("send","")
            except:
                pass
            try:
                more.replace("type","")
            except:
                pass
            kit.sendwhatmsg(to,more)
            sleep(1)
    return

def vscode():
    """
    open vscode
    :return:
    """
    import os
    # You have to provide the path of your vscode here
    path = "C:\\Users\\PARSHANT\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
    os.startfile(path)
    return

def pycharm():
    """
    Open pycharm
    :return:
    """
    import os
    # You have to provide the path of your pycharm here

    path = "C:\\Program Files\\JetBrains\\PyCharm Community Edition 2020.1.2\\bin\\pycharm64.exe"
    os.startfile(path)
    return

def mail(to,subject,contant):
    """
    Send mail to any person.
    First it check email address in mailFriends dictionary if address is not found then it ask for address and to store
    it for next time
    :param to:
    :param subject:
    :param contant:
    :return:
    """

    """
    Before using this feature you have to make some changes in your google gmail accunt. Follow simple steps:-
    1. cllick on given url : https://myaccount.google.com/lesssecureapps or you can search for (less secure apps) in google then enter on first link given by google
    2. Turn on - allow less secure app
    3. Done, Now you can use this feature
    """

    import smtplib
    from email.message import EmailMessage
    try:
        msg = EmailMessage()
        if subject == "none" or subject == "empty" or subject == "blank" or subject == "nothing":
            pass
        else:
            msg["Subject"] = subject
        # Enter your email id and password
        email_id = "YOUR_EMAIL_ID"
        pswd = "YOUR_PASSWORD"

        msg["From"] = email_id
        msg["To"] = to
        msg.set_content(contant)
        with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:

            smtp.login(email_id,pswd)
            smtp.send_message(msg)
            engine.say("mail sent")
            engine.runAndWait()
    except Exception as e:
        if "getaddrinfo" in e:
            text = speak("network error please try after some time")
        else:
            text = speak("somthing went wrong please try again")
        return text
    return

def time_now():
    """
    Speaks current time
    :return:
    """
    from time import strftime
    engine.say(strftime("%H:%M"))
    engine.runAndWait()
    return

def talk():
    import random
    rnd = random.choice(("I am fine. How are you?", "I am good. How are you?",
                         "I am good. What about you?", "Good to hear from you,I am good. What about you?",
                         "Pretty good. How about you?", "I'm fine, thank you. And you?"))
    text = speak(rnd)
    fineList = ["i am fine", "i am also fine", "i am good", "pretty good",
                "good to hear from you i am good"]
    for rst in fineList:
        if rst in text:
            rnd1 = random.choice(("Good", "Great", "I am glad to hear that"))
            rnd2 = random.choice(("What can i do for You", "How may,I help you", "What next ?"))
            text = speak(rnd1 + ", " + rnd2)
    fineList = ["Who are you ?", "What's your name?"]
    for rst in fineList:
        if rst in text:
            rnd1 = random.choice(("I am Jarvis", "My name is Jarvis", "You can call me Jarvis"))
            text = speak(rnd1)
    fineList = ["Tell me a joke", "Make me laugh", "Tell me something funny"]
    for rst in fineList:
        if rst in text:
            rnd1 = random.choice(("Why do we tell actors to 'break a leg?' Because every play has a cast",
                                  "Hear about the new restaurant called Karma? There’s no menu : You get what you deserve.",
                                  "Why don’t Calculus majors throw house parties? Because you should never drink and derive.",
                                  "What did the bald man exclaim when he received a comb for a present? Thanks— I’ll never part with it!",
                                  "What did the left eye say to the right eye? Between you and me, something smells.",
                                  "What did the 0 say to the 8? Nice belt!",
                                  "What do you call a pony with a cough? A little horse.",
                                  "What did one hat say to the other? You wait here.I’ll go on a head.",
                                  "What do you call a magic dog? A labracadabrador.",
                                  "What did the shark say when he ate the clownfish? This tastes a little funny."
                                  ))
            text = speak(rnd1)
    fineList = [""]

def todays_headline():
    """
    Read top today's headline from google news
    :return:
    """
    from bs4 import BeautifulSoup as soup
    from urllib.request import urlopen

    news_url = "https://news.google.com/news/rss"
    Client = urlopen(news_url)
    xml_page = Client.read()
    Client.close()

    soup_page = soup(xml_page, "xml")
    news_list = soup_page.findAll("item")
    i = 0
    for news in news_list:
        i += 1
        engine.say(news.title.text)
        engine.runAndWait()
        if i == 8:
            break
    return

def get_event():
    """
    Get events from google calendar
    :return:
    """
    from num2words import num2words as nw
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import pickle
    import datetime
    if_event = False
    nowee = timee()

    SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # You have to dwonload client_secret.json file of you google api and give path here
            flow = InstalledAppFlow.from_client_secrets_file(
                "c:\\Users\\PARSHANT\\Downloads\\client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        engine.say("No upcoming events found.")
        engine.runAndWait()
    for event in events:
        start = event['start'].get('dateTime')
        start = str(start)
        start = start.split("-")
        start = start[2].split("T")
        print(start[0])
        print(nowee[2])
        if start[0] == nowee[2]:
            if_event = True
            event_type = event["kind"]
            event_type  = str(event_type).split("#")
            engine.say(f"You have an {event_type[1]} at {nw(int(nowee[3])),nw(int(nowee[4]))} and {event_type[1]} summary is {event['summary']}")
            engine.runAndWait()
            try:
                event_location = event['location']
                try:
                    event_location = str(event_location).split(str(1))
                except:
                    pass
                engine.say(f"location is {event_location[0]}")
                engine.runAndWait()
            except:
                pass
            try:
                engine.say(f"description is {event['description']}")
                engine.runAndWait()
            except:
                pass
        if if_event == False:
            engine.say("You don't have any events or reminder")
            engine.runAndWait()

def set_event():
    """
    Set event in google calendar
    :return:
    """
    import datefinder
    from datetime import datetime, timedelta
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import pickle
    from time import strftime

    SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # You have to dwonload client_secret.json file of you google api and give path here
            flow = InstalledAppFlow.from_client_secrets_file(
                "c:\\Users\\PARSHANT\\Downloads\\client_secret.json",SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)

    # Enent startint time
    start_time_str = speak("Please prefer any date and time")
    if "today" in text or "for today" in start_time_str:
        event_time = start_time_str.split("at ")
        try:
            event_time = event_time[1].replace(" ", "")
        except:
            pass
        # setting up time
        start_time_str = timee()
        monthsNumToWord = {
            "01": "Jan",
            "02": "Feb",
            "03": "Mar",
            "04": "apr",
            "05": "may",
            "06": "jun",
            "07": "jul",
            "08": "aug",
            "09": "sep",
            "10": "oct",
            "11": "nov",
            "12": "dec"
        }
        start_time_str = str(start_time_str[1])
        start_time_str = monthsNumToWord[start_time_str]
        start_time_str = strftime(
            "%Y-" + start_time_str + "-%d at " + event_time[0] + event_time[1] + ":" + event_time[2] +
            event_time[3])
    elif "tommmorrow" in start_time_str:
        event_time = start_time_str.split("at ")
        try:
            event_time = event_time[1].replace(" ", "")
        except:
            pass
        # setting up time
        start_time_str = timee()
        monthsNumToWord = {
            "01": "Jan",
            "02": "Feb",
            "03": "Mar",
            "04": "apr",
            "05": "may",
            "06": "jun",
            "07": "jul",
            "08": "aug",
            "09": "sep",
            "10": "oct",
            "11": "nov",
            "12": "dec"
        }
        start_time_str = str(start_time_str[1])
        start_time_str = monthsNumToWord[start_time_str]
        date = int(strftime("%d")) + 1
        start_time_str = strftime(
            "%Y-" + start_time_str + "-" + str(date) + " at " + event_time[0] + event_time[1] + ":" +
            event_time[2] + event_time[3])
    else:
        event_time = None
        start_time_str = start_time_str.split("at ")
        try:
            event_time = start_time_str[1].replace(" ", "")
        except:
            pass
        start_time_str = start_time_str[0] + event_time[0] + event_time[1] + ":" + event_time[2] + event_time[3]
    # setting up time
    start_time = list(datefinder.find_dates(start_time_str))
    start_time = str(start_time[0])
    start_time = start_time.replace("-", ":")
    start_time = start_time.replace(" ", ":")
    start_time = start_time.split(":")
    start_time = datetime(int(start_time[0]), int(start_time[1]), int(start_time[2]), int(start_time[3]),
                          int(start_time[4]), int(start_time[5]))

    # Event ending time
    end_time_str = speak("Event ending time or duration?")
    if "hours" in end_time_str:
        end_time_str = end_time_str.replace(" ", "")
        end_time_str = end_time_str.split("hours")
        end_time_str = end_time_str[0]
        try:
            end_time_str1 = int(end_time_str[-2])
            end_time_str = str(end_time_str1) + end_time_str[-1]
            end_time = start_time + timedelta(hours=int(end_time_str))
        except:
            end_time_str = end_time_str[-1]
            end_time = start_time + timedelta(hours=int(end_time_str))
    else:
        end_time =  start_time + timedelta(hours=1)

    # Event summary...
    summary = speak("Event summary?")

    # Event description...
    description = speak("Eny description for event")
    if "none" in description or "negative" in description or "blank" in description or "empty" in description:
        description = None

    # Event location...
    location = speak("event location?")
    if "none" in location or "negative" in location or "blank" in location or "empty" in location:
        location = None
    else:
        try:
            location.replace(" ","/")
        except:
            pass

    # Event timezone...
    time_zone = speak("Ant time zone do you want to set")
    if "none" in time_zone or "negative" in time_zone or "blank" in time_zone or "empty" in time_zone:
        time_zone = "Asia/Kolkata"
    # All Event
    event = {
        "summary":summary,
        "location":location,
        "description":description,
        "start":{
            "dateTime":start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "timeZone":time_zone
        },
        "end":{
            "dateTime":end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "timeZone":time_zone
        },
        # you can set reminders here
        "reminder":{
            "useDefault":False,
            "overrides":[
                {"method": "email", "minutes": 60},
                {"method": "email", "minutes": 3*60},
                {"method": "popup", "minutes": 10},
            ]
        }
    }

    # Executing event to calendar
    service.events().insert(calendarId='primary', body=event).execute()

if __name__ == "__main__":
    class_date_time = None
    class_name = None
    start()
    while True:
        text = reco()
        text = text.lower()
        print(f"{text}")
        if "jarvis" in text:
            text = text.split("jarvis ")
            text = text[1]
            print(text)
            #Task handling...

            # wikipedia and give results direct
            if "wikipedia" in text or "wiki" in text:
                engine.say("Searching wikipedia...")
                engine.runAndWait()
                # removing extra struff for best search
                try:
                    text = text.replace("wikipedia","")
                except:
                    pass
                try:
                    text = text.replace("wiki","")
                except:
                    pass
                try:
                    text = text.replace("jarvis","")
                except:
                    pass
                try:
                    text = text.replace("from","")
                except:
                    pass
                try:
                    text = text.replace("according to","")
                except:
                    pass

                wiki(text)
                reco()

            # google
            elif "search" in text or "search for" in text:
                try:
                    text = text.replace("jarvis","")
                except:
                    pass
                try:
                    text = text.replace("search","")
                except:
                    pass
                try:
                    text = text.replace("for","")
                except:
                    pass

                google(text)
                reco()

            # open youtube and ask for song
            elif "play music on youtube" in text:
                song_name = speak("please enter song name!")
                youtube(song_name)
                reco()

            #open youtube and play song
            elif "play" in text and "on youtube" in text:
                try:
                    text = text.split("play ")
                    text = text[1].split(" on youtube")
                    text = text[0]
                    youtube(text)
                except:
                    pass
                reco()

            # sending message on whatsapp
            elif "send message" in text or "whatsapp" in text:
                try:
                    text = text.split("to ")
                    text = text[1]

                    sql = curAssisnat.execute(f"SELECT * FROM friends WHERE name = '{text}'")
                    result = sql.fetchall()
                    # if name is not found
                    if len(result) == 0:
                        while True:
                            to = speak("you don't have number please enter a number")
                            try:
                                to = to.replace(" ", "")
                            except:
                                pass

                            for value in to:
                                engine.say(value)
                                engine.runAndWait()
                            cnf = speak("Do you want to confirm if not say no or retype")
                            if "confirm" in cnf:
                                store = speak("Do you want to store this number for next time")
                                if "yes" in store:
                                    if "+91" in to:
                                        to = to.split("+91")
                                        to = to[1]

                                    curAssisnat.execute("INSERT INTO friends(name,phone) VALUES(?,?)", (text, int(to)))
                                msg_content = speak("what do you want to send")
                                whatsapp("+91" + to, msg_content)
                                break
                            elif "retype" in cnf or "retype number" in cnf:
                                continue
                            elif "cancel" in cnf:
                                break

                    # if name is in data btu number is not
                    elif result[0][2] == None:
                        while True:
                            to = speak("you don't have number please enter a number")
                            try:
                                to = to.replace(" ", "")
                            except:
                                pass

                            for value in to:
                                engine.say(value)
                                engine.runAndWait()
                            cnf = speak("Do you want to confirm if not say no or retype")
                            if "confirm" in cnf:
                                store = speak("Do you want to store this number for next time")
                                if "yes" in store:
                                    if "+91" in to:
                                        to = to.split("+91")
                                        to = to[1]
                                    sql = curAssisnat.execute(f"SELECT * FROM friends WHERE name = '{text}'")
                                    result = sql.fetchall()
                                    mail_id = result[0][1]
                                    curAssisnat.execute(f"DELETE FROM friends WHERE name = '{text}'")
                                    curAssisnat.execute(f"REPLACE INTO friends(name,mail,phone) VALUES(?,?,?) ",
                                            (text, mail_id, to))
                                    assistant.commit()
                                    del mail_id
                                    msg_content = speak("what do you want to send")
                                    whatsapp("+91" + to, msg_content)
                                    break
                                elif "retype" in cnf or "retype number" in cnf:
                                    continue
                                elif "cancel" in cnf:
                                    break

                    else:
                        msg_content = speak("what do you want to send")
                        whatsapp("+91"+result[0][2],msg_content)
                        continue

                    if "cancel" in cnf:
                        engine.say("Task cancel")
                        engine.runAndWait()
                        continue
                except:
                    pass
                reco()

            # opening code
            elif "open code" in text:
                vscode()
                reco()

            #opening pycharm
            elif "open pycharm" in text:
                pycharm()
                reco()

            # Sending mail
            elif "send mail to" in text or "write mail to" in text\
                    or "send gmail to" in text or "write gmail to" in text:
                print("ess")
                try:
                    text = text.split("to ")
                    text = text[1]
                    sql = curAssisnat.execute(f"SELECT * FROM friends WHERE name = '{text}'")
                    result = sql.fetchall()
                    if len(result) == 0:
                        while True:
                            to = speak("you don't have email address!!! please enter email address")
                            try:
                                to.replace(" ","")
                            except:
                                pass
                            engine.say("You enter...")
                            engine.runAndWait()
                            for value in to:
                                engine.say(value)
                                engine.runAndWait()
                            cnf = speak("Please confirm! to send!... or retype or cancel")
                            if cnf == "confirm":
                                store = speak("Do you want to store this address for next time")
                                if "yes" in store:
                                    curAssisnat.execute("INSERT INTO friends(name,mail) VALUES(?,?)", (text,to))

                                subject = speak("Enter enter any subject")
                                contant = speak("Enter content for mail")
                                text = mail(to,subject,contant)
                                break
                            elif "retype" in cnf or "retype number" in cnf:
                                continue
                            elif "cancel" in cnf:
                                break

                    elif result[0][1] == None:
                        to = speak("you don't have email address!!! please enter email address")
                        while True:
                            to = speak("you don't have email address!!! please enter email address")
                            try:
                                to.replace(" ", "")
                            except:
                                pass
                            engine.say("You enter...")
                            engine.runAndWait()
                            for value in to:
                                engine.say(value)
                                engine.runAndWait()
                            cnf = speak("Please confirm! to send!... or retype or cancel")
                            if cnf == "confirm":
                                store = speak("Do you want to store this address for next time")
                                if "yes" in store:
                                    sql = curAssisnat.execute(f"SELECT * FROM friends WHERE name = '{text}'")
                                    result = sql.fetchall()
                                    phn_no = result[0][2]
                                    curAssisnat.execute(f"DELETE FROM friends WHERE name = '{text}'")
                                    curAssisnat.execute(f"REPLACE INTO friends(name,mail,phone) VALUES(?,?,?) ",
                                                        (text, to, phn_no))
                                    assistant.commit()

                                subject = speak("Enter enter any subject")
                                contant = speak("Enter content for mail")
                                text = mail(to, subject, contant)
                                break
                            elif "retype" in cnf or "retype number" in cnf:
                                continue
                            elif "cancel" in cnf:
                                break

                    else:
                        subject = speak("Enter enter any subject")
                        contant = speak("Enter content for mail")
                        text = mail(result[0][1], subject, contant)
                        continue

                    if "cancel" in cnf:
                        engine.say("Task cancel")
                        engine.runAndWait()
                        continue
                except:
                    pass

            #time
            elif "what is the time" in text or "time please" in text\
                    or "time now" in text or "time please" in text:
                time_now()
                reco()

            # open any site
            elif "open site" in text:
                try:
                    text = text.split("open site")
                    text = text[1]
                except:
                    pass
                try:
                    text = text.replace(" ","")
                except:
                    pass
                googleSites(text)

            elif "how are you" in text:
                talk()

            elif "today's headline" in text or "today headlines" in text\
                    or "today headline" in text or "today's headline" in text:
                todays_headline()

            elif "set reminder" in text or "set event" in text:
                set_event()

            elif "any reminder for today" in text or "today's reminder" in text\
                    or "any work for today" in text or "today's event" in text:
                print("yes")
                get_event()

        else:
            continue