from flask import Flask, request, redirect, render_template, jsonify
import string
import random
import sqlite3

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls
                 (short_code TEXT PRIMARY KEY, original_url TEXT)''')
    conn.commit()
    conn.close()

def generate_short_code(length=6):
    """Generate a unique short code for URL"""
    characters = string.ascii_letters + string.digits
    while True:
        short_code = ''.join(random.choice(characters) for _ in range(length))
        
        # Check if code already exists
        conn = sqlite3.connect('urls.db')
        c = conn.cursor()
        c.execute('SELECT * FROM urls WHERE short_code = ?', (short_code,))
        if not c.fetchone():
            return short_code

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form.get('url')
        if not original_url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Validate URL (basic check)
        if not original_url.startswith(('http://', 'https://')):
            original_url = 'http://' + original_url
        
        # Generate short code and store
        conn = sqlite3.connect('urls.db')
        c = conn.cursor()
        short_code = generate_short_code()
        c.execute('INSERT INTO urls VALUES (?, ?)', (short_code, original_url))
        conn.commit()
        conn.close()
        
        # Return full short URL
        short_url = request.host_url + short_code
        return render_template('index.html', short_url=short_url)
    
    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_url(short_code):
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('SELECT original_url FROM urls WHERE short_code = ?', (short_code,))
    result = c.fetchone()
    conn.close()
    
    if result:
        return redirect(result[0])
    else:
        return jsonify({'error': 'URL not found'}), 404

# Initialize DB on startup
init_db()

if __name__ == '__main__':
    app.run(debug=True)
