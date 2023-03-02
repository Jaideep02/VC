import speech_recognition as sr
import webbrowser
import spotipy
import spotipy.util as util
import os

# Set up Spotify credentials
client_id = "589c8fb8f1a4445a95de7b9036954116"
client_secret = "a5c347ba1c1442029938cda381598fe9"
redirect_uri = "http://localhost:8080/callback/"
username = "5se0dsqrjjja963ec66baok0k"

scope = 'user-read-private user-read-playback-state user-modify-playback-state'

# Get Spotify token
token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

# Set up speech recognition
r = sr.Recognizer()

with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

try:
    # Recognize speech using Google Speech Recognition
    query = r.recognize_google(audio)
    print("Google Speech Recognition thinks you said ", query)
    
    # Search Google
    if "search for" in query:
        search_query = query.replace("search for", "")
        url = "https://www.google.com/search?q=" + search_query
        webbrowser.open_new_tab(url)

    # Search YouTube
    elif "play video" in query:
        search_query = query.replace("play video", "")
        url = "https://www.youtube.com/results?search_query=" + search_query
        webbrowser.open_new_tab(url)
    # Search Spotify
    elif "play" in query:
        if token:
            sp = spotipy.Spotify(auth=token)
            search_query = query.replace("play", "")
            results = sp.search(search_query, limit=1, type='track')
            if results['tracks']['items']:
                uri = results['tracks']['items'][0]['uri']
                sp.start_playback(uris=[uri])
        else:
            print("Can't get token for", username)

except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
