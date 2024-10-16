import argparse
from faster_whisper import WhisperModel

def transcribe_audio(wav_path, language=None):
    # Initialize Whisper Model
    model = WhisperModel("base", device="cpu", compute_type="int8")

    # Run transcription
    segments, info = model.transcribe(wav_path, language=language)

    # Collect results
    transcript = ""
    for segment in segments:
        transcript += f"{segment.text} "
    
    return transcript.strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe a WAV file using Faster-Whisper")
    parser.add_argument("wav_path", type=str, help="Path to the .wav file")
    parser.add_argument("--language", type=str, help="Optional language parameter", default=None)
    args = parser.parse_args()

    # Transcribe and print the text
    text = transcribe_audio(args.wav_path, args.language)
    print(f"Transcription: {text}")
