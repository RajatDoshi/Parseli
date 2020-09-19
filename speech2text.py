# Source:
# https://github.com/googleapis/python-speech/blob/master/samples/snippets/quickstart.py

# [START speech_quickstart]
import io
import os

# Imports the Google Cloud client library
# [START speech_python_migration_imports]
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
# [END speech_python_migration_imports]

# Instantiates a client
# [START speech_python_migration_client]
client = speech.SpeechClient()
# [END speech_python_migration_client]

# The name of the audio file to transcribe
# file_name = os.path.join(
#     os.path.dirname(__file__),
#     'resources',
#     'audio.raw')
"""file_name = "brooklyn.flac"

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
# [END speech_quickstart]"""

def getTranscript(file_name):
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
    recognized_text = ""

    for result in response.results:
        # print('Transcript: {}'.format(result.alternatives[0].transcript))
        recognized_text += result.alternatives[0].transcript

    return recognized_text

