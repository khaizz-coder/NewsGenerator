import os
import streamlit as st
import google.generativeai as genai

# Set your API key using Streamlit secrets (configured on Streamlit Cloud)
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize model
model = genai.GenerativeModel("gemini-2.0-flash")

# Clean article
def clean_article(text, tone):
    prompt = f"""
    Clean the following Urdu article:
    - Fix grammar and structure
    - Apply a {tone} tone

    Article:
    \"\"\"{text}\"\"\"
    """
    response = model.generate_content(prompt)
    return response.text.strip()

# Generate two headlines
def generate_headlines(text, tone):
    prompt = f"""
    Generate two headlines for this Urdu article in a {tone} tone. Each under 15 words.

    Article:
    \"\"\"{text}\"\"\"

    1.
    2.
    """
    response = model.generate_content(prompt)
    lines = response.text.strip().split("\n")
    headlines = [line.replace("1.", "").replace("2.", "").strip() for line in lines if line.strip()]
    return headlines[:2]

# Streamlit UI
st.set_page_config(page_title="📰 Urdu News Headline Generator")
st.title("📰 Urdu News Headline Generator")

article = st.text_area("Paste Urdu News Article:", height=200)
tone = st.selectbox("Select Tone:", ["Neutral", "Formal", "Dramatic", "Funny", "Sensational", "Inspiring"])

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
