import argparse
from faster_whisper import WhisperModel
from tqdm import tqdm

def transcribe_audio(wav_path, language=None):
    # Initialize Whisper Model
    model = WhisperModel("base", device="cpu", compute_type="int8")

    # Run transcription
    segments, info = model.transcribe(wav_path, language=language, beam_size=5)

    # Print detected language
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    # Collect results with progress bar
    transcript = ""
    for segment in tqdm(segments, desc="Transcribing", unit="segment"):
        transcript += f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}\n"
    
    return transcript.strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe a WAV file using Faster-Whisper")
    parser.add_argument("wav_path", type=str, help="Path to the .wav file")
    parser.add_argument("--language", type=str, help="Optional language parameter", default=None)
    args = parser.parse_args()

    # Transcribe and print the text
    text = transcribe_audio(args.wav_path, args.language)
    print(f"Transcription:\n{text}")
