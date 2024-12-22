from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

def test_connection():
    try:
        uri = os.getenv('MONGODB_URI')
        print(f"Attempting to connect to MongoDB...")
        
        client = MongoClient(uri)
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
        
        # Get the database and collection
        db = client['ai-image-generator']
        images = db.images
        
        # Add a test image
        test_image = {
            "prompt": "Test image",
            "image_url": "https://picsum.photos/200",
            "created_at": datetime.utcnow()
        }
        
        # Insert the test image
        result = images.insert_one(test_image)
        print(f"Inserted test image with ID: {result.inserted_id}")
        
        # Retrieve all images
        all_images = list(images.find())
        print("\nAll images in database:")
        for img in all_images:
            print(f"Image: {img}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_connection()