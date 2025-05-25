import streamlit as st
import google.generativeai as genai

# 🔑 Paste your API key directly here
GOOGLE_API_KEY = "AIzaSyBkqGIHS7iY8fLt5N__OEJELyD8aMoVVOs"

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Function to clean article
def clean_article(text, tone):
    prompt = f"""
    Clean the following Urdu news article:
    - Fix grammar and sentence structure
    - Apply a {tone} tone

    Article:
    \"\"\"{text}\"\"\"
    """
    response = model.generate_content(prompt)
    return response.text.strip()

# Function to generate 2 headlines
def generate_headlines(text, tone):
    prompt = f"""
    Generate two headlines (15 words max each) in {tone} tone for this Urdu article.

    Article:
    \"\"\"{text}\"\"\"

    1.
    2.
    """
    response = model.generate_content(prompt)
    lines = response.text.strip().split("\n")
    headlines = [line.replace("1.", "").replace("2.", "").strip() for line in lines if line.strip()]
    return headlines[:2]

# UI
st.set_page_config(page_title="📰 Urdu News Headline Generator")
st.title("📰 Urdu News Headline Generator")

article = st.text_area("📝 Paste Urdu News Article:", height=200)
tone = st.selectbox("🎭 Select Tone:", ["Neutral", "Formal", "Dramatic", "Funny", "Sensational", "Inspiring"])

if st.button("Generate"):
    if article.strip():
        with st.spinner("Processing..."):
            cleaned = clean_article(article, tone)
            headlines = generate_headlines(cleaned, tone)

        st.subheader("📃 Cleaned Article")
        st.write(cleaned)

        st.subheader("📝 Headlines")
        for i, h in enumerate(headlines, 1):
            st.markdown(f"**{i}.** {h}")
    else:
        st.warning("Please enter an article.")
