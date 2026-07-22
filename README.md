# 🤖 AI Chat Assistant - Streamlit App

A beautiful, production-ready AI chat application with URL context loading, multiple LLM support (Google Gemini and Groq Llama 3), and Streamlit Cloud deployment ready! Perfect for your resume! 🚀

## ✨ Features

- 🔄 **Multiple LLMs**: Switch between Google Gemini 1.5 Flash and Groq Llama 3
- 🌐 **URL Context Loading**: Load content from any URL to use as context
- 💬 **Interactive Chat**: Clean, modern chat interface
- 🎨 **Beautiful UI**: Responsive design with Streamlit
- 🚀 **Deploy Ready**: One-click deploy to Streamlit Cloud

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLMs**: Google Gemini (via LangChain), Groq Llama 3
- **Web Scraping**: BeautifulSoup4, Requests
- **Deployment**: Streamlit Cloud

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd gen-ai-project-renew
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Secrets

Create a `.streamlit/secrets.toml` file in the project root:
```toml
GOOGLE_API_KEY = "your-google-api-key"
GROQ_API_KEY = "your-groq-api-key"
```

### 4. Run the App
```bash
streamlit run streamlit_app.py
```
Open http://localhost:8501 in your browser!

## ☁️ Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Connect your GitHub repo and select `streamlit_app.py`
5. In the "Advanced settings" section, add your secrets:
   ```toml
   GOOGLE_API_KEY = "your-google-api-key"
   GROQ_API_KEY = "your-groq-api-key"
   ```
6. Deploy! 🎉

## 📖 How to Use

1. **Choose an LLM**: Select between Gemini or Groq (Llama 3) in the sidebar
2. **Load Context (Optional)**: Enter a URL and click "Load Context" to add website content
3. **Chat**: Ask questions! If context is loaded, the AI will use that information

## 📁 Project Structure

```
gen-ai-project-renew/
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml      # API keys (don't commit to GitHub!)
├── streamlit_app.py      # Main application
├── requirements.txt      # Dependencies
└── README.md
```

## 🎯 Resume Highlights

- Full-stack AI application development
- Integration with multiple LLM providers (Google, Groq)
- Web scraping with BeautifulSoup
- Modern UI/UX with Streamlit
- Production-ready deployment configuration
- Secret management best practices
- Context-aware AI responses

## 📝 Notes

- Keep your API keys secure! Never commit `secrets.toml` to GitHub
- The app uses a 5000-character limit for URL context to stay within token limits
- You can get free API keys from:
  - [Google AI Studio](https://aistudio.google.com)
  - [Groq Console](https://console.groq.com)

---
Built with ❤️ using Streamlit, LangChain, and Groq!
