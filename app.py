from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, static_folder='frontend/dist', static_url_path='')
CORS(app)

# Database setup
def init_db():
    conn = sqlite3.connect('cache.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS word_cache (
            id INTEGER PRIMARY KEY,
            first_word TEXT,
            second_word TEXT,
            result TEXT,
            emoji TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/craft', methods=['POST'])
def craft_new_word():
    data = request.json
    first_word = data.get('first')
    second_word = data.get('second')

    # Here you would implement the logic to generate a new word
    # For demonstration, we will just return a mock response
    result = f"{first_word}-{second_word}"
    emoji = "✨"  # Mock emoji

    # Cache the result in the database
    conn = sqlite3.connect('cache.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO word_cache (first_word, second_word, result, emoji) VALUES (?, ?, ?, ?)',
                   (first_word, second_word, result, emoji))
    conn.commit()
    conn.close()

    return jsonify({'result': result, 'emoji': emoji})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000) 