from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan_image():
    try:
        data = request.json
        url = data.get('url')
        
        if not url:
            return jsonify({"text": "", "error": "Geen URL meegeleverd"})
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            return jsonify({"text": "", "error": f"HTTP error {response.status_code}"})
            
        img = Image.open(BytesIO(response.content))
        
        # We halen de tekst op via Tesseract
        text = pytesseract.image_to_string(img)
        
        # Belangrijk: We sturen de tekst netjes terug in de JSON
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"text": "", "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
