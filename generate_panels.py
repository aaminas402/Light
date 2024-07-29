import re
import openai
import os
from openai import AsyncOpenAI

# Ensure you have set your OpenAI API key in your environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')
print("OPENAI_API_KEY:", os.getenv('OPENAI_API_KEY'))
template = """
You are a cartoon creator who illustrates educational content.
You will be given a chemical reaction,you have to generate a mnemonic story about it. you must split it in 6 parts.
Each part will be a different cartoon panel.
For each cartoon panel, you will write a description of it with:
 - the characters in the panel, they must be described precisely each time
 - the background of the panel
The description should be only word or group of word delimited by a comma, no sentence.
Always use the characters descriptions instead of their name in the cartoon panel description.
You can not use the same description twice.
You will also write the text of the panel.
The text should not be more than 2 small sentences.
Each sentence should start by the character name

Example input:
Chemical Reaction: Combustion of Methane

Example output:

# Panel 1
Description:
Characters- methane molecule with a smiley face, oxygen molecules with superhero capes
Background- sunny meadow, flowers, blue sky

Text:
Methane: "Hi, I'm Methane!"
Oxygen: "And we're the Oxygen twins!"
# end

Short Scenario:
{scenario}

Split the scenario in 6 parts:
"""


def generate_panels():
    scenario = input("Enter the chemical reaction: ")
    client = AsyncOpenAI()

    prompt = template.format(scenario=scenario)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    result = response.choices[0].message["content"].strip()
    print(result)

    return extract_panel_info(result)

def extract_panel_info(text):
    panel_info_list = []
    panel_blocks = text.split('# Panel')

    for block in panel_blocks:
        if block.strip() != '':
            panel_info = {}
            
            # Extracting panel number
            panel_number = re.search(r'\d+', block)
            if panel_number is not None:
                panel_info['number'] = panel_number.group()
            
            # Extracting panel description
            panel_description = re.search(r'description: (.+)', block)
            if panel_description is not None:
                panel_info['description'] = panel_description.group(1)
            
            # Extracting panel text
            panel_text = re.search(r'text:\n```\n(.+)\n```', block, re.DOTALL)
            if panel_text is not None:
                panel_info['text'] = panel_text.group(1)
            
            panel_info_list.append(panel_info)
    return panel_info_list

if __name__ == "__main__":
    panels = generate_panels()
    print(panels)
