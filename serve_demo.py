from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the demo HTML file"""
    return send_file('demo.html')

@app.route('/demo.html')
def demo():
    """Serve the demo HTML file explicitly"""
    return send_file('demo.html')

if __name__ == '__main__':
    print("Starting Flask server at http://0.0.0.0:5000")
    print("Access the demo at http://0.0.0.0:5000/demo.html or just /")
    app.run(host='0.0.0.0', port=5000, debug=True)