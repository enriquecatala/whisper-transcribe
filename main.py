import argparse
import wave
import os
from faster_whisper import WhisperModel
from tqdm import tqdm


def get_wav_duration(wav_path):
    with wave.open(wav_path, 'r') as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
    return round(duration)

def transcribe_audio(wav_path, language=None, model_size="base", device="cpu", compute_type="int8"):
    # Initialize Whisper Model
    model = WhisperModel(model_size, device=device, compute_type=compute_type)

    # Get WAV file duration
    wav_duration = get_wav_duration(wav_path)

    # Run transcription with the generator
    segments, info = model.transcribe(wav_path, language=language, beam_size=5)

    # Print detected language
    print("Detected language '%s' with probability %.2f" % (info.language, info.language_probability))

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

            # Update progress bar description with average segment duration and estimated time to completion
            avg_duration = total_duration / total_segments if total_segments > 0 else 0
            estimated_time_left = (wav_duration - total_duration) / avg_duration if avg_duration > 0 else 0
            pbar.set_postfix(est_time_left=f"{estimated_time_left:.2f}s")
            pbar.update(round(segment_duration, 2))
    
    return transcript.strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe a WAV file using Faster-Whisper")
    parser.add_argument("wav_path", type=str, help="Path to the .wav file")
    parser.add_argument("--language", type=str, help="Optional language parameter", default=None)
    parser.add_argument("--model_size", type=str, help="Model size to use (default: base). Example: large-v2", default="base")
    parser.add_argument("--device", type=str, help="Device to use for inference (default: cpu). Example: gpu", default="cpu")
    parser.add_argument("--compute_type", type=str, help="Compute type to use (default: int8). Example: float16", default="int8")
    
    args = parser.parse_args()

    # Transcribe and write the text to a .txt file
    text = transcribe_audio(args.wav_path, args.language, args.model_size, args.device, args.compute_type)
    txt_path = os.path.splitext(args.wav_path)[0] + ".txt"
    with open(txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(text)
    
    print(f"Transcription written to {txt_path}")
