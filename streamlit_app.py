import streamlit as st
import requests

API_BASE = "http://localhost:8000"

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="BlogAI",
    page_icon="✍️",
    layout="wide",
)

# ── Minimal custom CSS ────────────────────────────────────────
st.markdown("""
<style>
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f0f0f;
    }
    [data-testid="stSidebar"] * {
        color: #f0f0f0 !important;
    }

    /* Main background */
    .stApp {
        background-color: #111111;
        color: #f0f0f0;
    }

    /* Blog output card */
    .blog-card {
        background: #1a1a1a;
        border: 1px solid #2e2e2e;
        border-radius: 12px;
        padding: 2rem;
        margin-top: 1.5rem;
    }

    .blog-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
        border-bottom: 2px solid #444;
        padding-bottom: 0.5rem;
    }

    /* Button */
    .stButton > button {
        background-color: #7c3aed;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        transition: background 0.2s;
    }
    .stButton > button:hover {
        background-color: #6d28d9;
    }

    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #1e1e1e;
        color: #f0f0f0;
        border: 1px solid #333;
        border-radius: 8px;
    }

    /* Hide streamlit default footer */
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ✍️ BlogAI")
    st.markdown("---")
    mode = st.radio(
        "Choose mode",
        ["📝 Topic Blog", "🎥 YouTube Blog"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("**How it works**")
    if mode == "📝 Topic Blog":
        st.markdown("Enter any topic → AI writes a full blog post.")
    else:
        st.markdown("Paste a YouTube link → AI reads the video and writes a blog from it.")


# ── Main area ─────────────────────────────────────────────────
if mode == "📝 Topic Blog":
    st.markdown("## 📝 Generate Blog from Topic")
    topic = st.text_input("Enter a topic", placeholder="e.g. The future of AI in healthcare")

    if st.button("Generate Blog"):
        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Writing your blog..."):
                try:
                    res = requests.post(
                        f"{API_BASE}/blogs",
                        json={"topic": topic}
                    )
                    data = res.json()

                    if "data" in data:
                        blog = data["data"]["blog"]
                        st.markdown(f"""
                        <div class="blog-card">
                            <div class="blog-title">{blog['title']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(blog["content"])
                    else:
                        st.error(f"Error: {data}")

                except Exception as e:
                    st.error(f"Could not connect to API: {e}")

else:
    st.markdown("## 🎥 Generate Blog from YouTube Video")

    def generate_yt_blog(url):
        with st.spinner("Fetching transcript and writing blog..."):
            try:
                res = requests.post(
                    f"{API_BASE}/blogs/yt",
                    json={"yt_url": url}
                )
                data = res.json()
                if "data" in data:
                    blog = data["data"]["blog"]
                    st.markdown(f"""
                    <div class="blog-card">
                        <div class="blog-title">{blog['title']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(blog["content"])
                else:
                    st.error(f"Error: {data}")
            except Exception as e:
                st.error(f"Could not connect to API: {e}")

    yt_url = st.text_input("Paste YouTube link", placeholder="https://www.youtube.com/watch?v=...", key="yt_input")

    if yt_url.strip():
        generate_yt_blog(yt_url)