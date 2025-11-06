
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import time
import requests
from google import genai
import pygame
import os
from elevenlabs import ElevenLabs , play
from datetime import datetime
import threading
import random
import python_weather
import asyncio

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "YOUR_API_KEY"




    
def aiProcess(command):
    client = genai.Client(api_key="YOUR_API_KEY")
    
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=command
    )

    return(response.text)
 
API_KEY = "YOUR_API_KEY" 
VOICE_ID = "YOUR_API_KEY"  # Bella voice

pygame.mixer.init()


def speak(text):
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": API_KEY
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2"
        }

        response = requests.post(url, json=data, headers=headers)
        
        filename = "speech.mp3"
        with open(filename, "wb") as f:
            f.write(response.content)


        pygame.mixer.music.load(filename)

        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.unload()
        os.remove(filename)

    except Exception as e:
        print("Speech Error:", e)

# Weather Function using python-weather
import python_weather
import asyncio

async def fetch_weather(city="Delhi"):
    try:
        async with python_weather.Client(unit=python_weather.METRIC) as client:
            weather = await client.get(city)

            temp = weather.temperature
            condition = weather.description

            return f"The temperature in {city} is {temp} degrees Celsius with {condition}."
    
    except Exception as e:
        print("Weather Error:", e)
        return f"Unable to fetch weather for {city}."


def processCommand(c):
    if "open google" in c.lower():
        speak("Opening google")
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        speak("Opening youtube")
        webbrowser.open("https://youtube.com")
    elif "open instagram" in c.lower():
        speak("Opening Instagram")
        webbrowser.open("https://instagram.com")    
    elif "open linkedin" in c.lower():
        speak("Opening linkedin")
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().replace("play", "").strip()

        if song in musicLibrary.music:
            speak(f"Playing {song}")
            link = musicLibrary.music[song]
            webbrowser.open(link)
        else:
            speak(f"I couldn't find '{song}' in your music library.")
            print("DEBUG available keys:", musicLibrary.music.keys())
    
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
                    # Convert response to JSON format
        data = r.json()

            # Print headlines
        if data["status"] == "ok":
                headlines = data["articles"]
                for i, article in enumerate(headlines, start=1):
                    speak(f"{i}. {article['title']}")
        else:
                print("Error fetching news:", data)

        # Weather Feature
    elif "weather" in c:
        city = c.lower().replace("weather in", "").replace("weather", "").strip()
        
        if not city:
            city = "Delhi"

        result = asyncio.run(fetch_weather(city))
        speak(f"Here is the weather update for {city}. {result}")
        
        # Jokes features
    elif "joke" in c:
        jokes = [
            "Why don't robots have brothers? Because they all share the same motherboard!",
            "I told my computer I needed a break, and it said: No problem — I’ll go to sleep!",
        ]
        speak(random.choice(jokes))

    #  Reminders
    elif "remind me" in c:
        try:
            speak("What should I remind you about?")
            with sr.Microphone() as source:
                audio = recognizer.listen(source)
            task = recognizer.recognize_google(audio)

            speak("In how many seconds?")
            with sr.Microphone() as source:
                audio = recognizer.listen(source)
            sec = int(recognizer.recognize_google(audio))

            threading.Thread(target=reminder, args=(task, sec)).start()
            speak(f"I will remind you about {task} in {sec} seconds.")
        except:
            speak("Failed to set reminder.")


    else:
        # Let openAI handle the request
        output = aiProcess(c)
        speak(output)
    

if __name__ == "__main__":
    speak("Initializing Friday....  ")
    while True:
        # Listen for the Wake word "Nexa"
        # obtain audio from the mircophone
        r = sr.Recognizer()

        
        #recognize speech using Sphinx
        print("recognizing.....")
        try:
            with sr.Microphone() as source:
              print("Listening...")
              audio = r.listen(source , timeout=2 , phrase_time_limit=1)

            command = r.recognize_google(audio)
            if "friday" in command.lower():
                speak("yes sir")
    
                
                #listen command
                with sr.Microphone() as source:
                    print("Friday is Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)
        
        except Exception as e:
            print("Error; {0}".format(e))
