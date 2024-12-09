# Audio Transcription Script

This script processes audio recordings, reduces noise, uploads them to Google Cloud Storage, and transcribes them using Google Speech-to-Text with speaker diarization.

## Features
- Converts `.m4a` audio files to `.wav` format.
- Reduces noise in audio files for better transcription accuracy.
- Ensures compliance with Google Speech-to-Text API (mono audio, `LINEAR16` encoding).
- Supports speaker diarization to differentiate between speakers.
- Outputs speaker-differentiated transcriptions as `.txt` files.

---

## Prerequisites

### 1. Python Environment
- Ensure Python 3.8 or later is installed.
- Install the required dependencies:
  ```bash
  pip install google-cloud-speech google-cloud-storage pydub

### 2. Google Cloud Setup
- Create a Project: Set up a Google Cloud Project.
- Enable APIs: Enable the Google Speech-to-Text API and Cloud Storage API.
- Create a Cloud Storage Bucket: Note the bucket name.
- Set Up Credentials: Download the service account key (JSON) and set the GOOGLE_APPLICATION_CREDENTIALS environment variable:
  ```bash
  export GOOGLE_APPLICATION_CREDENTIALS="path_to_your_service_account_key.json"

### 3. Install FFmpeg
Install FFmpeg for audio processing:
- macOS (using Homebrew):
  ```bash
  brew install ffmpeg
- Ubuntu/Debian:
  ```bash
  sudo apt update && sudo apt install ffmpeg

---

## Folder Structure
Organize your files as follows:
- Place .m4a files in the recordings folder.
- The script automatically creates a converted folder for processed files.
  ```bash
  project-root/
  ├── recordings/
  │   ├── subject1/
  │   │   ├── audio1.m4a
  │   │   ├── audio2.m4a
  ├── converted/
  ├── transcribe_audio.py
  └── README.md

---

## Usage

### 1. Clone the Repository
git clone https://github.com/your-username/your-repo.git
cd your-repo

### 2. Install the Dependencies
Install all the required packages by running the following command:
pip install -r requirements.txt

### 3. Run the Script
Execute the script to process and transcribe your audio files:
python transcribe_rec2text.py

### 4. Output
The script will:
- Convert .m4a files to .wav format with reduced noise.
- Upload .wav files to the specified Cloud Storage bucket.
- Transcribe the audio and save transcriptions as .txt files in the converted folder.

The transcriptions will include speaker differentiation, with the text structured like this:
```bash
Speaker 1: Hello, how are you?
Speaker 2: I'm doing well, thank you!



