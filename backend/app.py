import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from routes.image_routes import image_routes
from config import Config

app = Flask(__name__)

# Update CORS configuration for production
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-frontend-domain.com", "http://localhost:8000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Register blueprints
app.register_blueprint(image_routes, url_prefix='/api/images')

# Test route
@app.route('/test')
def test():
    return jsonify({"message": "Backend is working!"})

# Serve frontend files
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
