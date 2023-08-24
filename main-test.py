import pyttsx3
import speech_recognition as sr
from decouple import config
from datetime import datetime
from random import choice

# get global variables
USERNAME = config('USER')
BOTNAME = config('BOTNAME')

opening_text = [
    "D'accord, j'y travaille.",
    "Un instant s'il vous plait.",
]

# init text-to-speech
engine = pyttsx3.init()
# on windows
# engine = pyttsx3.init("sapi5")
engine.setProperty("rate", 180)
engine.setProperty("volume", 1.0)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[29].id)

# Text to Speech Conversion
def speak(text):
    """Used to speak whatever text is passed to it"""    
    
    engine.say(text)
    engine.runAndWait()
    
# Greet the user
def greet_user():
    """Greets the user according to the time"""
    
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening {USERNAME}")
    speak(f"I am {BOTNAME}. How may I assist you?")

# Takes Input from User
def take_user_input():
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""
    
    r = sr.Recognizer()
    m = sr.Microphone()
    
	try:
		print("Un moment de silence, s'il vous plaît...")
		with m as source: r.adjust_for_ambient_noise(source)
		print("Le seuil minimal d'energie est de {}".format(r.energy_threshold))
		
		# listen to the user
		print("Dites quelque chose! --- {}".format(r.energy_threshold))
		with m as source: audio = r.listen(source)
		print("C'est bon! reconnaissance vocale...")

		try:
			# recognize speech using Google Speech Recognition
			query = r.recognize_google(audio, language="fr-FR")
			
			if not "au revoir" in query or "aurevoir" in query or "stop" in query:
				speak(choice(opening_text))
			else:
				hour = datetime.now().hour
				if hour >= 21 and hour < 6:
				    speak('Bonne nuit {USERNAME}, à demain!')
				else:
				    speak('Bonne journée {USERNAME}!')
				exit()

		except sr.UnknownqueryError:
			speak("Oops! Je n'ai pas bien compris. Pouvez-vous repetez s'il vous plaît?")
			query = none
		except sr.RequestError as e:
			speak("Désole, le service est momentanement indisponible {0}".format(e))
			query = none
	except Exception:
		speak("Oops! Je n'ai pas bien compris. Pouvez-vous repetez s'il vous plaît?")	
		query = none
	return query

if __name__ == '__main__':
    greet_user()
    while True:
        query = take_user_input().lower()
        print(query)
        speak("Vous avez dit {}".format(query))	
		
		except KeyboardInterrupt:
			pass
	

