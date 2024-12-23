import os
from datetime import datetime
from PIL import Image
import google.generativeai as genai
import io

# Configure API
os.environ['GOOGLE_API_KEY'] = 'AIzaSyAGwxJZzFUWhYkczhTKfDgBXZjJxhmSl68'
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

def generate_image(prompt):
    try:
        # Create model with imagen-3.0-generate-001
        model = genai.GenerativeModel('imagen-3.0-generate-001')
        
        # Generate image with correct content format
        response = model.generate_content({
            "parts": [{
                "text": prompt,
                "inline_data": {
                    "mime_type": "image/png",
                    "parameters": {
                        "size": "1024x1024",
                        "samples": 1,
                        "steps": 50,
                        "cfg_scale": 7.5
                    }
                }
            }]
        })
        
        # Create directory for saving
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_dir = os.path.join('generated_images', timestamp)
        os.makedirs(save_dir, exist_ok=True)
        
        # Save and display image
        if hasattr(response, 'image'):
            image_path = os.path.join(save_dir, 'generated_image.png')
            response.image.save(image_path)
            Image.open(image_path).show()
            print(f"Image saved to: {image_path}")
            return image_path
        else:
            print("No image in response")
            return None
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# Test the function
result = generate_image("A photorealistic cute puppy in a garden")