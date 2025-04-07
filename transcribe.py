import whisper

# Load the pre-trained model; "base" is a good starting point.
model = whisper.load_model("base")

# Specify the path to your audio file. Supported formats include .mp3, .wav, etc.
audio_file = "audio.mp3"

# Perform the transcription.
result = model.transcribe(audio_file)

# Print the transcribed text.
print("Transcribed Text:")
print(result["text"])