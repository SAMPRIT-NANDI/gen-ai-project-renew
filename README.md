# Gemini AI Chatbot - Streamlit App

## 🎯 Features
- 🚀 Fast Gemini 2.5 Flash conversations via LangChain
- 📄 Optional webpage context (RAG-like)
- 🎨 Beautiful responsive UI
- 🔑 API key in `.streamlit/secrets.toml`
- Minimal deps, production ready

## 🏃 Local Run
```
pip install -r requirements.txt
streamlit run streamlit_app.py
```
Open http://localhost:8501

## ☁️ Deploy to Streamlit Cloud (5 mins)
1. Push to GitHub repo
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. "Deploy an app" → Connect GitHub repo
4. Select `streamlit_app.py`
5. **Advanced**: Add `GOOGLE_API_KEY` in secrets
6. Deploy!

App live instantly. Free tier ok for testing.

## 🔧 Requirements
See `requirements.txt`

## 📝 Secrets.toml (local + cloud)
```
GOOGLE_API_KEY = "your_key_here"
```

## 🎉 Test
- Chat normally
- Sidebar: Add URL → "Add Context"
- Clear anytime

Made simple & deployable! 🚀
