Introduction
J.A.R.V.I.S. (Just A Rather Very Intelligent System) is a voice-activated virtual assistant built in Python. This program can perform a variety of tasks, including opening applications, playing music, fetching real-time information, and more, all through voice commands. The project is designed to be a personal assistant for Windows operating systems.

Features
Voice Interaction: Uses pyttsx3 for text-to-speech output and SpeechRecognition to listen to and interpret user commands.

Facial Recognition: Integrates with OpenCV to detect and save a photo of the user's face upon startup. This feature provides a personalized welcome.

System Control: Allows users to lock or shut down their PC using simple voice commands.

Application Management: Can open and close common applications like Microsoft Word, Excel, and Chrome, as well as specific websites.

Information Retrieval: Fetches and reads news headlines and Wikipedia summaries.

Real-time Data: Gets the current time, date, and weather for a specified city using the OpenWeatherMap API.

Media and Automation:

Plays random songs from a designated music folder.

Sends WhatsApp messages to predefined contacts.

Reads PDF or TXT files from a specified folder.

Takes screenshots and adjusts system volume using pyautogui.

Multi-threading: Uses the threading module for features like the alarm function, allowing the assistant to continue listening for commands while the alarm is set to ring at the specified time.

Requirements
To run J.A.R.V.I.S., you'll need to install the following Python libraries:

SpeechRecognition

pyttsx3

wikipedia

requests

pyautogui

pywhatkit

PyPDF2

opencv-python

pyaudio (required for SpeechRecognition)

You can install all these packages at once using pip:

pip install SpeechRecognition pyttsx3 wikipedia requests pyautogui pywhatkit PyPDF2 opencv-python PyAudio
Setup and Configuration
Before running the code, you must configure a few things to ensure all features work correctly:

API Keys:

News API: Get an API key from NewsAPI and replace "YOUR_NEWS_API_KEY" in the tell_news() function.

OpenWeatherMap API: Get an API key from OpenWeatherMap and replace "YOUR_OPENWEATHER_API_KEY" in the get_temperature() function.

File Paths:

Update the music_folder variable in the play_music() function to the correct path of your music directory.

Ensure the read_document() function's paths (path_pdf and path_txt) point to the correct directory where your documents are stored.

Verify the screenshot path in automate_task().

WhatsApp Contacts:

Modify the nums dictionary in the send_whatsapp_message() function to include your desired contacts and their phone numbers. The numbers must include the country code (e.g., "+91").

pywhatkit setup:

When you run the code and use the "send WhatsApp message" command for the first time, pywhatkit will open a web browser. You'll need to manually log in to WhatsApp Web by scanning the QR code with your phone. Once logged in, pywhatkit can send messages automatically.

How to Run
Save the code: Save the provided code as a Python file (e.g., jarvis.py).

Open a terminal: Navigate to the directory where you saved the file.

Execute the script: Run the command: python jarvis.py

The program will start by initializing its components and will prompt you to press 'q' to skip face detection. Upon successful startup, it will greet you and wait for a command.

Voice Commands
Here are some of the commands J.A.R.V.I.S. understands:

"what is the time"

"what is the date"

"wikipedia [topic]" (e.g., "wikipedia Albert Einstein")

"news" or "fresh news"

"open [app/site]" (e.g., "open youtube", "open word")

"close [app]" (e.g., "close chrome", "close calculator")

"temperature [city]" (e.g., "temperature Delhi")

"play song" or "music"

"send message" or "whatsapp"

"set alarm"

"read document" or "read pdf"

"lock pc"

"shutdown pc"

"screenshot"

"volume up"

"volume down"

"exit" or "quit"