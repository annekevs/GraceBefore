import faulthandler
faulthandler.enable()
import pyttsx3
import speech_recognition as sr
from decouple import config
from datetime import datetime
from random import choice

#also install espeak

#USERNAME = "Melchi"
#BOTNAME = "GRACE"

USERNAME = config('USER')
BOTNAME = config('BOTNAME')

engine = pyttsx3.init()
# Set Rate
engine.setProperty('rate', 180)
# Set Volume
engine.setProperty('volume', 1.0)
# Set Voice (Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[29].id)

#for index, voice in enumerate(voices):
 #print(index, voice)

# default 11 (english)
# english_us 17 (12 - 18)
# spanish 20
# french 29 (28 : french_belgium)
# italien 41

# Text to Speech Conversion
def speak(text):
    """Used to speak whatever text is passed to it"""

    engine.say(text)
    engine.runAndWait()

#speak("Hello, my name is GRACE. I'm happy to meet you !")
speak("Bonjour, je m'appelle Grace. Qu'est ce que je peux faire pour vous ?")
#speak("Bongiorno, mi chiamo Grace. Che poi fare per te ?")

def change_voice(engine, language, gender='male'):
    for voice in engine.getProperty('voices'):
        if language == voice.name:
            engine.setProperty('voice', voice.id)
            return True

    raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))

#change_voice(engine, "french")
#engine.say("Bonjour")
#engine.runAndWait()

# Greet the user
def greet_user():
    """Greets the user according to the time"""
    hour = datetime.now().hour
    if (hour >= 1) and (hour < 12):
        speak(f"Bonjour {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Bon après-midi {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Bonsoir {USERNAME}")
    speak(f"Je suis {BOTNAME}. Comment puis je vous aider ?")

# Takes Input from User
def take_user_input():
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('A votre écoute....')
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print('Traitement...')
        query = r.recognize_google(audio, language='french')
        if not 'exit' in query or 'stop' in query:
            speak(choice(opening_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Bonne nuit {USERNAME}, À plus tard!")
            else:
                speak('Bonne journée !')
            exit()
    except Exception:
            speak('Désolé, Je ne comprends pas. Pouvez-vous repeter s\'il vous plaît?')
            query = 'None'
    return query

opening_text = [
    "D'accord monsieur, J\'y travaille.",
    "D'accord monsieur,J'\y travaillle.",
    "Un instant s'il vous plaît.",
]

if __name__ == '__main__':
    greet_user()
#    while True:
#        query = take_user_input().lower()
#        print(query)
