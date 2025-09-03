import os
import sys
import subprocess
import webbrowser
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import requests
import pyautogui
import time
import random
import pywhatkit
import PyPDF2
import cv2
from datetime import datetime as dt
import threading

#for detect the face and save the image 
def detect_and_save_face():
    folder_name = "captured_images"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        # draw rectangles
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow("Face Detection — Press 'q' to skip", frame)

        if len(faces) > 0:
            timestamp = dt.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = os.path.join(folder_name, f"face_capture_{timestamp}.jpg")
            cv2.imwrite(filename, frame)
            print(f"[INFO] Image saved as {filename}")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[INFO] Face detection skipped by user.")
            break

    cap.release()
    cv2.destroyAllWindows()
# for speak the text
engine = pyttsx3.init()
engine.setProperty('rate', 175)
voices = engine.getProperty('voices')
voice = engine.setProperty('voice', voices[1].id)

def speak(text):
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()
# for greeting the user
def wish_user():
    h = datetime.datetime.now().hour
    if h < 12:
        speak("Good Morning!")
    elif h < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am JARVIS. How can I assist you?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as src:
        r.pause_threshold = 1
        audio = r.listen(src)
    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that.")
        return "none"
    except sr.RequestError:
        speak("Speech service is down.")
        return "none"

def open_application(name):
    # ensure Chrome is registered
    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

    sites = {
        "youtube": "https://www.youtube.com",
        "chatgpt": "https://chat.openai.com",
        "youtube music": "https://music.youtube.com",
        "classroom": "https://classroom.google.com",
        "map": "https://maps.google.com",
    }
    apps = {
        "word": "winword.exe",
        "excel": "excel.exe",
        "powerpoint": "powerpnt.exe",
        "calculator": "calc.exe",
        "store": "ms-windows-store:",
        "whatsapp": "whatsapp.exe",
    }

    if name in sites:
        webbrowser.get('chrome').open(sites[name])
        speak(f"Opening {name} on Chrome.")
    elif name in apps:
        subprocess.Popen(apps[name], shell=True)
        speak(f"{name} launched.")
    else:
        speak(f"App or site '{name}' not recognized.")

def close_application(name):
    procs = {
        "word": "WINWORD.EXE",
        "excel": "EXCEL.EXE",
        "powerpoint": "POWERPNT.EXE",
        "calculator": "Calculator.exe",
        "whatsapp": "WhatsApp.exe",
        "chrome": "chrome.exe"
    }
    if name in procs:
        subprocess.call(
            ["taskkill","/f","/im",procs[name]],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        speak(f"{name} closed.")
    else:
        speak(f"Cannot close '{name}'.")

def tell_news():
    api_key = "YOUR_NEWS_API_KEY"
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    try:
        articles = requests.get(url).json()["articles"][:5]
        speak("Here are today's top headlines.")
        for i,a in enumerate(articles,1):
            speak(f"News {i}: {a['title']}")
    except:
        speak("Unable to fetch news.")

def search_wikipedia():
    speak("Searching Wikipedia. What is the topic?")
    topic = take_command()
    if topic != "none":
        try:
            res = wikipedia.summary(topic, sentences=2)
            speak("According to Wikipedia:")
            speak(res)
        except:
            speak("Topic not found.")

def get_temperature():
    speak("Tell me the city.")
    city = take_command()
    if city != "none":
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=YOUR_OPENWEATHER_API_KEY&units=metric"
            temp = requests.get(url).json()["main"]["temp"]
            speak(f"The temperature in {city} is {temp}°C")
        except:
            speak("Cannot get temperature.")

def play_music():
    music_folder = "C:\\Users\\Dell\\Music"
    songs = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]
    if songs:
        choice = random.choice(songs)
        os.startfile(os.path.join(music_folder, choice))
        speak(f"Playing {choice}")
    else:
        speak("No music files found.")

def send_whatsapp_message():
    speak("Who? Say 'one' or 'two'.")
    c = take_command()
    nums = {"one":"+917088348992", "two":"+917078260045"}
    if c in nums:
        speak("What is your message?")
        msg = take_command()
        now = datetime.datetime.now()
        pywhatkit.sendwhatmsg_instantly(nums[c], msg)
        speak("Message sent.")
    else:
        speak("Contact not recognized.")

def set_alarm():
    speak("Set hour for alarm.")
    h = int(take_command())
    speak("Set minute.")
    m = int(take_command())
    speak(f"Alarm set for {h}:{m}.")
    def ring():
        while True:
            if dt.now().hour==h and dt.now().minute==m:
                speak("Wake up! Alarm ringing.")
                break
            time.sleep(30)
    threading.Thread(target=ring).start()

def read_document():
    speak("Enter the PDF or TXT filename (without extension).")
    name = input("File name: ")
    path_pdf = f"C:\\Users\\Dell\\Documents\\{name}.pdf"
    path_txt = f"C:\\Users\\Dell\\Documents\\{name}.txt"
    if os.path.exists(path_pdf):
        reader = PyPDF2.PdfReader(path_pdf)
        text = "".join(page.extract_text() for page in reader.pages[:2])
        speak(text)
    elif os.path.exists(path_txt):
        with open(path_txt) as f:
            speak(f.read()[:500])
    else:
        speak("File not found.")

def automate_task(task):
    if "screenshot" in task:
        p = f"C:\\Users\\Dell\\Pictures\\Screenshots\\screenshot_{time.strftime('%Y%m%d-%H%M%S')}.png"
        pyautogui.screenshot().save(p)
        speak("Screenshot taken.")
    elif "volume up" in task:
        pyautogui.press("volumeup"); speak("Volume up.")
    elif "volume down" in task:
        pyautogui.press("volumedown"); speak("Volume down.")

def handle_command(cmd):
    if "what is the time" in cmd:
        speak(datetime.datetime.now().strftime("%H:%M:%S"))
    elif "what is the date" in cmd:
        speak(datetime.datetime.now().strftime("%A, %d %B %Y"))
    elif "wikipedia" in cmd:
        search_wikipedia()
    elif "news" in cmd or "fresh news" in cmd:
        tell_news()
    elif "open" in cmd:
        open_application(cmd.replace("open","").strip())
    elif "close" in cmd:
        close_application(cmd.replace("close","").strip())
    elif "temperature" in cmd:
        get_temperature()
    elif "play song" in cmd or "music" in cmd:
        play_music()
    elif "send message" in cmd or "whatsapp" in cmd:
        send_whatsapp_message()
    elif "set alarm" in cmd:
        set_alarm()
    elif "read document" in cmd or "read pdf" in cmd:
        read_document()
    elif "lock pc" in cmd:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        speak("PC locked.")
    elif "shutdown pc" in cmd:
        os.system("shutdown /s /t 5"); speak("Shutting down.")
    elif cmd in ("exit","quit"):
        speak("Goodbye!"); sys.exit()
    else:
        automate_task(cmd)


if __name__ == "__main__":
    detect_and_save_face()   
    wish_user()             
    while True:
        command = take_command()
        if command != "none":
            handle_command(command)
