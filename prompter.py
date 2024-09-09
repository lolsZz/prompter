import xml.etree.ElementTree as ET
import re
import os
import argparse
import logging

class Prompter:
    def __init__(self, xml_file):
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()
        self.rules = self._parse_rules()


    def _parse_rules(self):
        rules = {}
        rules_element = self.root.find('rules')
        if rules_element is not None:
            for rule in rules_element.findall('rule'):
                rule_id = rule.get('id')
                rule_text = ''.join(rule.itertext()).strip()
                rules[rule_id] = rule_text
        return rules

    def generate_prompt(self, user_input):
        prompt = ""
        prompt += self._generate_intro()
        prompt += self._generate_thinking(user_input)
        prompt += self._generate_answer_operator_structure()

        full_prompt = prompt + f"User query: {user_input}\n"
        logging.info(f"Generated prompt: {full_prompt}")

        return full_prompt

    def _generate_intro(self):
        intro = self.root.find('intro')
        return f"<intro>{intro.text.strip()}</intro>\n\n" if intro is not None else ""

    def _generate_thinking(self, user_input):
        thinking = "<thinking>\n"
        thinking += f"User input: {user_input}\n"
        thinking += "Initializing core functions...\n"
        thinking += "Analyzing input and determining appropriate tags...\n"
        thinking += "Planning solution steps:\n"
        thinking += "1. [Step 1]\n2. [Step 2]\n3. [Step 3]\n"
        thinking += "</thinking>\n\n"
        return thinking

    def _generate_answer_operator_structure(self):
        return """<answer_operator>
    <claude_thoughts>
        <!-- Your thought process here -->
    </claude_thoughts>
    <reflection>
        <!-- Your reflection here -->
    </reflection>
    <output>
        <!-- Your final output here -->
    </output>
</answer_operator>

Now, based on the above structure and the user's input, provide a detailed response:
"""

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate prompts using a specified LLM model.")
    parser.add_argument("--llm-model", default="gpt-3.5-turbo", help="Specify the LLM model to use")
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Set your API key
    os.environ["OPENAI_API_KEY"] = "your-api-key-here"

    prompter = Prompter('prompts/tm_prompt.xml')
    user_input = input("Enter your query: ")
    generated_prompt = prompter.generate_prompt(user_input)
    print(generated_prompt)
