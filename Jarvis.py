import datetime
import getpass  # Import the getpass module for secure password input
import os
import smtplib
import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("I am Jarvis Sir. Please tell me how may I help you")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5)  # Add a timeout for listening
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query.lower()
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Unexpected error during speech recognition; {e}")
        return "None"


def sendEmail(to, content, email_password):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', email_password)
    server.sendmail('youremail@gmail.com', to, content)
    server.close()


if __name__ == "__main__":
    wishMe()
    email_password = getpass.getpass("Enter your email password: ")  # Securely input the email password

    # Dictionary to store email addresses and names
    contacts = {
        'friend': 'friendEmail@gmail.com',
        'family': 'familyEmail@gmail.com',
        'colleague': 'colleagueEmail@gmail.com'
        # Add more contacts as needed
    }
    
    while True:
        query = takeCommand()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except wikipedia.DisambiguationError as e:
                speak("Multiple results found. Please be more specific.")
            except wikipedia.PageError as e:
                speak("No results found for the query.")

        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube")

        elif 'open google' in query:
            webbrowser.open("https://www.google.com")
            speak("Opening Google")

        elif 'open stackoverflow' in query:
            webbrowser.open("https://www.stackoverflow.com")
            speak("Opening Stack Overflow")

        elif 'play music' in query:
            music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2'
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
                speak("Playing music")
            else:
                speak("No music files found in the specified directory.")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "D:\Microsoft VS Code\Code.exe"
            os.startfile(codePath)
            speak("Opening Visual Studio Code")

        elif 'email to' in query:
            try:
                speak("Who do you want to send the email to? (e.g., friend, family, colleague)")
                contact_name = takeCommand().lower()
                to = contacts.get(contact_name)
                if to:
                    speak(f"What should I say to {contact_name}?")
                    content = takeCommand()
                    sendEmail(to, content, email_password)
                    speak("Email has been sent!")
                else:
                    speak(f"Sorry, I don't have the email address for {contact_name}.")
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send this email at the moment")

        elif 'exit' in query or 'quit' in query:
            speak("Goodbye!")
            break
