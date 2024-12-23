from flask import Blueprint, request, jsonify
from models.image import Image
from config import Config
import logging
from PIL import Image as PILImage
from io import BytesIO
import base64
from imaginairy import imagine, ImaginePrompt, LazyLoadingImage
import os

image_routes = Blueprint('image_routes', __name__)
logger = logging.getLogger(__name__)

# Ensure output directory exists
OUTPUT_DIR = 'generated_images'
os.makedirs(OUTPUT_DIR, exist_ok=True)

@image_routes.route('/', methods=['POST'])
def generate_image():
    try:
        data = request.json
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        logger.debug(f"Generating image for prompt: {prompt}")
        
        # Generate image using imaginAIry
        prompt_obj = ImaginePrompt(
            prompt=prompt,
            width=512,
            height=512,
            seed=None,  # Random seed
            steps=50,
            upscale=False
        )
        
        # Generate the image
        generated_images = list(imagine(prompt_obj))
        
        if not generated_images:
            return jsonify({'error': 'Failed to generate image'}), 500
            
        # Get the first generated image
        img = generated_images[0]
        
        # Convert to base64
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
