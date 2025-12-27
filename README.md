# Void Whisper

Void Whisper is a voice-enabled AI chat interface that blends text and speech into a calm, cosmic conversational experience.  
It features real-time voice transcription, spoken AI responses, and a visually immersive neon “void” UI powered by Groq.

---

## Features

- **Voice Input with Live Transcription**  
  Speak to the app and see your words transcribed instantly in chat.

- **AI Voice Responses (TTS)**  
  Assistant replies are spoken back using high-quality text-to-speech.

- **Persistent Chat History**  
  Text and voice messages are stored and replayed during the session.

- **Groq-Powered LLM**  
  Uses `llama-3.3-70b-versatile` for fast, high-quality responses.

- **Immersive Void UI**  
  Animated gradients, neon glow chat bubbles, and futuristic typography.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM API**: Groq
- **Speech-to-Text**: Whisper (`whisper-large-v3-turbo`)
- **Text-to-Speech**: Orpheus (`canopylabs/orpheus-v1-english`)
- **Styling**: Custom CSS + Google Fonts (Orbitron)

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Saadajee/void-whisper.git
cd void-whisper
```
2. Create Environment & Install Dependencies
```
conda create -n voidwhisper python=3.10
conda activate voidwhisper
pip install -r requirements.txt
```
3. Set Up Environment Variables
Create a .env file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
ELEVENLABS_API_KEY=elevenlabs
```
4. Run the App
```
streamlit run app.py
```
The app will be available at: 
http://localhost:8501

## How It Works
- Type a message or record your voice.
- Voice input is transcribed using Whisper.
- Conversation context is sent to Groq’s LLM.
- The AI responds with text and optional spoken audio.
- All messages (text + voice) persist in session history.

## Notes & Limitations

- Chat history is session-based (not persisted to disk/database).
- Streamlit currently limits true embedding of buttons inside st.chat_input.
- Best experienced on desktop with microphone access enabled.

## Future Enhancements
- Multi-session chat memory
- Push-to-talk recording
- Streaming token responses
- Persistent storage (SQLite / MongoDB)
- Mobile-optimized layout

“Speak, and the void shall answer.” 
