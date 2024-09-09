import streamlit as st
import os
from prompter import Prompter

# Set page config
st.set_page_config(page_title="AI Prompter", page_icon="🤖", layout="wide")

# Initialize session state
if 'prompter' not in st.session_state:
    st.session_state.prompter = Prompter('tm_prompt.xml')

# Set your API key (consider using st.secrets for better security)
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Title
st.title("AI Prompter")

# Sidebar for model selection
model = st.sidebar.selectbox(
    "Choose an LLM model",
    ("gpt-3.5-turbo", "gpt-4", "anthropic.claude-3-sonnet-20240229")
)

# User input
user_input = st.text_area("Enter your query:", height=100)

if st.button("Generate Prompt"):
    if user_input:
        with st.spinner("Generating prompt..."):
            generated_prompt = st.session_state.prompter.generate_prompt(user_input, model)

        st.subheader("Generated Prompt:")
        st.text_area("", value=generated_prompt, height=300)

        # You can add more visualizations or analysis here
    else:
        st.warning("Please enter a query.")

# Add some information about the app
st.sidebar.markdown("## About")
st.sidebar.info("This app generates AI prompts based on the structure defined in tm_prompt.xml.")
