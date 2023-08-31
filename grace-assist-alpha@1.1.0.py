from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
from tkinter.messagebox import *
import pyttsx3
import speech_recognition as sr
from decouple import config
from datetime import datetime
from random import choice
from pprint import pprint
import time

import os
import sys
import subprocess as sp
import requests
import wikipedia
import pywhatkit as kit

def search_on_google(query):
    kit.search(query)

def search_on_wikipedia(query):
    try:
        results = wikipedia.summary(query, sentences=2)
    except Exception:
        results = "Probleme de connexion"
    return results

def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]


# Path above are for windows applications
paths = {
    'calculator': "C:\\Windows\\System32\\calc.exe",
    'sublime': "    C:\\Program Files\\Sublime Text\\sublime_text.exe"
}

def open_sublime_text():
    os.startfile(paths['sublime'])

def open_calculator(): 
    sp.Popen(paths['calculator'])

def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)

def open_terminal(): 
    os.system('start cmd')

# get global variables
USERNAME = "Anne"
BOTNAME = "GRACE"
CIVILITE = "madame"

opening_text = [
	"D'accord, j'y travaille."
]

# init text-to-speech
engine = pyttsx3.init("sapi5")
engine.setProperty("rate", 190)
engine.setProperty("volume", 1.0)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

def speak(text):
	engine.say(text)
	engine.runAndWait()

#speak("Bonjour, je m'appelle GRACE. Comment puis-je vous aider?")

def greet_user():
	"""Greets the user according to the time"""
	
	hour = datetime.now().hour
	if (hour >= 1) and (hour < 16):
		speak(f"Bonjour {CIVILITE}")
	# elif (hour >= 12) and (hour < 16):
	# 	speak(f"Bon après-midi {USERNAME}")
	elif (hour >= 16) and (hour < 19):
		speak(f"Bonsoir {CIVILITE}")
	speak(f"Je m'appelle {BOTNAME}. Votre nouvelle assistante virtuelle.\n\n Ravie de faire votre connaissance !")

def bye_user():
	hour = datetime.now().hour
	if hour >= 21 and hour < 6:
		speak('Bonne nuit, à demain!')
	else:
		speak("Bonne journée, à plus tard !")
	#exit()
	#go_to_start();

####################################################
# create a window
window = Tk()
window["bg"]= "white"
window.iconbitmap("grace_icon.ico")
window.title("Grace -alpha@1.1.0 | starter")
window.geometry("600x500")

font1 = font.Font(family='Georgia', size='22', weight='bold')
font2 = font.Font(family='Aerial', size='12')

# PhotoImage supports the GIF, PGM, PPM, and PNG file formats
#photo = PhotoImage(file="./grace_vector.jpg")
# canvas = Canvas(window,width=350, height=200)
# canvas.create_image(0, 0, anchor=NW, image=photo)
# canvas.pack()

# create all the frames
fr_start = Frame(window, borderwidth=2, relief="flat")
fr_initialisation =  Frame(window, borderwidth=2, relief="flat")
fr_home = Frame(window, borderwidth=2, relief="flat")
fr_quit = Frame(window, borderwidth=2, relief="flat")

########################### pyttsx3 module ############################3
def take_user_input(done):
	# init speech recognition
	r = sr.Recognizer()
	m = sr.Microphone()
	
	try:
		if not done == True:
			speak("Un instant s'il vous plait...")
			with m as source: r.adjust_for_ambient_noise(source)
			#speak("Dites quelque chose! --- {}".format(r.energy_threshold))
			speak("Qu'est ce que je dois faire ?")
		with m as source: audio = r.listen(source, timeout = 1, phrase_time_limit = 10 ) 
		print("Reconnaissance vocale...")
		try:
			# recognize speech using Google Speech Recognition
			query = r.recognize_google(audio, language="fr-FR")
			print("Vous avez dit {}".format(query))
			if done == True :
				if 'non' in query or 'ca va' in query:
					speak("D'accord madame.")
					return "quit"
			if not "au revoir" in query or "aurevoir" in query or "stop" in query:
				speak(choice(opening_text))
			else:
				bye_user()
		except sr.UnknownValueError:
			speak("Oops! Je n'ai pas bien compris. Pouvez-vous repetez ?")
			query = None
		except sr.RequestError as e:
			speak("Désole, le service est momentanement indisponible. Pouvez-vous repetez s'il vous plait ?")
			query = None
	except Exception:
		speak("Oops! Une erreur est survenue. Veuillez repetez s'il vous plait!")
		query = None
	return query

def done():
	speak("C'est fait")

