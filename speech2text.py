# Source:
# https://github.com/googleapis/python-speech/blob/master/samples/snippets/quickstart.py

import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

import spacy
from spacy.pipeline import EntityRuler
from spacy import displacy
from nltk.corpus import brown

import pandas as pd
from tqdm import tqdm

# Instantiates a client
client = speech.SpeechClient()


# Instantiates nlp model
nlp = spacy.load("en_core_web_sm")
normal_corpus = set(brown.words())

drug_data = pd.read_csv('db/Drug_data_table.csv', index_col=0)
drug_names = set() # Drug names
single_terms = set() # Single words
print("Reading drug data...")
for i, row in tqdm(drug_data.iterrows()):
    prop_name, medical_name = row['Proprietary Name'], row['Medical Name']
    if pd.notnull(prop_name) and pd.notnull(medical_name):
        prop_name = prop_name.strip()
        medical_name = medical_name.strip()
        drug_names.update([prop_name, medical_name])

        for term in prop_name.split(' ') + medical_name.split(' '):
            if term not in normal_corpus:
                single_terms.add(term)

disease_data = pd.read_csv('disease_data/dataset.csv')
print("Reading disease data...")
DISEASE_SYMPTOMS = {}
symptom_names = set()
for i, row in tqdm(disease_data.iterrows()):
    # Convert to lowercase
    disease = row['Disease'].strip().lower()
    if disease not in DISEASE_SYMPTOMS.keys():
        DISEASE_SYMPTOMS[disease] = set()

    for n in range(1, 18):
        symptom = row[f"Symptom_{n}"]
        if pd.notnull(symptom):
            symptom = symptom.strip().replace('_', ' ')
            DISEASE_SYMPTOMS[disease].add(symptom)
            symptom_names.add(symptom)

# Add names to entity ruler
entity_ruler = EntityRuler(nlp)

drug_patterns = []
print("Creating drug patterns...")
for name in tqdm(list(drug_names) + list(single_terms)):
    pattern = {'label':'DRUG', 'pattern':name, 'id': name.replace(' ', '_')}
    drug_patterns.append(pattern)
# print(drug_patterns[:1000])

disease_patterns = []
print("Creating disease patterns...")
for name in tqdm(list(DISEASE_SYMPTOMS.keys())):
    tokens = name.split(' ')
    pattern = {'label':'DISEASE', 'pattern':[{"LOWER": s} for s in tokens], 'id': name.replace(' ', '_')}
    disease_patterns.append(pattern)
print(disease_patterns[:10])

symptom_patterns = []
print("Creating symptom patterns...")
for name in tqdm(list(symptom_names)):
    tokens = name.split(' ')
    pattern = {'label':'SYMPTOM', 'pattern':[{"LOWER": s} for s in tokens], 'id': name.replace(' ', '_')}
    symptom_patterns.append(pattern)
print(symptom_patterns[:10])

other_pipes = [p for p in nlp.pipe_names if p != "tagger"]
with nlp.disable_pipes(*other_pipes):
    entity_ruler.add_patterns(drug_patterns + disease_patterns + symptom_patterns)

nlp.add_pipe(entity_ruler, before='ner')
print(nlp.pipe_names)

def transcribe(file_name):
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
    with open('test_data/transcription.txt', 'r') as f:
        recognized_text = f.read()
    doc = parse(recognized_text)
    print(renderEntities(doc))