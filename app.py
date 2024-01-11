from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def detect_pii(text):
    # Basic PII detection using regular expressions
    pii_patterns = {
        'name': r'\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b',
        'aadhaar': r'\b(\d{12})\b',
        'passport': r'\b([A-Z]{3}\d{9})\b',
        'mobile': r'\b(\d{10})\b',
    }

    pii_detected = []

    for pii_type, pattern in pii_patterns.items():
        matches = re.findall(pattern, text)
        for match in matches:
            pii_detected.append({'pii_type': pii_type.capitalize(), 'pii_value': match})

    return pii_detected

@app.route('/analyze', methods=['POST'])
def analyze_text():
    try:
        data = request.get_json()
        if 'body' not in data:
            raise ValueError("Missing 'body' in the request")

        text = data['body']
        pii_detected = detect_pii(text)

        response = {'pii_detected': pii_detected, 'error': None}
        return jsonify(response)

    except Exception as e:
        response = {'pii_detected': [], 'error': str(e)}
        return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)