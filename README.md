# BlogAI 🤖✍️

Turn any topic or YouTube video into a full blog post — instantly.

🔗 **Live Demo:** [Try it here](https://agntic-blog-generation-kv4avhdgfeghgazpkrbn4w.streamlit.app/)

---

## What's this?

BlogAI is an agentic AI app built with LangGraph that generates structured blog posts from either a **topic** or a **YouTube link**. Paste a YT URL and it pulls the transcript, reads it, and writes a blog based on the actual video content. No fluff, no templates.

---

## How it works

Two flows, both powered by LLaMA 3.3 70B on Groq:

```
Topic Input
  └── title_creation → content_generation → Blog ✅

YouTube URL
  └── yt_transcript → title_creation → content_generation → Blog ✅
```

Each step is a LangGraph node. They share a common state object — each node reads what it needs and writes back only what it produces.

---

## Features

- 📝 **Topic → Blog** — type any topic, get a full markdown blog
- 🎥 **YouTube → Blog** — paste any YT link, get a blog from the video's content
- 🌐 **Auto English output** — works even if the video transcript is in another language
- 🎨 **Clean Streamlit UI** — dark theme, sidebar navigation, no clutter
- ⚡ **Fast** — Groq's LLaMA 3.3 70B is genuinely quick

---

## Tech Stack

| | |
|---|---|
| LLM | LLaMA 3.3 70B (Groq) |
| Agent Framework | LangGraph + LangChain |
| Backend | FastAPI |
| Frontend | Streamlit |
| Transcript | youtube-transcript-api |
| Backend Deploy | Render |
| Frontend Deploy | Streamlit Cloud |

---

## Project Structure

```
agntic-blog-generation/
├── app.py                     # FastAPI — /blogs and /blogs/yt routes
├── streamlit_app.py           # Streamlit frontend
├── src/
│   ├── graphs/
│   │   └── graph_builder.py   # LangGraph graph (topic + yt flows)
│   ├── nodes/
│   │   ├── blog_node.py       # Title + content generation nodes
│   │   └── yt_node.py         # YouTube transcript extraction
│   ├── states/
│   │   └── blogstate.py       # Shared state TypedDict
│   └── llms/
│       └── groqllm.py         # Groq LLM setup
├── requirements.txt
└── .env                       # API keys (not on GitHub)
```

---

## Setup & Run

### 1. Clone

```bash
git clone https://github.com/singh-105/agntic-blog-generation
cd agntic-blog-generation
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create `.env`

```env
GROQ_API_KEY=your_groq_key
LANGCHAIN_API_KEY=your_langsmith_key
```

Get your Groq key → [console.groq.com](https://console.groq.com)

### 4. Start backend

```bash
python app.py
# runs on http://localhost:8000
```

### 5. Start frontend

```bash
streamlit run streamlit_app.py
# opens at http://localhost:8501
```

---

## API

### `POST /blogs`
```json
{ "topic": "How transformers changed NLP" }
```

### `POST /blogs/yt`
```json
{ "yt_url": "https://www.youtube.com/watch?v=..." }
```

Both return:
```json
{
  "data": {
    "blog": {
      "title": "...",
      "content": "..."
    }
  }
}
```

> YouTube videos need captions enabled (auto-generated works fine).

---

## Limitations

- Videos without captions won't work
- Transcript is currently capped at ~3000 characters (best for 10–20 min videos)
- Private or age-restricted videos can't be accessed