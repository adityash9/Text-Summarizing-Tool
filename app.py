import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from googletrans import Translator  # For translation

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt template for text summarization
BASE_PROMPT = """You are a text summarizer. You will take the given input text 
and summarize it based on the requested format and language. 
Summarize in the format: {format}. Language: {language}. 
Please provide the summary of the text given here: """

# Translator for language support
translator = Translator()

# Function to generate summary using Gemini AI
def generate_gemini_summary(input_text, format, language):
    prompt = BASE_PROMPT.format(format=format, language=language)
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + input_text)
        return response.text
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return None

# Streamlit App Title
st.title("📄 Text Summarization Tool")

# Text input for summarization
input_text = st.text_area("📝 Enter the Text to Summarize:")

# Dropdown for summary format
format_option = st.selectbox(
    "📋 Select Summary Format:",
    ["Bullet Points", "Key Points", "Short Paragraph"]
)

# Dropdown for language selection
language_option = st.selectbox(
    "🌐 Select Language for Summary:",
    ["English", "Spanish", "French", "German", "Hindi", "Chinese", "Japanese", "Arabic"]
)

if st.button("Generate Summary"):
    if input_text.strip():
        with st.spinner("Generating summary using Gemini AI..."):
            # Generate summary based on selected format and language
            summary = generate_gemini_summary(
                input_text,
                format=format_option,
                language=language_option
            )

        if summary:
            st.markdown("### 📄 Summary:")
            st.write(summary)

            # Option to download the summary
            st.download_button(
                label="📥 Download Summary as Text File",
                data=summary,
                file_name="summary.txt",
                mime="text/plain"
            )
    else:
        st.error("Please enter some text to summarize!")
