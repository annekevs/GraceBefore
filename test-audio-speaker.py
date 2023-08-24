import pyttsx3
import speech_recognition as sr

# init text-to-speech
engine = pyttsx3.init()
engine.setProperty("rate", 180)
engine.setProperty("volume", 1.0)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[29].id)

# init speech recognition
r = sr.Recognizer()
m = sr.Microphone()

def speak(text):
    engine.say(text)
    engine.runAndWait()

speak("Bonjour, je m'appelle GRACE. Comment puis-je vous aider?")

try:
    print("Un moment de silence, s'il vous plaît...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Le seuil minimal d'energie est de {}".format(r.energy_threshold))
    while True:
        with m as source: r.adjust_for_ambient_noise(source)
        print("Dites quelque chose! --- {}".format(r.energy_threshold))
        with m as source: audio = r.listen(source)
        print("C'est bon! reconnaissance vocale...")
        try:
	        # recognize speech using Google Speech Recognition
	        value = r.recognize_google(audio, language="fr-FR")

	        speak("Vous avez dit {}".format(value))
        except sr.UnknownValueError:
            speak("Oops! Je n'ai pas bien compris. Pouvez-vous repetez ?")
        except sr.RequestError as e:
            speak("Désole, le service est momentanement indisponible {0}".format(e))

except KeyboardInterrupt:
        pass

