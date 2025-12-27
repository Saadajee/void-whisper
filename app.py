import os
import streamlit as st
from groq import Groq
import tempfile
import base64
from dotenv import load_dotenv

# ENV
load_dotenv()
st.set_page_config(page_title="Void Whisper", layout="centered")

st.markdown("""
<style>
/* Main background with subtle animated gradient and stars */
.stApp {
    background: linear-gradient(-45deg, #0f001a, #1a0033, #000000, #0d0022);
    background-size: 400% 400%;
    animation: gradientShift 20s ease infinite;
    overflow: hidden;
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
/* Subtle floating particles effect */
.stApp::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: 
        radial-gradient(circle at 20% 80%, rgba(120, 20, 220, 0.1) 0%, transparent 10%),
        radial-gradient(circle at 80% 20%, rgba(20, 220, 220, 0.1) 0%, transparent 10%),
        radial-gradient(circle at 40% 40%, rgba(220, 20, 120, 0.08) 0%, transparent 15%);
    pointer-events: none;
    animation: floatParticles 30s linear infinite;
}
@keyframes floatParticles {
    0% { transform: translate(0, 0); }
    100% { transform: translate(100px, -100px); }
}

/* Chat messages with neon glow */
[data-testid="stChatMessage"] {
    background-color: rgba(15, 10, 35, 0.6) !important;
    border: 1px solid rgba(100, 50, 200, 0.4);
    border-radius: 16px;
    padding: 1.2rem;
    backdrop-filter: blur(8px);
    box-shadow: 
        0 0 15px rgba(138, 43, 226, 0.3),
        inset 0 0 10px rgba(138, 43, 226, 0.1);
    margin-bottom: 1rem;
}
div[data-testid="chat-message-user"] {
    background-color: rgba(10, 30, 60, 0.6) !important;
    border-left: 4px solid #00ffff;
    box-shadow: 
        0 0 15px rgba(0, 255, 255, 0.3),
        inset 0 0 10px rgba(0, 255, 255, 0.1);
}
div[data-testid="chat-message-assistant"] {
    background-color: rgba(40, 10, 60, 0.6) !important;
    border-left: 4px solid #bb86fc;
    box-shadow: 
        0 0 15px rgba(187, 134, 252, 0.4),
        inset 0 0 10px rgba(187, 134, 252, 0.15);
}

/* Header with stronger neon glow */
h1 {
    color: #bb86fc;
    text-align: center;
    text-shadow: 
        0 0 10px #bb86fc,
        0 0 20px #bb86fc,
        0 0 30px #9932cc;
    font-family: 'Orbitron', 'Courier New', monospace;
    font-size: 3rem;
    letter-spacing: 4px;
    margin-bottom: 0.5rem;
}
p {
    color: #a0a0ff !important;
    text-align: center;
    font-style: italic;
    text-shadow: 0 0 8px rgba(160, 160, 255, 0.5);
}

/* Input bar with neon border glow */
.stChatFloatingInputContainer {
    background-color: rgba(20, 15, 40, 0.8) !important;
    border: 2px solid #bb86fc !important;
    border-radius: 20px !important;
    box-shadow: 
        0 0 20px rgba(187, 134, 252, 0.5),
        inset 0 0 10px rgba(187, 134, 252, 0.2);
    backdrop-filter: blur(5px);
}

/* Spinner with neon */
.stSpinner > div > div {
    border-top-color: #00ffff !important;
    border-left-color: #bb86fc !important;
}

/* Audio players with subtle glow */
audio {
    filter: drop-shadow(0 0 5px rgba(187, 134, 252, 0.4));
}

/* General text */
span, label, div {
    color: #e0e0ff !important;
}
</style>
""", unsafe_allow_html=True)

# Load custom font (Orbitron for futuristic feel)
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# HEADER
st.markdown("<h1>Void Whisper</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#a0a0ff;font-style:italic;text-shadow:0 0 8px rgba(160,160,255,0.5);'>A calm intelligence from the void</p>", unsafe_allow_html=True)

# GROQ CLIENT
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("Missing GROQ_API_KEY")
    st.stop()
client = Groq(api_key=api_key)

# SESSION STATE
if "llm_history" not in st.session_state:
    st.session_state.llm_history = []
if "ui_history" not in st.session_state:
    st.session_state.ui_history = []

# DISPLAY CHAT
for msg in st.session_state.ui_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("audio"):
            st.markdown(msg["audio"], unsafe_allow_html=True)

# INPUTS
user_text = st.chat_input("Speak or type into the void…")

st.markdown('<div class="mic-overlay">', unsafe_allow_html=True)
audio_bytes = st.audio_input(
    "Voice input",
    key="mic",
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# AUDIO → TEXT
is_voice = False
user_audio_html = ""
if audio_bytes:
    is_voice = True
    user_audio = base64.b64encode(audio_bytes.getvalue()).decode()
    user_audio_html = f"""
    <audio controls style="width:100%;margin-top:0.6rem">
        <source src="data:audio/wav;base64,{user_audio}">
    </audio>
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_bytes.getvalue())
        path = tmp.name
    try:
        with open(path, "rb") as f:
            user_text = client.audio.transcriptions.create(
                model="whisper-large-v3-turbo",
                file=f,
                response_format="text"
            ).strip()
    finally:
        os.unlink(path)

# HANDLE MESSAGE
if user_text:
    # USER
    with st.chat_message("user"):
        st.markdown(user_text)
        if is_voice:
            st.markdown(user_audio_html, unsafe_allow_html=True)
    user_msg = {"role": "user", "content": user_text}
    if is_voice:
        user_msg["audio"] = user_audio_html
    st.session_state.llm_history.append({"role": "user", "content": user_text})
    st.session_state.ui_history.append(user_msg)

    # ASSISTANT
    with st.chat_message("assistant"):
        with st.spinner("Listening to the void…"):
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are Void Whisper — calm, ancient, precise. "
                        "Speak briefly. Never ramble. "
                        "Your tone is thoughtful and restrained."
                    )
                },
                *st.session_state.llm_history
            ]
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.65,
                max_tokens=400
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

        # TTS
        audio_html = ""
        try:
            tts = client.audio.speech.create(
                model="canopylabs/orpheus-v1-english",
                voice="hannah",
                input=reply,
                response_format="wav"
            )
            audio = base64.b64encode(tts.read()).decode()
            audio_html = f"""
            <audio controls autoplay style="width:100%;margin-top:0.6rem">
                <source src="data:audio/wav;base64,{audio}">
            </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)
            audio_html_no_autoplay = audio_html.replace(' autoplay', '')
        except:
            audio_html_no_autoplay = ""

    st.session_state.llm_history.append({"role": "assistant", "content": reply})
    st.session_state.ui_history.append(
        {"role": "assistant", "content": reply, "audio": audio_html_no_autoplay}
    )