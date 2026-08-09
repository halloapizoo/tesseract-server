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

        # Download de afbeelding
        response = requests.get(url, timeout=10)
        img = Image.open(BytesIO(response.content))

        # Laat Tesseract de tekst lezen
        text = pytesseract.image_to_string(img)

        return jsonify({"text": text, "logo": ""})
    except Exception as e:
        return jsonify({"text": "", "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
