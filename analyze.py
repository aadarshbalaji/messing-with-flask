from dotenv import load_dotenv
from pprint import pprint
import requests
import os
from groq import Groq
import re

# Load environment variables
API_KEY = os.getenv("API_KEY")

def get_answer(question='two sum'):
    """
    This function sends the user's question to the Groq model and retrieves the response.
    """
    client = Groq(api_key=API_KEY)
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": '''You are a coding assistant focused on solving LeetCode problems using Python. Your responses must:
1. Provide a clear, optimal solution with all necessary imports and type hints.
2. Include a detailed explanation that covers:
    - Problem intuition
    - Time and space complexity
    - Edge cases and constraints
3. Structure your response as follows:
    - Start with "LeetCode Problem #{number}" if applicable, or "Custom Solution" otherwise.
    - Provide code in proper Python formatting, like this:
        ```python
        [Your solution]
        ```
    - Follow the code with a detailed explanation that includes:
        - Explanation of the logic
        - Time and space complexity analysis
        - Edge cases and constraints to consider

Please ensure the response is well-organized for easy readability and understanding.'''
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0,
        max_tokens=6000,
        top_p=1,
        stream=True,
        stop=None,
    )

    full_response = ""
    
    # Concatenate all chunks into the full response
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content

    return full_response

def parse_llm_response(response):
    """
    Parse the LLM response to extract LeetCode problem number, code, and explanation.
    """
    leetcode_number = None
    code = ""
    explanation = ""

    # Try to find the LeetCode problem number
    number_match = re.search(r'(?i)leetcode\s*#?\s*(\d+)', response)
    if number_match:
        leetcode_number = number_match.group(1)

    # Extract the code (between triple backticks)
    code_match = re.search(r'```python(.*?)```', response, re.DOTALL)
    if code_match:
        code = code_match.group(1).strip()

    # Extract the explanation (after code block)
    explanation_match = re.split(r'```', response)
    if len(explanation_match) > 2:
        explanation = explanation_match[-1].strip()

    return leetcode_number, code, explanation

if __name__ == "__main__":
    print('\n*** Welcome to the LeetCode Chatbot! ***\n')
    question = input('Please enter a question: ')
    response = get_answer(question)
    print('\nResponse from model:\n')
    pprint(response)

    # Parse the model response
    leetcode_number, code, explanation = parse_llm_response(response)
    print(f"\nLeetCode Problem Number: {leetcode_number}")
    print(f"\nCode:\n{code}")
    print(f"\nExplanation:\n{explanation}")
