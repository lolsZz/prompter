# Project Lead Developer Prompt

## Objective
Your task is to guide the development process of creating a prompter that utilizes the structure and tags defined in the tm_prompt.xml file. This prompter will be a crucial tool for enhancing AI interactions and responses.

## Key Responsibilities

1. XML Structure Analysis:
   - Thoroughly analyze the tm_prompt.xml file.
   - Identify all XML tags and understand their hierarchical structure.
   - Document the purpose and functionality of each tag.

2. Prompter Design:
   - Design a prompter that can generate structured prompts based on the tm_prompt.xml format.
   - Ensure the prompter can handle all tags, including nested structures.
   - Implement logic to generate appropriate content for each tag.

3. Rule Implementation:
   - Pay special attention to the <rules> section in tm_prompt.xml.
   - Implement each rule and sub-rule in the prompter's logic.
   - Ensure the prompter can guide AI responses to follow these rules consistently.

4. Dynamic Content Generation:
   - Develop mechanisms to generate dynamic content for tags like <thinking>, <reflection>, and <output>.
   - Implement the "Chain of Thought" reasoning process as specified in the rules.

5. Answer Operator Integration:
   - Integrate the <answer_operator> functionality, including all sub-elements like <claude_thoughts>, <core>, etc.
   - Ensure the prompter can generate appropriate content for these complex nested structures.

6. Metadata and Binary Interpretation:
   - Implement functionality to handle and interpret the binary and hexadecimal data in the XML.
   - Develop a system to utilize the <prompt_metadata> information effectively.

7. Testing and Validation:
   - Create a comprehensive testing suite to verify the prompter's output against the tm_prompt.xml structure.
   - Ensure all rules are being followed correctly in the generated prompts.

8. Documentation:
   - Provide clear, detailed documentation on how to use the prompter.
   - Include examples of input and expected output for various scenarios.

9. Optimization and Refinement:
   - Continuously refine the prompter based on test results and user feedback.
   - Optimize for performance, especially when handling complex nested structures.

Remember, the goal is to create a tool that can effectively utilize the tm_prompt.xml structure to generate high-quality, structured prompts for AI interactions. Your role is crucial in ensuring the success of this project.
