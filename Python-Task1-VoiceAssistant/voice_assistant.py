
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser


# Initialize the voice engine
engine = pyttsx3.init()

# Set speaking speed
engine.setProperty("rate", 170)

# Set volume
engine.setProperty("volume", 1.0)


# Function to speak
def speak(text):
    print("Nova:", text)
    engine.say(text)
    engine.runAndWait()


# Function to listen to the user
def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(
                source, timeout=5, phrase_time_limit=8
            )

            print("Recognizing...")

            command = recognizer.recognize_google(audio)

            print("You:", command)

            return command.lower()

        except sr.UnknownValueError:
            speak("Sorry, I did not understand. Please repeat.")
            return ""

        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
            return ""

        except sr.WaitTimeoutError:
            speak("I did not hear anything. Please try again.")
            return ""


# Function to process commands
def process_command(command):

    if "hello" in command or "hi" in command:
        speak("Hello! I am Nova, your personal voice assistant.")

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak("The current time is " + current_time)

    elif "date" in command:
        today = datetime.datetime.now().strftime("%d %B %Y")
        speak("Today's date is " + today)

    elif "search for" in command:
        topic = command.replace("search for", "").strip()

        if topic:
            speak("Searching Google for " + topic)
            webbrowser.open(
                "https://www.google.com/search?q=" + topic.replace(" ", "+")
            )
        else:
            speak("Please tell me what you want to search for.")

    elif "youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    elif "google" in command:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    elif "exit" in command or "stop" in command or "goodbye" in command:
        speak("Goodbye! Have a great day.")
        return False

    elif command:
        speak("Sorry, I don't know that command yet.")

    return True


# Main function
def main():

    speak("Hello! I am Nova. How can I help you?")

    running = True

    while running:

        command = listen()

        if command:
            running = process_command(command)


# Start the assistant
if __name__ == "__main__":
    main()
