import xml.etree.ElementTree as ET
import re

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
        prompt += self._generate_answer_operator(user_input)
        prompt += self._generate_reflection()
        prompt += self._generate_output()
        return prompt

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

    def _generate_answer_operator(self, user_input):
        # This is a placeholder. We'll implement the complex logic later.
        return "<answer_operator>\n[Answer operation details here]\n</answer_operator>\n\n"

    def _generate_reflection(self):
        return "<reflection>\n[Reflection on the reasoning and potential errors]\n</reflection>\n\n"

    def _generate_output(self):
        return "<output>\n[Final concise answer here]\n</output>\n"

if __name__ == "__main__":
    prompter = Prompter('tm_prompt.xml')
    user_input = input("Enter your query: ")
    generated_prompt = prompter.generate_prompt(user_input)
    print(generated_prompt)
