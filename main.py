import argparse
import wave
from faster_whisper import WhisperModel
from tqdm import tqdm

def get_wav_duration(wav_path):
    with wave.open(wav_path, 'r') as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
    return round(duration) # quito los decimales

def transcribe_audio(wav_path, language=None):
    # Initialize Whisper Model
    model = WhisperModel("base", device="cpu", compute_type="int8")

    # Get WAV file duration
    wav_duration = get_wav_duration(wav_path)

    # Run transcription with the generator
    segments, info = model.transcribe(wav_path, language=language, beam_size=5)

    # Print detected language
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    # Collect results with progress bar
    transcript = ""
    total_segments = 0
    total_duration = 0.0

    with tqdm(desc="Transcribing", unit="segment", total=round(wav_duration)) as pbar:
        for segment in segments:
            transcript += f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}\n"
            total_segments += 1
            segment_duration = segment.end - segment.start
            total_duration += segment_duration

            pbar.update(round(segment_duration, 2))
    
    return transcript.strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe a WAV file using Faster-Whisper")
    parser.add_argument("wav_path", type=str, help="Path to the .wav file")
    parser.add_argument("--language", type=str, help="Optional language parameter", default=None)
    args = parser.parse_args()

    # Transcribe and print the text
    text = transcribe_audio(args.wav_path, args.language)
    print(f"Transcription:\n{text}")
