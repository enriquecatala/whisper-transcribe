# whisper-transcribe
FastWhisper Audio-to-Text: Efficient Transcription of .wav Files Using FastWhisper" A command-line tool for transcribing .wav files to text quickly and accurately using the FastWhisper library. Includes optional language detection and GPU acceleration support.

# Transcribe

```bash
conda activate whisper-transcribe
python main.py audio/audio.wav  # this will automatically detect the language
python main.py audio/audio.wav --language en
# Performance options
python main.py audio/audio.wav --cpu_threads 8 --vad_filter True
```

# Export audio from video

```bash
# batch
./convert.sh /path/to/input ./audio/
# manual
ffmpeg -i video.mp4 -vn -acodec pcm_s16le -ar 44100 -ac 2 audio/audio.wav
ffmpeg -i video.mp4 -vn -acodec aac -ar 44100 -ac 2 audio/audio.m4a

```

# Prompts to get summary from the output

Use those prompts with your output to get your summary using another LLM

## Prompt for Summary to Save in Your Notes

---Please provide a comprehensive summary of the meeting, including the main points discussed, key decisions made, action items assigned, and any important deadlines. Highlight any critical insights or strategic directions mentioned during the meeting. Additionally, include any follow-up actions required and the responsible parties. Write it like if it was me writing the notes, I´m Enrique.



## Prompt for Summary to Share with Participants

---Please provide a concise summary of our meeting for distribution to all participants. Include the main topics covered, key decisions made, action items assigned, and respective deadlines. Highlight any important insights or agreements reached. Ensure that the summary is clear and actionable for all attendees. Write it like if it was me writing the notes, , I´m Enrique.

## Prompt for RAG 

```
Summarize the following transcript in a **highly structured and information-dense manner**, ensuring all key points, discussions, and conclusions are captured with precision. Attribute contributions to specific participants where possible, preserving critical phrasing, questions, and terminology.

Omit only **irrelevant or redundant sections**, but **retain all contextually significant details** to ensure optimal retrieval in a **Retrieval-Augmented Generation (RAG) system**.

#### **Output format:**
The summary must follow this structured format:

**1. Introduction**  
- Briefly describe the purpose of the discussion, participants, and key topics.  

**2. Key Discussions**  
- Organize content into **clear subtopics with headers**.  
- Include **specific arguments, counterpoints, and supporting evidence**.  
- Maintain original wording for key phrases, quotes, and **questions asked**.  
- Use **short, concise bullet points** for improved tokenization.  

**3. Decisions & Action Items**  
- Explicitly state **decisions made**, next steps, and assigned responsibilities.  

**4. Key Insights & Context**  
- Capture any **background knowledge, definitions, or external references** that add useful context.  

### **Additional Instructions for RAG Optimization:**
- **Avoid unnecessary abstraction**—prioritize **factual, structured, and well-segmented content** for efficient retrieval.  
- **Ensure the summary retains specific terminology and wording** that might match user queries in a retrieval system.  
- **Do not remove valuable details**, even if they seem secondary; a future query may require them.  
---
```
