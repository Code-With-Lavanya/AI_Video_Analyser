# 🎥 AI Video Assistant

An AI-powered Video & Audio Analysis Assistant that transforms long-form content into actionable insights.

Upload a YouTube video, MP3, MP4, WAV, or M4A file and the system automatically:

* Generates accurate transcripts using Faster-Whisper
* Creates concise AI summaries
* Extracts action items, key decisions, and open questions
* Enables intelligent Q&A with the uploaded content using RAG (Retrieval-Augmented Generation)

---

## 🚀 Features

### 🎙️ Multi-Format Input Support

Supports:

* YouTube URLs
* MP3
* MP4
* WAV
* M4A

### 📝 AI Transcription

Uses Faster-Whisper for fast and accurate speech-to-text conversion.

### 📋 Smart Summarization

Automatically generates:

* Meeting Summary
* Key Insights
* Important Highlights

### ✅ Action Item Extraction

Identifies:

* Tasks
* Responsibilities
* Follow-ups

### 🔑 Key Decision Detection

Extracts major decisions discussed in the content.

### ❓ Open Question Detection

Identifies unresolved topics and follow-up discussions.

### 💬 Chat with Your Content

Ask questions about the uploaded audio/video and receive answers grounded only in the transcript.

Examples:

* What is the main topic?
* What decisions were made?
* Summarize the discussion.
* What action items were assigned?

### 🧠 RAG-Powered Search

Uses:

* LangChain
* Chroma Vector Database
* HuggingFace Embeddings

to retrieve relevant transcript chunks before generating answers.

---

## 🏗️ Tech Stack

### AI & NLP

* Faster-Whisper
* LangChain
* Mistral AI
* HuggingFace Embeddings

### Vector Database

* ChromaDB

### Backend

* Python

### Frontend

* Streamlit

### Media Processing

* FFmpeg
* yt-dlp

---

## ⚙️ Architecture

```text
User Input
     │
     ▼
Audio / Video Extraction
     │
     ▼
Faster-Whisper Transcription
     │
     ▼
Transcript Generation
     │
     ├────────► AI Summary
     │
     ├────────► Action Items
     │
     ├────────► Key Decisions
     │
     └────────► Open Questions
     │
     ▼
Vector Embeddings
     │
     ▼
Chroma Vector Store
     │
     ▼
Retriever
     │
     ▼
Mistral LLM
     │
     ▼
Chat with Your Content
```

---

## 📂 Project Structure

```bash
AI-Video-Assistant/
│
├── app.py
├── requirements.txt
│
├── core/
│   ├── transcriber.py
│   ├── summarizer.py
│   ├── extractor.py
│   ├── rag_engine.py
│   └── vector_store.py
│
├── utils/
│   └── audio_processor.py
│
└── downloads/
```

---

## 🔧 Installation

### Clone Repository

```bash
git clone https://github.com/your-username/ai-video-assistant.git

cd ai-video-assistant
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install FFmpeg

Download FFmpeg and add it to your system PATH.

---

## 🔑 Environment Variables

Create a `.env` file:

```env
MISTRAL_API_KEY=your_api_key
SARVAM_API_KEY=your_api_key
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

---

## 📸 Sample Workflow

1. Upload a video/audio file.
2. Generate transcript.
3. View AI-generated summary.
4. Review action items and decisions.
5. Ask questions using the chat interface.

---

## 🎯 Use Cases

* Meeting Analysis
* Lecture Summarization
* Podcast Understanding
* YouTube Video Insights
* Interview Analysis
* Research Content Review

---

## 📈 Future Improvements

* Speaker Diarization
* Multi-language Support
* PDF Export
* Email Summary Generation
* Sentiment Analysis
* Video Timestamp Referencing
* Cloud Storage Integration

---

## 👨‍💻 Author

**Lucky**

Built to simplify long-form content analysis using Generative AI, RAG, and Speech Intelligence.
