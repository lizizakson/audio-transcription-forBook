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
