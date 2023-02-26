import speech_recognition as sr
import pyttsx3
import speedtest
import datetime
import openai

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set up the OpenAI API client
openai.api_key = "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"

# Set up the model and prompt
model_engine = "text-davinci-003"


# Function to speak out text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize speech recognition engine
r = sr.Recognizer()

# Set wake word
wake_word = "hello"

# Start listening for voice commands
with sr.Microphone() as source:
    print("Listening...")
    r.adjust_for_ambient_noise(source)
    while True:
        audio = r.listen(source)
        try:
            # Recognize speech and get text
            text = r.recognize_google(audio)
            print("You said: ", text)
            if wake_word in text.lower():
                # Remove wake word from text
                command = text.lower().replace(wake_word, "").strip()
                # Check command and execute appropriate Python code
                if "speed test" in command:
                    st = speedtest.Speedtest()
                    download_speed = st.download() / 10**6
                    upload_speed = st.upload() / 10**6
                    speak(f"My download speed is {download_speed:.2f} megabits per second and my upload speed is {upload_speed:.2f} megabits per second.")
                elif "date and time" in command:
                    now = datetime.datetime.now()
                    date = now.strftime("%d %B %Y")
                    time = now.strftime("%I:%M %p")
                    response = "The date is "+date+" and the time is "+time+"."
                    print(response)
                    speak(f"The date is {date} and the time is {time}.")
                else:
                    prompt = command
                    # Generate a response
                    completion = openai.Completion.create(
                        engine=model_engine,
                        prompt=prompt,
                        max_tokens=1024,
                        n=1,
                        stop=None,
                        temperature=0.5,
                    )
                    response = completion.choices[0].text
                    print(response)
                    speak(response)
                # Add more commands here
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service: {e}")
