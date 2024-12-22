from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from routes.image_routes import image_routes
from config import Config

app = Flask(__name__)

# Update CORS configuration
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:8000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
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
    app.run(debug=True, port=5000)
