# Streamlit Deployment for URL Chatbot - Make Easily Deployable

## Status: Local Test Pending

### Deployment Steps:
1. [✅] Create requirements.txt with dependencies (pinned for Cloud)
2. [✅] Create .streamlit/config.toml for config
3. [✅] Update streamlit_app.py to use st.secrets for API key
4. [✅] Update README.md with deploy instructions
5. [ ] Test locally: `pip install -r requirements.txt && streamlit run streamlit_app.py` (set GOOGLE_API_KEY)
6. [ ] Deploy to Streamlit Cloud: Connect GitHub repo, add GOOGLE_API_KEY secret

**Terminal commands for local test:**
```
cd "c:/Users/SAMPRIT/OneDrive/Desktop/resume/GEN_AI-BCT-FINAL-PROJECT"
set GOOGLE_API_KEY=your_actual_key_here
pip install -r requirements.txt
streamlit run streamlit_app.py
```

**Streamlit Cloud Notes:**
- Pinned requirements.txt to avoid version conflicts
- Added google-generativeai + requests explicitly
- Ensure GOOGLE_API_KEY in app secrets

**Next:** Run local test before Cloud redeploy.

