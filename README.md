Audio Transcription Script
This script processes audio recordings, reduces noise, uploads them to Google Cloud Storage, and transcribes them using Google Speech-to-Text with speaker diarization.

Features
Converts .m4a audio files to .wav format.
Reduces noise in audio files for better transcription accuracy.
Ensures compliance with Google Speech-to-Text API (mono audio, LINEAR16 encoding).
Supports speaker diarization to differentiate between speakers.
Outputs speaker-differentiated transcriptions as .txt files.
Prerequisites
1. Python Environment
Ensure Python 3.8 or later is installed.
Install the required dependencies:
bash
Copy code
pip install google-cloud-speech google-cloud-storage pydub
2. Google Cloud Setup
Create a Project: Set up a Google Cloud Project.
Enable APIs: Enable the Google Speech-to-Text API and Cloud Storage API.
Create a Cloud Storage Bucket: Note the bucket name.
Set Up Credentials: Download the service account key (JSON) and set the GOOGLE_APPLICATION_CREDENTIALS environment variable:
bash
Copy code
export GOOGLE_APPLICATION_CREDENTIALS="path_to_your_service_account_key.json"
3. Install FFmpeg
Install FFmpeg for audio processing:

macOS (using Homebrew):
bash
Copy code
brew install ffmpeg
Ubuntu/Debian:
bash
Copy code
sudo apt update && sudo apt install ffmpeg
Folder Structure
Organize your files as follows:

Place .m4a files in the recordings folder.
The script automatically creates a converted folder for processed files.
plaintext
Copy code
project-root/
├── recordings/
│   ├── subject1/
│   │   ├── audio1.m4a
│   │   ├── audio2.m4a
├── converted/
├── transcribe_audio.py
└── README.md
Usage
1. Clone the Repository
bash
Copy code
git clone https://github.com/your-username/your-repo.git
cd your-repo
2. Run the Script
Execute the script to process and transcribe your audio files:

bash
Copy code
python transcribe_audio.py
3. Output
The script:

Converts .m4a files to .wav format with reduced noise.
Uploads .wav files to the specified Cloud Storage bucket.
Transcribes the audio and saves transcriptions as .txt files in the converted folder.
Transcriptions include speaker differentiation, with text structured like:

plaintext
Copy code
Speaker 1: Hello, how are you?
Speaker 2: I'm doing well, thank you!
Customization
Edit Script Variables
recordings_folder: Path to the folder containing .m4a files.
output_folder: Path for saving .txt transcription files.
bucket_name: Your Cloud Storage bucket name.
Change Language Code
To transcribe audio in a language other than Hebrew (he-IL), update the language_code in the script. For example, for English (en-US):

python
Copy code
language_code="en-US"
Adjust Timeout
If transcription takes too long, increase the custom_timeout variable (in seconds).

Troubleshooting
1. InvalidArgument: Must Use Single Channel (Mono) Audio
Ensure your audio files are converted to mono. The script performs this conversion automatically.

2. Permissions Error
Verify your service account has the required permissions for:

Google Speech-to-Text API
Google Cloud Storage API
3. Missing Transcriptions
Ensure .m4a files are in the correct recordings subfolders.
