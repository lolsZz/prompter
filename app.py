import streamlit as st
import os
from prompter import Prompter
import warnings
from litellm import completion
import xml.etree.ElementTree as ET
import os
import glob
import shutil
import tempfile
import base64

# Set page config
st.set_page_config(page_title="AI Prompter", page_icon="🤖", layout="wide")

# Set your API key (consider using st.secrets for better security)
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Function to get list of XML files
def get_xml_files():
    return glob.glob('prompts/*.xml')

# Sidebar for template selection and management
st.sidebar.header("Prompt Template")

# Template selection
xml_files = get_xml_files()
selected_xml = st.sidebar.selectbox(
    "Select a template",
    xml_files,
    index=xml_files.index('prompts/tm_prompt.xml') if 'prompts/tm_prompt.xml' in xml_files else 0,
    format_func=lambda x: os.path.basename(x)
)

# Template management expander
with st.sidebar.expander("Manage Templates"):
    # File uploader
    uploaded_file = st.file_uploader("Upload new template", type="xml", key="uploader")

    if uploaded_file:
        # Save the uploaded file to the prompts folder
        with open(os.path.join("prompts", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Uploaded {uploaded_file.name} successfully!")

        # Validate the uploaded XML
        try:
            tree = ET.parse(os.path.join("prompts", uploaded_file.name))
            root = tree.getroot()
            if root.tag != "tm_prompt":
                raise ValueError("Invalid XML structure: root element should be 'tm_prompt'")
        except Exception as e:
            st.error(f"Error in uploaded XML: {str(e)}. File removed.")
            os.remove(os.path.join("prompts", uploaded_file.name))
        else:
            st.success("XML structure validated successfully!")
            st.experimental_rerun()

    # Template removal
    template_to_remove = st.selectbox(
        "Select template to remove",
        [""] + [os.path.basename(f) for f in xml_files],
        key="remove_template"
    )

    if st.button("Remove Selected Template"):
        if template_to_remove:
            file_to_remove = os.path.join("prompts", template_to_remove)
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)
                st.success(f"Removed {template_to_remove}")
                st.experimental_rerun()
            else:
                st.error("File not found")

# Template preview and download
with st.sidebar.expander("Template Preview"):
    with open(selected_xml, 'r') as file:
        template_content = file.read()
        st.code(template_content, language="xml")

    # Download template
    with open(selected_xml, "rb") as file:
        st.download_button(
            label="Download Template",
            data=file,
            file_name=os.path.basename(selected_xml),
            mime="application/xml"
        )

# Function to get XML file info
def get_xml_info(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    intro = root.find('intro')
    intro_text = intro.text.strip() if intro is not None and intro.text else "No introduction available."
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
            ai_response = completion(model=model, messages=[{"role": "user", "content": prompt + user_input}])
            st.text_area("AI Response:", value=ai_response.choices[0].message.content, height=300)
    else:
        st.warning("Please enter a query.")

# Add some information about the app
st.sidebar.markdown("## About")
st.sidebar.info(f"""
    **Current template:** {os.path.basename(selected_xml)}
    **Rules count:** {rules_count}

    This app generates AI prompts based on 
    the structure defined in the selected template.
    """)

# Add a footer
st.markdown("---")
st.markdown("Developed with ❤️ using Streamlit")
