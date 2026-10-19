import base64
import io
import os
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image, ImageEnhance, ImageFilter

load_dotenv()

def process_image_edit(input_image: Image.Image, prompt_text: str):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("API Key not found in .env file!")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # Ensure RGB format
    if input_image.mode in ("RGBA", "P"):
        image_to_send = input_image.convert("RGB")
    else:
        image_to_send = input_image

    # Base64 encode for Gemini vision analysis
    buffered = io.BytesIO()
    image_to_send.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Ask Gemini to interpret the edit command and provide a short summary
    response = client.chat.completions.create(
        model="google/gemini-2.5-flash",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": f"You are an AI image editing assistant. Analyze the image and the user's request: '{prompt_text}'. Provide a brief 1-2 sentence confirmation of the edit being applied."
                    },
                    {
                        "type": "image_url", 
                        "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}
                    }
                ]
            }
        ]
    )
    ai_message = response.choices[0].message.content

    # --- APPLIED IMAGE EDITING LOGIC (Simulating AI-driven visual transforms) ---
    prompt_lower = prompt_text.lower()
    edited_image = image_to_send.copy()

    if "black and white" in prompt_lower or "grayscale" in prompt_lower or "b&w" in prompt_lower:
        edited_image = edited_image.convert("L").convert("RGB")
    elif "blur" in prompt_lower:
        edited_image = edited_image.filter(ImageFilter.GaussianBlur(radius=5))
    elif "bright" in prompt_lower:
        enhancer = ImageEnhance.Brightness(edited_image)
        edited_image = enhancer.enhance(1.4)
    elif "contrast" in prompt_lower:
        enhancer = ImageEnhance.Contrast(edited_image)
        edited_image = enhancer.enhance(1.5)
    else:
        # Default subtle enhancement if custom prompt doesn't match predefined filters
        enhancer = ImageEnhance.Color(edited_image)
        edited_image = enhancer.enhance(1.2)

    return edited_image, ai_message