def intend():
	again = False
	while True: 
		try:
			response = take_user_input(again)
			if not response == None :
				if not response == "quit":
					try : 
						print("before lowering response...")
						query = response.lower()
						print("after lowering response...")
						if 'terminal' in query:
							open_terminal()
							done()
						elif 'calculatrice' in query or 'calcul' in query:
							open_calculator()
							done()
						elif 'caméra' in query or 'photo' in query:
							open_camera()
							done()
						elif 'text' in query or 'sublime' in query:
							open_sublime_text()
							done()
						elif 'recherche' in query or 'comment' in query:
							speak(f"Qu'est ce que je dois chercher {CIVILITE} ?")
							search_query = take_user_input(True).lower()
							results = search_on_google(search_query)
							speak("J'ai trouvé quelque chose. Permettez moi d'afficher les résultats à l'écran")
							print(results)
							done()
						elif 'adresse IP' in query or 'adresse' in query or 'I P' in query:
							ip_address = find_my_ip()
							speak(f"Votre adresse IP est {ip_address}.")
						elif 'menu' in query or "mange" in query or "restaurant" in query:
							speak("Au menu du jour, il y'a en entrée de la macédoine avec pain farcie. En résistance, vous avez le choix entre du poisson braisé avec les bâtons et du poulet fris avec les plantains murs.\n En déssert, une glace à la banane. Désirez vous passez une commande ? ")
						else:
							speak("Désolé, je n'ai pas l'autorisation d'effectuer cette tâche.")
						time.sleep(1)
					except Exception as e:
						speak("Désolé {CIVILITE}, le service est momentanement indisponible. Je n'arrive pas à me connecter à internet.")
						print("error  :", e)
					finally:
						speak(f"Desirez-vous autre chose {CIVILITE} ?")
						#time.sleep(1)
						if not again:
							again = True
				else:
					bye_user()
					return False
			else:
				again = True
		except Exception as e:
			speak("Une erreur est survenue. Patientez s'il vous plait, je me mets à jour")
			print("error  :", e)
			again = False

def resourcePath(relativePath):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")

    return os.path.join(basePath, relativePath)

########################################################

def alert_propos():
	showinfo('A propos', 'nom de l\'application: Grace Assistant\n\n version: alpha 1.1.0\n\n nom de l\'assistant: GRACE\n\n description : Assistant virtuel\n\n langage : Francais (FR)\n\n fonctionnalites :\n \tOuverture des applications (terminal, camera, calculatrice, sublime text)\n \t Recherche sur google\n \t Détermine l\'adresse IP de l\'appareil\n\t Présente le menu du jour du restaurant de la banque\n\n date de mise à jour : 30/08/2023\n\n compatibilité : Windows 10+ uniquement\n\n Pour tout report de bugs, requêtes, contactez nous à l\'adresse suivante :\n email : annekevinanguen091@gmail.com\n telephone : (+237) 655 244 570\n\n\n Grace vous remercie pour votre contribution')

# define router | switching between frames
def go_to_start():
	fr_start.pack(fill='both', expand=1, side="top", padx=30, pady=10)
	fr_home.pack_forget()
	fr_initialisation.pack_forget()
	
def go_to_initialisation():
	fr_initialisation.pack(fill='both', expand=1, side="top", padx=30, pady=10)
	fr_home.pack_forget()
	fr_start.pack_forget()

def go_to_home():
	fr_home.pack(fill='both', expand=1, side="top", padx=30, pady=10)
	fr_initialisation.pack_forget()
	fr_start.pack_forget()
	image_h = Image.open('grace_vector_min.jpg')
	home_image = image_h.resize((250,150))
	h_image_for_tk = ImageTk.PhotoImage(home_image)

	heading = Label(fr_home)
	heading.pack()

	Label(heading, image=h_image_for_tk).pack(side="left")

	label2 = Label(heading, text="Qu'est ce que je dois faire ?", font=("Helvetica", 14))
	label2.pack(side="right", pady=20)

	mic_image = PhotoImage(file="icons8-microphone.gif")
	Label(fr_home, image=mic_image).pack(ipady=60)
	tips = Label(fr_home, text="Je suis à votre écoute ...", font=("Helvetica", 14))
	tips.pack(pady=20)

	button_name2 = Button(fr_home, text = "Nouvelle requete", font=("Helvetica", 14), command=intend)
	button_name2.pack(side="bottom", ipadx=10, ipady=5)
	
	button_name2.update()
	#time.sleep(1)
	#speak("Qu'est ce que je dois faire ?")
	intend()

def quit():
	bye_user()
	time.sleep(3)
	exit()

# render the first frame : started page
go_to_start()

# Set start fr_start
image = Image.open('grace_vector.jpg')
landing_image = image.resize((450,350))
image_for_tk = ImageTk.PhotoImage(landing_image)

Label(fr_start, image=image_for_tk).pack()
# :lbl 
newLabel = Label(fr_start, text = "Bonjour, je m'appelle Grace. Votre nouvelle assistante virtuelle", font=("Helvetica", 14))
newLabel.pack(ipadx=10, ipady=10)
# :btn A PROPOS
button_propos = Button(fr_start, text = "A propos", font=("Helvetica", 14), command=alert_propos)
button_propos.pack(side="bottom", ipadx=10)

button_propos.update()

time.sleep(1)
greet_user()
intend()

# :btn COMMENCER
button_name = Button(fr_start, text = "Nouvelle requete", font=("Helvetica", 14), background="#3399FF", command=intend)
button_name.pack(side="bottom", ipadx=10, ipady=5)


# render window
window.resizable(False, False) # disable resizing for window
window.mainloop()