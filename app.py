import streamlit as st
import requests
import base64

st.set_page_config(page_title="QuickScribe AI", page_icon="📝", layout="wide")

# 🌟 CSS for clear fonts + better colors
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #f8f9fa, #dde2f0, #e1f5fe);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.app-header {
    padding: 20px;
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(12px);
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}
.app-header h1 {
    font-size: 50px;
    font-weight: 800;
    color: #2c3e50;
}
.app-header p {
    font-size: 20px;
    color: #34495e;
}
.card {
    background: #ffffffdd;
    padding: 30px;
    border-radius: 14px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}
.stButton > button {
    background: #3498db;
    color: white;
    font-weight: bold;
    padding: 12px 30px;
    border: none;
    border-radius: 8px;
    font-size: 16px;
}
.stButton > button:hover {
    background: #2980b9;
}
.progress-container {
    width: 100%;
    background: #ccc;
    border-radius: 8px;
    margin-top: 5px;
}
.progress-bar {
    height: 10px;
    border-radius: 8px;
    background: linear-gradient(90deg, #3498db, #9b59b6);
}
.footer {
    text-align: center;
    font-size: 14px;
    color: #555;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# 🌟 Header
st.markdown("""
<div class="app-header">
    <h1>QuickScribe AI</h1>
    <p>Summarize smarter ✨ Read faster ⚡ Learn better 🚀</p>
</div>
""", unsafe_allow_html=True)

# 🌟 Input section
st.markdown('<div class="card">', unsafe_allow_html=True)

model = st.selectbox("🤖 Choose summarizer model:", [
    "sshleifer/distilbart-cnn-12-6", 
    "t5-small", 
    "google/pegasus-xsum"
])

user_input = st.text_area("📝 Paste your notes below:", height=200)

words = len(user_input.split())
chars = len(user_input)
st.caption(f"📊 Words: {words} | Characters: {chars}")

max_chars = 1024
percent = min(int((chars / max_chars) * 100), 100)

st.markdown(f"""
<div class="progress-container">
  <div class="progress-bar" style="width:{percent}%"></div>
</div>
""", unsafe_allow_html=True)

if chars > max_chars:
    st.warning("⚠ Your input exceeded the limit. It will be trimmed.")
    user_input = user_input[:max_chars]

summarize = st.button("✨ Generate Summary")
st.markdown('</div>', unsafe_allow_html=True)

# 🌟 Output section
if summarize:
    if not user_input.strip():
        st.warning("Please enter some text to summarize!")
    else:
        with st.spinner("Generating your summary..."):
            API_URL = f"https://api-inference.huggingface.co/models/{model}"
            headers = {"Authorization": "Bearerhf_vnMBivaIEfEkKWHhIKPiaFBjWdaaAinsNf"}  # Replace with your token
            payload = {"inputs": user_input}
            r = requests.post(API_URL, headers=headers, json=payload)

            if r.status_code == 200:
                try:
                    summary = r.json()[0]["summary_text"]
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.success("✅ Summary generated successfully!")
                    st.markdown(f"<div style='font-size:18px; color:#2c3e50;'>{summary}</div>", unsafe_allow_html=True)

                    st.download_button("📥 Download Summary", summary, "summary.txt", "text/plain")

                    b64 = base64.b64encode(summary.encode()).decode()
                    st.markdown(
                        f'<a href="data:text/plain;base64,{b64}" download="summary.txt">'
                        f'<button style="background:#9b59b6; color:white; padding:10px 20px; border:none; border-radius:6px;">📋 Copy to Clipboard (Download small txt)</button></a>',
                        unsafe_allow_html=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Parse error: {e}")
                    st.json(r.json())
            else:
                st.error(f"API Error {r.status_code}: {r.text}")

# 🌟 Footer
st.markdown('<div class="footer">© 2025 QuickScribe AI | Built with ❤️ using Streamlit + Hugging Face</div>', unsafe_allow_html=True)
