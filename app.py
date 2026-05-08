from flask import Flask, render_template, jsonify, request
import random
import unicodedata
from phrases import PHRASES, ACCEPTED_ANSWERS, VALID_COUNTRIES

app = Flask(__name__)

def normalize(text):
    """Normalize text: lowercase, remove accents, strip spaces."""
    text = text.lower().strip()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/phrase')
def get_phrase():
    phrase = random.choice(PHRASES)
    return jsonify({
        "phrase": phrase["phrase"],
        "language": phrase["language"],
        "country": phrase["country"],
        "catalan_translation": phrase["catalan_translation"],
        "flag": phrase["flag"],
        "hint": phrase["hint"],
    })

@app.route('/api/check', methods=['POST'])
def check_answer():
    data = request.json
    user_answer = normalize(data.get('answer', ''))
    correct_country = data.get('country', '')

    # Check if it's a valid country name
    if user_answer not in VALID_COUNTRIES:
        return jsonify({"valid": False})

    correct_normalized = normalize(correct_country)
    accepted = ACCEPTED_ANSWERS.get(correct_country, [])
    accepted_normalized = [normalize(a) for a in accepted]

    is_correct = (
        user_answer == correct_normalized or
        user_answer in accepted_normalized
    )

    return jsonify({
        "valid": True,
        "correct": is_correct,
        "correct_country": correct_country,
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
