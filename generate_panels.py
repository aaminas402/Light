import re
import openai
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
import asyncio
import json
import requests

load_dotenv()
# Ensure you have set your OpenAI API key in your environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("No OpenAI API key found in environment variables. Please set the OPENAI_API_KEY.")

# Create the client with the API key
openai.api_key = openai_api_key

template = """
You are a cartoon creator who illustrates educational content.
You will be given a chemical reaction, you have to generate a mnemonic story about it. you must split it in 6 parts.
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

async def generate_panels(scenario):
    client = AsyncOpenAI(api_key=openai_api_key)

    prompt = template.format(scenario=scenario)

    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
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
            panel_description = re.search(r'Description:\n(.+)', block, re.DOTALL)
            if panel_description is not None:
                panel_info['description'] = panel_description.group(1).strip()
            
            # Extracting panel text
            panel_text = re.search(r'Text:\n(.+)', block, re.DOTALL)
            if panel_text is not None:
                panel_info['text'] = panel_text.group(1).strip()
            
            panel_info_list.append(panel_info)
    return panel_info_list

async def main():
    scenario = input("Enter the chemical reaction: ")
    panels = await generate_panels(scenario)
    
    # Ensure the output directory exists
    os.makedirs('output', exist_ok=True)
    
    with open('output/panels.json', 'w') as outfile:
        json.dump(panels, outfile, indent=4)
    
    print(panels)

if __name__ == "__main__":
    asyncio.run(main())
