import os
from google.cloud import speech
from google.cloud import storage
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

# Define paths
recordings_folder = "../recordings"  # Adjust as needed for the relative or absolute path
output_folder = "../recordings/converted"  # Folder for converted .wav files
bucket_name = "my-audio-bucket-111288"  # Replace with your Cloud Storage bucket name

# Set custom timeout (in seconds)
custom_timeout = 3600  # 1 hour

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Initialize the Google Cloud Storage client
storage_client = storage.Client()

# Function to reduce noise using Pydub
def reduce_noise(input_path, output_path, timeout=custom_timeout):
    print(f"Reducing noise for {input_path}...")
    audio = AudioSegment.from_file(input_path, format="m4a")

    # Ensure the audio is mono
    if audio.channels > 1:
        audio = audio.set_channels(1)
        # Save the mono audio for later listening
        audio.export(output_path, format="wav")
        print(f"Converted to mono and saved as {output_path}.")
    else:
        audio.export(output_path, format="wav")
        print(f"Audio is already mono, saved as {output_path}.")

# Function to upload audio file to Cloud Storage
def upload_to_cloud_storage(local_path, destination_blob_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_path)
    print(f"File {local_path} uploaded to {destination_blob_name}.")

# Function to transcribe audio using Google Speech-to-Text with speaker diarization
def transcribe_audio_from_gcs(gcs_uri, language_code="he-IL", timeout=custom_timeout):
    client = speech.SpeechClient()

    # Configure the recognition request for long-running recognition with speaker diarization
    audio = speech.RecognitionAudio(uri=gcs_uri)
    diarization_config = speech.SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=1,
        max_speaker_count=2,
    )
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code=language_code,
        diarization_config=diarization_config,
    )

    print(f"Starting transcription for {gcs_uri} with a timeout of {timeout} seconds...")
    operation = client.long_running_recognize(config=config, audio=audio)

    # Wait for the transcription result
    response = operation.result(timeout=timeout)
    print(f"Transcription completed for {gcs_uri}.")

    # Initialize variables to handle conversation formatting
    transcript = []
    current_speaker = None
    current_paragraph = []

    # Iterating over the transcription results and formatting speaker-specific paragraphs
    for result in response.results:
        alternative = result.alternatives[0]
        for word_info in alternative.words:
            speaker_tag = word_info.speaker_tag
            word = word_info.word

            print(f"Speaker Tag: {speaker_tag}, Word: {word}")  # Debugging the speaker tag and word

            # If the speaker tag has changed, save the previous speaker's paragraph and start a new one
            if speaker_tag != current_speaker:
                if current_speaker is not None:
                    transcript.append(f"Speaker {current_speaker}: {' '.join(current_paragraph)}")
                current_speaker = speaker_tag
                current_paragraph = [word]  # Start a new paragraph for the new speaker
            else:
                current_paragraph.append(word)  # Continue adding words for the current speaker

    # Add the final speaker's paragraph
    if current_paragraph:
        transcript.append(f"Speaker {current_speaker}: {' '.join(current_paragraph)}")

    # Join the transcript into a single string with paragraphs
    return '\n\n'.join(transcript)

# Function to check if a transcription already exists
def transcription_exists(file_name):
    transcription_path = os.path.join(output_folder, os.path.splitext(file_name)[0] + ".txt")
    return os.path.exists(transcription_path)

# Process all .m4a files in the recordings folder
for subject_folder in os.listdir(recordings_folder):
    subject_path = os.path.join(recordings_folder, subject_folder)

    if os.path.isdir(subject_path):
        print(f"Processing subject folder: {subject_folder}")

        for file_name in os.listdir(subject_path):
            if file_name.endswith(".m4a"):
                input_path = os.path.join(subject_path, file_name)

                # Skip transcription if already exists
                if transcription_exists(file_name):
                    print(f"Skipping transcription for {file_name}, already processed.")
                    continue

                print(f"Reducing noise and converting {file_name} to .wav format...")
                # Convert m4a to wav and apply noise reduction
                noise_reduced_path = os.path.join(subject_path, os.path.splitext(file_name)[0] + "_reduced.wav")
                reduce_noise(input_path, noise_reduced_path)

                # Upload the .wav file to Cloud Storage
                cloud_uri = f"gs://{bucket_name}/{subject_folder}/{os.path.basename(noise_reduced_path)}"
                upload_to_cloud_storage(noise_reduced_path, f"{subject_folder}/{os.path.basename(noise_reduced_path)}")

                # Transcribe audio from Cloud Storage with speaker diarization
                transcription = transcribe_audio_from_gcs(cloud_uri, timeout=custom_timeout)
                print(f"Transcription for {file_name}:\n{transcription[:100]}...")  # Print a short preview

                # Save the transcription to a text file
                transcription_path = os.path.join(output_folder, os.path.splitext(file_name)[0] + ".txt")
                with open(transcription_path, "w", encoding="utf-8") as text_file:
                    text_file.write(transcription)

                # Clean up the local .wav file after uploading
                os.remove(noise_reduced_path)
                print(f"Finished processing {file_name}.")
    print(f"Finished processing subject folder: {subject_folder}.")
