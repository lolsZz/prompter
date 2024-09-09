import streamlit as st
import os
from prompter import Prompter
from litellm import completion
import xml.etree.ElementTree as ET
import glob
import json

# Set page config
st.set_page_config(page_title="AI Prompter Pro", page_icon="🧠", layout="wide")


# Custom CSS to improve the look and feel
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .st-emotion-cache-16idsys p {
        font-size: 18px;
    }
    .custom-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Set your API key (consider using st.secrets for better security)
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Function to get list of XML files
def get_xml_files():
    return glob.glob('prompts/*.xml')

# Sidebar for template selection and management
st.sidebar.title("🧠 AI Prompter Pro")
st.sidebar.header("🔧 Configuration")

# Template selection
xml_files = get_xml_files()
selected_xml = st.sidebar.radio(
    "📄 Select a template",
    xml_files,
    index=xml_files.index('prompts/tm_prompt.xml') if 'prompts/tm_prompt.xml' in xml_files else 0,
    format_func=lambda x: os.path.basename(x)
)

# Template management expander
with st.sidebar.expander("🔄 Manage Templates"):
    # File uploader
    uploaded_file = st.file_uploader("📤 Upload new template", type="xml", key="uploader")

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

    if st.button("🗑️ Remove Selected Template"):
        if template_to_remove:
            file_to_remove = os.path.join("prompts", template_to_remove)
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)
                st.success(f"Removed {template_to_remove}")
                st.experimental_rerun()
            else:
                st.error("File not found")

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

# Template preview and download in sidebar
with st.sidebar.expander("👁️ Template Preview"):
    with open(selected_xml, 'r') as file:
        template_content = file.read()
        st.code(template_content, language="xml")

    # Download template
    col1, col2 = st.columns([3, 1])
    with col2:
        template_name = os.path.basename(selected_xml)
        with open(selected_xml, "rb") as file:
            st.download_button(
                label=f"Download {template_name}",
                data=file,
                file_name=template_name,
                mime="application/xml"
            )

# Sidebar for model selection
model = st.sidebar.radio(
    "🤖 Choose an LLM model",
    ("bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0", "gpt-3.5-turbo", "gpt-4"),
    index=0  # Set the default to the first option (Claude 3)
)

# Main content area
st.title("🧠 AI Prompter Pro")

# Display chat history
for i, message in enumerate(st.session_state.chat_history):
    if message['role'] == 'user':
        st.markdown(f"**You:** {message['content']}")
    else:
        with st.chat_message("assistant"):
            st.markdown(f"**AI:** {message['content']}")

# User input area
with st.container():
    st.markdown("### 💬 Chat with AI")
    user_input = st.text_area("Enter your message:", height=100, key="user_input")
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button("🚀 Send", use_container_width=True):
            if user_input:
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                with st.spinner("AI is thinking..."):
                    prompt = st.session_state.prompter.generate_prompt(user_input)
                    ai_response = completion(model=model, messages=[{"role": "user", "content": prompt + user_input}])
                    ai_content = ai_response.choices[0].message.content
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_content})
                st.experimental_rerun()
            else:
                st.warning("Please enter a message.")
    with col2:
        if st.button("🔄 Reset Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.experimental_rerun()
    with col3:
        if st.button("📋 Copy Last Response", use_container_width=True):
            if st.session_state.chat_history:
                last_response = next((msg['content'] for msg in reversed(st.session_state.chat_history) if msg['role'] == 'assistant'), None)
                if last_response:
                    st.write("Last response copied to clipboard!")
                    st.write(last_response)  # This is a placeholder. In a real app, you'd use JavaScript to copy to clipboard.
                else:
                    st.warning("No AI response to copy.")
            else:
                st.warning("No chat history available.")

# Advanced options
with st.expander("🛠️ Advanced Options"):
    st.subheader("Prompt Generation")
    if st.button("Generate Prompt Only"):
        if user_input:
            with st.spinner("Generating prompt..."):
                generated_prompt = st.session_state.prompter.generate_prompt(user_input)
            st.text_area("Generated Prompt:", value=generated_prompt, height=200)
        else:
            st.warning("Please enter a message.")

    st.subheader("Chat Export")
    if st.button("Export Chat History"):
        if st.session_state.chat_history:
            chat_export = json.dumps(st.session_state.chat_history, indent=2)
            st.download_button(
                label="📥 Download Chat History",
                data=chat_export,
                file_name="chat_history.json",
                mime="application/json"
            )
        else:
            st.warning("No chat history to export.")

# Add some information about the app
st.sidebar.markdown("## About")
st.sidebar.info(f"""
    **Current template:** {os.path.basename(selected_xml)}
    **Rules count:** {rules_count}

    This app generates AI prompts based on 
    the structure defined in the selected template.
    """)

# Add a footer
st.sidebar.markdown("---")
st.sidebar.markdown("Developed with ❤️ using Streamlit")
