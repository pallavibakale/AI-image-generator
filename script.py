import gradio as gr
import openai
import requests
import os
from PIL import Image
from io import BytesIO

#API key delte krtoy ithun, tu use krshil 
openai.api_key = "openai_api_key_placeholder"

if not openai.api_key:
    raise ValueError("Missing OpenAI API Key. Set it as an environment variable: OPENAI_API_KEY")

client = openai.OpenAI(api_key=openai.api_key)  

def generate_image(prompt, num_images):
    """Generates multiple images from a text prompt using OpenAI's DALL-E API."""
    try:
        response = client.images.generate(
            model="dall-e-3",  
            prompt=prompt,
            n=num_images,
            size="1024x1024"
        )
        
        images = []
        for i in range(num_images):
            image_url = response.data[i].url
            image_response = requests.get(image_url)
            img = Image.open(BytesIO(image_response.content))
            images.append(img)
        
        return images
    except Exception as e:
        return [f"Error: {str(e)}"]

iface = gr.Interface(
    fn=generate_image,
    inputs=[
        gr.Textbox(label="Enter your text prompt", placeholder="Describe the image you want"),
        gr.Slider(minimum=1, maximum=5, step=1, label="Number of images")
    ],
    outputs=gr.Gallery(label="Generated Images"),
    title="AI-Powered Design Generator",
    description="Enter a text prompt to generate AI-powered designs."
)

iface.launch(share=True)
