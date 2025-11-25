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
    return duration

def transcribe_audio(model, wav_path, language=None, include_segments_start_end=False, vad_filter=True):
    wav_duration = get_wav_duration(wav_path)
    segments, info = model.transcribe(wav_path, language=language, beam_size=5, vad_filter=vad_filter)
    print("Detected language '%s' with probability %.2f" % (info.language, info.language_probability))
    transcript = ""
    total_segments = 0
    total_duration = 0.0

    with tqdm(total=wav_duration, unit="s", desc="Transcribing") as pbar:
        for segment in segments:
            if include_segments_start_end:
                line = f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}"
            else:
                line = f"{segment.text}"
            
            transcript += line + "\n"
            tqdm.write(line)
            
            # Update progress bar to match the end of the current segment
            # This handles potential silence gaps correctly by jumping to the segment end
            pbar.update(segment.end - pbar.n)
    
    return transcript.strip()

def process_directory(model, directory, language, include_segments_start_end, vad_filter):
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            wav_path = os.path.join(directory, filename)
            print(f"Processing file: {filename}")
            text = transcribe_audio(model, wav_path, language, include_segments_start_end, vad_filter)
            txt_path = os.path.splitext(wav_path)[0] + ".txt"
            with open(txt_path, "w", encoding="utf-8") as txt_file:
                txt_file.write(text)
            print(f"Transcription written to {txt_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe WAV files using Faster-Whisper")
    parser.add_argument("path", type=str, help="Path to the .wav file or directory containing .wav files")
    parser.add_argument("--language", type=str, help="Optional language parameter", default=None)
    parser.add_argument("--model_size", type=str, help="Model size to use (default: base). Example: large-v2", default="base")
    parser.add_argument("--device", type=str, help="Device to use for inference (default: cpu). Example: gpu", default="cpu")
    parser.add_argument("--compute_type", type=str, help="Compute type to use (default: int8). Example: float16", default="int8")
    parser.add_argument("--include_segments_start_end", type=bool, help="Include segments start-end in the output", default=False)
    parser.add_argument("--cpu_threads", type=int, help="Number of threads to use for CPU inference (default: 4)", default=4)
    parser.add_argument("--vad_filter", type=bool, help="Enable VAD filter to skip silence (default: True)", default=True)
    
    args = parser.parse_args()
    
    print(f"Loading model '{args.model_size}' on {args.device} with {args.compute_type} precision...")
    model = WhisperModel(
        args.model_size, 
        device=args.device, 
        compute_type=args.compute_type, 
        cpu_threads=args.cpu_threads
    )
    
    if os.path.isdir(args.path):
        process_directory(model, args.path, args.language, args.include_segments_start_end, args.vad_filter)
    else:
        text = transcribe_audio(model, args.path, args.language, args.include_segments_start_end, args.vad_filter)
        txt_path = os.path.splitext(args.path)[0] + ".txt"
        with open(txt_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(text)
        print(f"Transcription written to {txt_path}")
