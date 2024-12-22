from datetime import datetime
from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGODB_URI)
db = client['ai-image-generator']
images = db.images

class Image:
    def __init__(self, prompt, image_url):
        self.prompt = prompt
        self.image_url = image_url
        self.created_at = datetime.utcnow()

    def save(self):
        return images.insert_one({
            'prompt': self.prompt,
            'image_url': self.image_url,
            'created_at': self.created_at
        })

    @staticmethod
    def get_all(limit=10):
        return list(images.find().sort('created_at', -1).limit(limit))
