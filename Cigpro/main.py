import pyautogui
import speech_recognition as sr
import spacy
import requests
from bs4 import BeautifulSoup
import os
import random
import webbrowser
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import openai

# set OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# define the OpenAI model to use
MODEL_ENGINE = "text-davinci-003"
MODEL_NAME = "openai/text-davinci-003"

# define the Google Search API endpoint
SEARCH_API_ENDPOINT = "https://www.google.com/search"

# define the number of search results to retrieve
NUM_RESULTS = 5

# define the wake word
WAKE_WORD = "hey assistant"

# load the English language model for spaCy
nlp = spacy.load("en_core_web_sm")

# create a recognizer object
r = sr.Recognizer()

# create a Spotify client object
SPOTIPY_CLIENT_ID = 'YOUR_CLIENT_ID_HERE'
SPOTIPY_CLIENT_SECRET = 'YOUR_CLIENT_SECRET_HERE'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope='user-read-playback-state, user-modify-playback-state'))

# define a function to listen for and process user input
def listen():
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # use the Google Speech Recognition API to convert audio to text
    try:
        text = r.recognize_google(audio)
        print("You said:", text)

        # check if the wake word is present
        if WAKE_WORD in text.lower():
            process_intent(text.lower().replace(WAKE_WORD, "").strip())

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def process_intent(text):
    # use spaCy to parse the input text and extract relevant information
    doc = nlp(text)

    # iterate over the detected entities in the text
    for ent in doc.ents:
        if ent.label_ == "ACTION":
            # if the user's intent is to perform an action, execute the action
            action = ent.text.lower()
            if action == "open":
                open_application()
            elif action == "search":
                search_web(ent)
            elif action == "play":
                play_music(ent)
        elif ent.label_ == "QUERY":
            # if the user's intent is to retrieve information, provide a response
            response = get_response(ent.text.lower())
            speak(response)

def open_application():
    # code to open a specified application
    pass

def search_web(query):
    # construct the search query URL
    search_query = {
        "q": query,
        "num": NUM_RESULTS
    }
    search_url = "{}?{}".format(SEARCH_API_ENDPOINT, "&".join(["{}={}".format(k, v) for k, v in search_query.items()]))

    # send the search query and retrieve the search results page HTML
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # extract the search result titles and URLs
    results = soup.select("div.g > div > div.rc > div.r > a")
    for i, result in enumerate(results):
        title = result.get_text()
        url = result["href"]
        print("{}: {}".format(i+1, title))
        print(url)

def get_response(query):
    # use OpenAI's GPT-3 model to generate a response to the user's query
    prompt = "Generate a response to the following query: {}\n".format(query)
    response = openai.Completion.create(
        engine=MODEL_ENGINE,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7
    )

    # return the generated response
    return response.choices[0].text.strip()

'''def play_music(song):
    # search for the specified song or playlist
    search_url = "https://www.youtube.com/results?search_query=" + song
    webbrowser.get().open(search_url)

    # wait for the search results to load
    time.sleep(5)

    # click on the first video in the search results to play it
    pyautogui.click(476, 358)

    # wait for the video to load and start playing
    time.sleep(5)

    # press the "f" key to enter fullscreen mode
    pyautogui.press("f")

    # wait for the video to finish playing
    time.sleep(180)

    # press the "esc" key to exit fullscreen mode
    pyautogui.press("esc")

    # close the browser window
    pyautogui.hotkey("ctrl", "w")
'''
def play_music(song):
    # search for the specified song or playlist
    results = sp.search(q=song, limit=1, type='track')
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        sp.start_playback(uris=[track_uri])

def speak(response):
    # code to use text-to-speech to speak the response to the user
    pass

# listen for user input indefinitely
while True:
    listen()
