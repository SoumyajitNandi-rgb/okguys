import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests

recogniser = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "c84e0eff05834730bcaa8ede676305cc"  # Your News API key

def speak(text):
    print(f"Speaking: {text}")
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    c = c.lower()
    print(f"Processing Command: {c}")

    if "open google" in c:
        webbrowser.open("https://www.google.com")
    elif "open facebook" in c:
        webbrowser.open("https://www.facebook.com")
    elif "open spotify" in c:
        webbrowser.open("https://www.spotify.com")
    elif "open instagram" in c:
        webbrowser.open("https://www.instagram.com")
    elif "open linkedin" in c:
        webbrowser.open("https://www.linkedin.com")
    elif c.startswith("play"):
        parts = c.split()
        if len(parts) > 1:
            song = ' '.join(parts[1:]).strip().lower()
            print(f"User asked for song: {song}")
            for key in musiclibrary.music:
                if key.strip().lower() == song:
                    speak(f"Playing {key}")
                    webbrowser.open(musiclibrary.music[key])
                    return
            speak(f"Sorry, I don't have {song} in the music library.")
        else:
            speak("Please say the name of the song after 'play'.")
    elif any(word in c for word in ["news", "latest", "headlines"]):
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
            articles = r.json().get("articles", [])[:5]
            if not articles:
                speak("Sorry, no news found.")
                return
            for i, article in enumerate(articles, start=1):
                speak(f"News {i}: {article['title']}")
        except Exception as e:
            print(f"Error fetching news: {e}")
            speak("Sorry, I couldn't fetch the news at the moment.")
    elif "stop" in c or "exit" in c:
        speak("Goodbye!")
        exit()
    else:
        speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word (say 'Jarvis')...")
                recogniser.adjust_for_ambient_noise(source, duration=0.5)
                audio = recogniser.listen(source, timeout=5, phrase_time_limit=5)

            word = recogniser.recognize_google(audio)
            print(f"Wake word heard: {word}")

            if word.lower() == "jarvis":
                speak("Yes, how can I help?")
                with sr.Microphone() as source:
                    recogniser.adjust_for_ambient_noise(source, duration=0.5)
                    print("Listening for your command...")
                    audio = recogniser.listen(source, timeout=5, phrase_time_limit=7)
                command = recogniser.recognize_google(audio)
                print(f"Command heard: {command}")
                processCommand(command)

        except sr.WaitTimeoutError:
            print("Timeout. No speech detected.")
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Speech Recognition service error: {e}")
