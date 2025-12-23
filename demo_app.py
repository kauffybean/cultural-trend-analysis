from flask import Flask, send_file, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the demo HTML file"""
    return send_file('demo.html')

@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('static', path)

if __name__ == '__main__':
    print("Starting Demo Flask server at http://0.0.0.0:8080")
    print("Access the demo at http://0.0.0.0:8080/")
    # Use a different port (8080) to avoid conflicts with the main app
    app.run(host='0.0.0.0', port=8080, debug=True)