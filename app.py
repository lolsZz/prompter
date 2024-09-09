import streamlit as st
import os
from prompter import Prompter
import warnings
from litellm import completion
import xml.etree.ElementTree as ET
import os
import glob
import shutil

# Set page config
st.set_page_config(page_title="AI Prompter", page_icon="🤖", layout="wide")

# Set your API key (consider using st.secrets for better security)
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# File uploader in the sidebar
uploaded_file = st.sidebar.file_uploader("Upload a new XML prompt template", type="xml")

if uploaded_file is not None:
    # Save the uploaded file to the prompts folder
    with open(os.path.join("prompts", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.success(f"Uploaded {uploaded_file.name} successfully!")

    # Validate the uploaded XML
    try:
        tree = ET.parse(os.path.join("prompts", uploaded_file.name))
        root = tree.getroot()
        if root.tag != "prompt_template":
            raise ValueError("Invalid XML structure: root element should be 'prompt_template'")
    except Exception as e:
        st.sidebar.error(f"Error in uploaded XML: {str(e)}. File removed.")
        os.remove(os.path.join("prompts", uploaded_file.name))
    else:
        st.sidebar.success("XML structure validated successfully!")
        st.experimental_rerun()  # Rerun the app to update the file list

# Get list of XML files
xml_files = glob.glob('prompts/*.xml')

# Sidebar for XML template selection
selected_xml = st.sidebar.selectbox(
    "Choose prompt template",
    xml_files,
    index=xml_files.index('prompts/tm_prompt.xml') if 'prompts/tm_prompt.xml' in xml_files else 0
)

# Function to get XML file info
def get_xml_info(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    intro = root.find('intro')
    intro_text = intro.text.strip() if intro is not None else "No introduction available."
    rules_count = len(root.findall('.//rule'))
    return intro_text, rules_count

# Create Prompter instance and get XML info
st.session_state.prompter = Prompter(selected_xml)
intro_text, rules_count = get_xml_info(selected_xml)


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
st.sidebar.info(f"""
    This app generates AI prompts based on the structure defined in {os.path.basename(selected_xml)}.

    **Current XML template:** {selected_xml}
    **Number of rules:** {rules_count}

    **Template intro:** {intro_text[:100]}...""")

# Add a footer
st.markdown("---")
st.markdown("Developed with ❤️ using Streamlit")
