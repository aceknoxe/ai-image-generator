from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from routes.image_routes import image_routes
from config import Config
import os

app = Flask(__name__)

# Update CORS configuration
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],  # Allow all origins for now, update with your frontend URL later
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
    # Get port from environment variable (Render sets this automatically)
    port = int(os.environ.get("PORT", 5000))
    # Important: bind to 0.0.0.0 to listen on all interfaces
    app.run(host='0.0.0.0', port=port)
