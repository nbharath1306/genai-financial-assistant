#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import pyjokes
import random
import pygame
import os
from imdb import IMDb

# Speech recognition initiation
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # 0 for male and 1 for female
activationWord = 'titan'  # To call

# Pygame initialization
pygame.init()

music_file = "C:/Users/amazi/Downloads/missionimpossible.mp3"

# Configure web browsing
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

# IMDbPY initialization
ia = IMDb()

# Set initial value of listening flag
listening_enabled = True

def speak(text, rate=120):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

def parseCommand():
    listener = sr.Recognizer()
    print("Listening for a command")
    with sr.Microphone() as source:
        listener.pause_threshold = 2
        input_speech = listener.listen(source)
    try:
        print("Recognising Speech")
        query = listener.recognize_google(input_speech, language='en_gb')
        print('The input speech was:', query)
    except Exception as exception:
        print("I did not quite catch it")
        speak("I did not quite catch it")
        print(exception)
        return 'None'
    return query

def search_wikipedia(query):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print("No Wikipedia result")
        return "No result received"
    
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    
    print(wikiPage.title)
    wikiSummary = wikiPage.summary.split(".")[0]  # Extracting only the first sentence
    return wikiSummary

def tell_joke():
    joke = pyjokes.get_joke()
    print(joke)
    speak(joke)

def play_music():
    global listening_enabled
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()
    # Disable listening while music is playing
    listening_enabled = False

def calculate(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return str(e)

def get_random_movie_details():
    # Generate a random search term (e.g., a single letter)
    random_search_term = random.choice('abcdefghijklmnopqrstuvwxyz')

    # Search for movies with the random search term
    search_results = ia.search_movie(random_search_term)

    # Check if there are any search results
    if not search_results:
        print("No movies found")
        return "No movies found", None, None

    # Choose a random movie from the search results
    random_movie = random.choice(search_results)

    # Fetch details of the selected movie
    movie = ia.get_movie(random_movie.movieID)
    movie_title = movie['title']
    movie_rating = movie['rating']
    
    # Get the first 5 actors from the cast list
    cast = ', '.join([actor['name'] for actor in movie['cast'][:5]])

    # Print movie details
    print(f"Title: {movie_title}")
    print(f"Rating: {movie_rating}")
    print(f"Cast: {cast}")

    return movie_title, movie_rating, cast

# Main loop
if __name__ == '__main__':
    speak("All systems nominal")
    while True:
        # If listening is enabled, parse commands
        if listening_enabled:
            query = parseCommand().lower().split()
            if len(query) == 0:
                continue  # Skip the rest of the loop iteration if no command is detected
                
            if query[0] == activationWord:
                query.pop(0)
                if len(query) == 0:
                    speak("Please provide a command.")
                    continue  # Continue to the next iteration of the loop
                
                # Handle commands based on user input
                if query[0] == 'say':
                    if 'hello' in query[1:]:
                        speak("Greetings, all!")
                    else:
                        query.pop(0)
                        speech = ' '.join(query)
                        speak(speech)
                elif query[0] == 'go' and query[1] == 'to':
                    speak("Ongoing...")
                    website = ' '.join(query[2:])
                    webbrowser.get('chrome').open_new(website)
                elif query[0] == 'wikipedia':
                    query = ' '.join(query[1:])
                    speak("Querying the Universal database")
                    results = search_wikipedia(query)
                    speak(results)
                elif query[0] == 'joke':
                    speak("Here's a joke for you")
                    tell_joke()
                elif query[0] == 'music':
                    speak("Now playing music")
                    play_music()
                elif query[0] == 'calculate':
                    expression = ' '.join(query[1:])
                    result = calculate(expression)
                    speak(f"The result of {expression} is {result}")
                elif query[0] == 'movie':
                    movie_title, movie_rating, cast = get_random_movie_details()
                    speak(f"I recommend the movie {movie_title}. It has a rating of {movie_rating}. The cast includes: {cast}")
                elif query[0] == 'date':
                    # Get current date and speak it
                    current_date = datetime.now().strftime("%A, %B %d, %Y")
                    speak(f"Today's date is {current_date}")
                elif query[0] == 'time':
                    # Get current time and speak it
                    current_time = datetime.now().strftime("%I:%M %p")
                    speak(f"The current time is {current_time}")
                elif query[0] == 'exit':
                    speak("Goodbye")
                    break
                
        # Check if music has stopped playing
        if not pygame.mixer.music.get_busy():
            listening_enabled = True  # Enable listening when music ends
            


# In[ ]:





# In[ ]:




