# hackMIT

## MySQL setup using GCP

Install Google Cloud SDK:

https://cloud.google.com/sdk/docs/quickstart

Install cloud sql proxy:

https://cloud.google.com/sql/docs/mysql/sql-proxy#proxy_startup_options

Starting proxy:

https://cloud.google.com/sql/docs/mysql/connect-external-app#sqlalchemy-tcp

## Speech2Text

### Setup

Create service account in GCP console:
- Create a service account.
- Download a private key as JSON.

```
export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/service-account-file.json"
export GOOGLE_APPLICATION_CREDENTIALS="/Users/agong/research/hackmit2020/galvanic-axle-290004-a4517a7b5ca8.json"
```

### Run transcription

```
gsutil cp gs://path .
```

Command line:

```
gcloud ml speech recognize gs://cloud-samples-tests/speech/brooklyn.flac \
    --language-code=en-US
```

Python code samples:

https://github.com/googleapis/python-speech/tree/master/samples

## NLP Parsing

Setup:

```
python -m spacy download en_core_web_sm
python -m nltk.downloader all
```

## Data Sources

### Diseases & Symptoms

https://www.kaggle.com/data/55703#

https://www.kaggle.com/itachi9604/disease-symptom-description-dataset?select=dataset.csv

https://www.kaggle.com/plarmuseau/sdsort/home?select=symptoms2.csv

Drug Review Data:

https://www.kaggle.com/jessicali9530/kuc-hackathon-winter-2018