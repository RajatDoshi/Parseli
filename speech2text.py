# Source:
# https://github.com/googleapis/python-speech/blob/master/samples/snippets/quickstart.py

import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

import spacy
from spacy import displacy

# Instantiates a client
client = speech.SpeechClient()
# Instantiates nlp model
nlp = spacy.load("en_core_web_sm")

# The name of the audio file to transcribe
# file_name = os.path.join(
#     os.path.dirname(__file__),
#     'resources',
#     'audio.raw')
"""
file_name = "brooklyn.flac"

# Loads the audio into memory
with io.open(file_name, 'rb') as audio_file:
    content = audio_file.read()
    audio = types.RecognitionAudio(content=content)

config = types.RecognitionConfig(
    # encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code='en-US')

# Detects speech in the audio file
response = client.recognize(config, audio)

for result in response.results:
    print('Transcript: {}'.format(result.alternatives[0].transcript))
"""

def getTranscript(file_name):
    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        # encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        # sample_rate_hertz=16000,
        language_code='en-US')

    # Detects speech in the audio file
    response = client.recognize(config, audio)
    recognized_text = ""

    for result in response.results:
        # print('Transcript: {}'.format(result.alternatives[0].transcript))
        recognized_text += result.alternatives[0].transcript

    return recognized_text

def parse(text):
    doc = nlp(text)
    return doc

def renderEntities(doc):
    return displacy.render(doc, style="ent", page=False)

if __name__ == "__main__":
    doc = nlp("thank you for taking the time to speak with us I have some information regarding your test results for test results indicate that you I test positive for diabetes I understand that this can be an alarming thing to hear just note that this is a process and it's a fight for weekend fight hard and strong the medication I recommend isn't metformin I need you to take this twice a day every single day this will help ensure that your blood sugar does not draw closer and point are you following")
    html = displacy.render(doc, style="ent", page=False)
    print(html)