from cgitb import text
import speech_recognition as sr
import gtts
from playsound import playsound
import os
from datetime import datetime
from notion import NotionClient

r = sr.Recognizer()

token = "secret_R2rwYoFh1AKwHaGxRg63bxDlPCwP8ocspHGUcC2kpbS"
database_id = "26da1eca5af9498997898593f80f30ca"

client = NotionClient(token, database_id)

ACTIVATION_COMMAND = "take a note"

def get_audio():
    with sr.Microphone() as source:
        print("Say 'take a note' to initialize text to Speech Bot!")
        audio = r.listen(source)
    return audio  

def audio_to_text(audio):
        text=""
        try:
            text = r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Could Not Recognize Speech.")
        except sr.RequestError:
            print("could not request results from API")
        return text  

def play_sound(text):
    try:
        tts = gtts.gTTS(text)
        tempfile = "./temp.mp3"
        tts.save(tempfile)
        playsound(tempfile)
        os.remove(tempfile)             #creates a temporary mp3 file on the system then removes it from the system
    except AssertionError:
        print("Sound Could not be played.")

if __name__ == "__main__":

    while True:
        a = get_audio()
        command = audio_to_text(a)

    
        if ACTIVATION_COMMAND in command.lower():
            print("activate")
            play_sound("How can i help you?")
            #sound is played for user to be alerted of activation

            note = get_audio()
            note = audio_to_text(note)

            if note:
                play_sound(note)

                now = datetime.now().astimezone().isoformat()
                res = client.create_page(note, now, status="Active")
                if res.status_code == 200:
                    play_sound("Note has been stored!")

