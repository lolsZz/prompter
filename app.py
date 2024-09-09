import streamlit as st
import os
from prompter import Prompter
import warnings
from litellm import completion
import glob

# Set page config
st.set_page_config(page_title="AI Prompter", page_icon="🤖", layout="wide")

# Set your API key (consider using st.secrets for better security)
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Get list of XML files
xml_files = glob.glob('*.xml')

# Sidebar for XML template selection
selected_xml = st.sidebar.selectbox(
    "Choose XML template",
    xml_files,
    index=xml_files.index('tm_prompt.xml') if 'tm_prompt.xml' in xml_files else 0
)

st.session_state.prompter = Prompter(selected_xml)

# Title
st.title("AI Prompter")

# Sidebar for model selection
model = st.sidebar.selectbox(
    "Choose an LLM model",
    ("bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0", "gpt-3.5-turbo", "gpt-4"),
    index=0  # Set the default to the first option (Claude 3)
)

# User input
user_input = st.text_area("Enter your query:", height=100, key="user_input")

if st.button("Generate Prompt"):
    if user_input:
        with st.spinner("Generating prompt..."):
            generated_prompt = st.session_state.prompter.generate_prompt(user_input)

        st.subheader("Generated Prompt:")
        st.text_area("", value=generated_prompt, height=300)

        # You can add more visualizations or analysis here
    else:
        st.warning("Please enter a query.")

if st.button("Generate AI Response"):
    if user_input:
        with st.spinner("Generating AI response..."):
            prompt = st.session_state.prompter.generate_prompt(user_input)
            ai_response = completion(model=model, messages=[{"role": "user", "content": prompt}])
            st.text_area("AI Response:", value=ai_response.choices[0].message.content, height=300)
    else:
        st.warning("Please enter a query.")

# Add some information about the app
st.sidebar.markdown("## About")
st.sidebar.info(f"This app generates AI prompts based on the structure defined in {selected_xml}.")
st.sidebar.info(f"Current XML template: {selected_xml}")

# Add a footer
st.markdown("---")
st.markdown("Developed with ❤️ using Streamlit")
