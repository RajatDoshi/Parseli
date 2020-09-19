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