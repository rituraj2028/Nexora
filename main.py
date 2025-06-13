import speech_recognition as sr
import webbrowser
import datetime
import urllib.parse
import pyttsx3 
import requests
import pyjokes    
import os         


API_KEY = os.getenv("WEATHER_API_KEY")

recognizer = sr.Recognizer()
engine = pyttsx3.init()




def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("Speech service is down.")
            return ""



def tell_joke():
    joke = pyjokes.get_joke()
    print("JARVIS:", joke)
    speak(joke)



def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return "City not found."

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        return f"The weather in {city} is {weather} with a temperature of {temp}°C, feels like {feels_like}°C."
    except:
        return "Sorry, I couldn't get the weather right now."        

if __name__ == "__main__":
    speak("Hello, I am Nexora. How can I assist you today?")
    
    while True:
        command = listen()

        if "open youtube" in command:
            webbrowser.open("https://youtube.com")
            speak("Opening YouTube.")
        elif "open google" in command:
            webbrowser.open("https://google.com")
            speak("Opening Google.")
        elif "open facebook" in command:
            webbrowser.open("https://facebook.com")
            speak("Opening facebook")
        elif "open linkedin" in command:
            webbrowser.open("https://linkedin.com")
            speak("Opening linkedin.")
        elif "time" in command:
            now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {now}")
        elif "date" in command:
            today = datetime.datetime.now().strftime("%A, %B %d, %Y")
            speak(f"Today is {today}")  
        elif "search for" in command:
            query = command.replace("search for", "").strip()
            if query:
                url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
                webbrowser.open(url)
                speak(f"Searching Google for {query}")
            else:
                speak("What should I search for?")
        
        elif "play" in command and "on youtube" in command:
            song = command.replace("play", "").replace("on youtube", "").strip()
            if song:
                url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(song)}"
                webbrowser.open(url)
                speak(f"Playing {song} on YouTube")
            else:
                speak("What song should I play?")  
        elif "weather in" in command:
            city = command.split("weather in")[-1].strip()
            if city:
              weather_info = get_weather(city)
              speak(weather_info)          
            else:
               speak("Please specify a city.")

        elif "exit" in command or "stop" in command:
            speak("Goodbye!")
            break
        elif "joke" in command or "make me laugh" in command:
            tell_joke()
        elif command != "":
            speak("I don't know how to do that yet.")
        
        
            


            




