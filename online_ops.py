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
    

