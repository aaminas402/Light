import json
import os
import asyncio
from generate_panels import generate_panels
from stability_ai import text_to_image
from add_text import add_text_to_panel
from create_strip import create_strip

STYLE = "american comic, colored"

async def main(scenario):
    panels = await generate_panels(scenario)

    # Ensure the output directory exists
    os.makedirs('output', exist_ok=True)

    with open('output/panels.json', 'w') as outfile:
        json.dump(panels, outfile, indent=4)

    panel_images = []

    for panel in panels:
        panel_prompt = panel["description"] + ", cartoon box, " + STYLE
        print(f"Generate panel {panel['number']} with prompt: {panel_prompt}")
        panel_image = text_to_image(panel_prompt)
        panel_image_with_text = add_text_to_panel(panel["text"], panel_image)
        panel_image_with_text.save(f"output/panel-{panel['number']}.png")
        panel_images.append(panel_image_with_text)

    create_strip(panel_images).save("output/strip.png")

if __name__ == "__main__":
    scenario = input("Enter the scenario: ")
    asyncio.run(main(scenario))
