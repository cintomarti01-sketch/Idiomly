from flask import Flask, render_template, jsonify, request
import random
import unicodedata
from phrases import PHRASES, ACCEPTED_ANSWERS, VALID_COUNTRIES

app = Flask(__name__)

# URL base per als contorns de països (mapsicon via GitHub)
OUTLINE_BASE_URL = "https://raw.githubusercontent.com/djaiss/mapsicon/master/all/{iso_code}/512.png"

# Ordre i configuració de les pistes progressives
HINT_SEQUENCE = [
    {
        "type": "population",
        "label": "Població",
        "icon": "👥",
    },
    {
        "type": "outline",
        "label": "Contorn del país",
        "icon": "🗺️",
    },
    {
        "type": "continent",
        "label": "Continent",
        "icon": "🌍",
    },
    {
        "type": "flag",
        "label": "Bandera",
        "icon": "🚩",
    },
]


def normalize(text):
    """Normalize text: lowercase, remove accents, strip spaces."""
    text = text.lower().strip()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return text


def build_hints(phrase):
    """Build all four progressive hints for a phrase."""
    return [
        {
            "type": "population",
            "label": "Població",
            "icon": "👥",
            "value": phrase["population"],
        },
        {
            "type": "outline",
            "label": "Contorn del país",
            "icon": "🗺️",
            "value": OUTLINE_BASE_URL.format(iso_code=phrase["iso_code"]),
        },
        {
            "type": "continent",
            "label": "Continent",
            "icon": "🌍",
            "value": phrase["continent"],
        },
        {
            "type": "flag",
            "label": "Bandera",
            "icon": "🚩",
            "value": f"https://flagcdn.com/w160/{phrase['iso_code']}.png",
        },
    ]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/phrase')
def get_phrase():
    phrase = random.choice(PHRASES)
    hints = build_hints(phrase)
    return jsonify({
        "phrase": phrase["phrase"],
        "language": phrase["language"],
        "country": phrase["country"],
        "catalan_translation": phrase["catalan_translation"],
        "flag": phrase["flag"],
        "hint": phrase["hint"],
        "hints": hints,  # Les 4 pistes progressives
    })


@app.route('/api/check', methods=['POST'])
def check_answer():
    data = request.json
    user_answer = normalize(data.get('answer', ''))
    correct_country_name = data.get('country', '')
    attempt = data.get('attempt', 0)

    if user_answer not in VALID_COUNTRIES:
        return jsonify({"valid": False})

    # Busquem l'objecte de la frase actual per saber l'idioma correcte
    current_phrase = next((p for p in PHRASES if p["country"] == correct_country_name), None)
    
    is_correct = False
    guessed_language = False

    # 1. Comprovem si és el país correcte
    accepted = ACCEPTED_ANSWERS.get(correct_country_name, [])
    accepted_normalized = [normalize(a) for a in accepted]
    if user_answer == normalize(correct_country_name) or user_answer in accepted_normalized:
        is_correct = True

    # 2. Si no és el país, comprovem si l'idioma coincideix
    if not is_correct and current_phrase:
        user_country_official_name = None
        for country, aliases in ACCEPTED_ANSWERS.items():
            if user_answer == normalize(country) or user_answer in [normalize(a) for a in aliases]:
                user_country_official_name = country
                break
        
        if user_country_official_name:
            # Agafem l'idioma base (ex: "Castellà") ignorant el que hi hagi entre parèntesis
            def get_base_lang(lang_string):
                return lang_string.split('(')[0].strip()

            target_lang = get_base_lang(current_phrase["language"])
            
            # Busquem si algun exemple del país de l'usuari usa aquest mateix idioma base
            for p in PHRASES:
                if p["country"] == user_country_official_name:
                    if get_base_lang(p["language"]) == target_lang:
                        guessed_language = True
                        break

    return jsonify({
        "valid": True,
        "correct": is_correct,
        "guessed_language": guessed_language, # Nova clau
        "correct_country": correct_country_name,
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)