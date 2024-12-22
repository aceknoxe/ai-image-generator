from flask import Blueprint, request, jsonify
import google.generativeai as genai
from models.image import Image
from config import Config
import logging
import requests
from PIL import Image as PILImage
from io import BytesIO
import base64

image_routes = Blueprint('image_routes', __name__)
logger = logging.getLogger(__name__)

# Configure Google AI with safety settings
genai.configure(api_key=Config.GOOGLE_API_KEY)

# Updated Gemini model configuration
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Initialize the model with configurations
model = genai.GenerativeModel(model_name="gemini-pro",
                            generation_config=generation_config,
                            safety_settings=safety_settings)

@image_routes.route('/', methods=['POST'])
def generate_image():
    try:
        data = request.json
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        logger.debug(f"Generating image for prompt: {prompt}")
        
        # For now, let's use a placeholder image service
        image_url = f"https://picsum.photos/512/512"  # Random placeholder image
        
        # Download the image and convert to base64
        response = requests.get(image_url)
        img = PILImage.open(BytesIO(response.content))
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        base64_url = f"data:image/png;base64,{img_str}"

        # Save to database
        image = Image(prompt=prompt, image_url=base64_url)
        image.save()
        
        return jsonify({
            'prompt': prompt,
            'imageUrl': base64_url,
            'createdAt': image.created_at.isoformat()
        }), 201

    except Exception as e:
        logger.error(f"Error in generate_image: {str(e)}")
        return jsonify({'error': str(e)}), 500

@image_routes.route('/', methods=['GET'])
def get_images():
    try:
        images = Image.get_all()
        return jsonify([{
            'prompt': img['prompt'],
            'imageUrl': img['image_url'],
            'createdAt': img['created_at'].isoformat()
        } for img in images])
    except Exception as e:
        logger.error(f"Error in get_images: {str(e)}")
        return jsonify({'error': str(e)}), 500
