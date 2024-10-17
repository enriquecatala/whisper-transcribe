# whisper-transcribe
FastWhisper Audio-to-Text: Efficient Transcription of .wav Files Using FastWhisper" A command-line tool for transcribing .wav files to text quickly and accurately using the FastWhisper library. Includes optional language detection and GPU acceleration support.

# Transcribe

```bash
python main.py audio/audio.wav  # this will automatically detect the language
python main.py audio/audio.wav --language en
```

# Export audio from video

```bash
ffmpeg -i video.mp4 -vn -acodec pcm_s16le -ar 44100 -ac 2 audio/audio.wav
ffmpeg -i video.mp4 -vn -acodec aac -ar 44100 -ac 2 audio/audio.m4a

```

# Prompts to get summary from the output

Use those prompts with your output to get your summary using another LLM

## Prompt for Summary to Save in Your Notes

---Please provide a comprehensive summary of the meeting, including the main points discussed, key decisions made, action items assigned, and any important deadlines. Highlight any critical insights or strategic directions mentioned during the meeting. Additionally, include any follow-up actions required and the responsible parties. Write it like if it was me writing the notes, I´m Enrique.

## Prompt for Summary to Share with Participants

---Please provide a concise summary of our meeting for distribution to all participants. Include the main topics covered, key decisions made, action items assigned, and respective deadlines. Highlight any important insights or agreements reached. Ensure that the summary is clear and actionable for all attendees. Write it like if it was me writing the notes, , I´m Enrique.
