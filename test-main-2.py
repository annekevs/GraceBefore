import pyttsx3
import speech_recognition as sr
from decouple import config
from datetime import datetime
from random import choice
from functions.os_ops import open_firefox, open_libreoffice
from functions.online_ops import find_my_ip, search_on_google, search_on_wikipedia
from pprint import pprint

# get global variables
USERNAME = config('USER')
BOTNAME = config('BOTNAME')

opening_text = [
    "D'accord, j'y travaille.",
    "Un instant s'il vous plait.",
]

# init text-to-speech
engine = pyttsx3.init()
engine.setProperty("rate", 180)
engine.setProperty("volume", 1.0)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[29].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

#speak("Bonjour, je m'appelle GRACE. Comment puis-je vous aider?")

def greet_user():
    """Greets the user according to the time"""
    
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Bonjour {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Bon après-midi {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Bonsoir {USERNAME}")
    speak(f"Je suis {BOTNAME}. Comment puis-je vous aider?")

def take_user_input():
    # init speech recognition
    r = sr.Recognizer()
    m = sr.Microphone()
    
    try:
        print("Un moment de silence, s'il vous plaît...")
        with m as source: r.adjust_for_ambient_noise(source)
        print("Le seuil minimal d'energie est de {}".format(r.energy_threshold))
        with m as source: r.adjust_for_ambient_noise(source)
        print("Dites quelque chose! --- {}".format(r.energy_threshold))
        with m as source: audio = r.listen(source)
        print("C'est bon! reconnaissance vocale...")
        try:
            # recognize speech using Google Speech Recognition
            query = r.recognize_google(audio, language="fr-FR")
            print("Vous avez dit {}".format(query))
            if not "au revoir" in query or "aurevoir" in query or "stop" in query:
                speak(choice(opening_text))
            else:
               	hour = datetime.now().hour
               	if hour >= 21 and hour < 6:
               	    speak('Bonne nuit {USERNAME}, à demain!')
               	else:
           	    	speak("Bonne journée, à plus tard !")
               	exit()
        except sr.UnknownValueError:
            speak("Oops! Je n'ai pas bien compris. Pouvez-vous repetez ?")
            query = None
        except sr.RequestError as e:
            speak("Désole, le service est momentanement indisponible {0}".format(e))
            query = None
    except Exception:
        speak("Oops! Une erreur est survenue. Veuillez repetez s'il vous plait!")
        query = None
    return query
                
if __name__ == '__main__':
    greet_user()
    while True:
        query = take_user_input().lower()
        
        if 'firefox' in query:
            open_firefox()
        elif 'libre office' in query:
            open_libreoffice()
        elif 'recherche' in query:
            speak("Qu'est ce que je dois chercher madame ?")
            search_query = take_user_input().lower()
            results = search_on_wikipedia(search_query)
            #speak(f"Selon Wikipedia, {results}")
            speak("Permettez moi d'afficher les résultats à l'écran")
            print(results)
        elif 'adresse IP' in query:
            ip_address = find_my_ip()
            speak(f"Votre adresse IP est {ip_address}.\n Je l'affiche à l'écran")
        else:
            speak("Désolé, je n'ai pas l'autorisation d'effectuer cette tâche.")   


