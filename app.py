from flask import Flask, render_template, g
import sqlite3
import os

app = Flask(__name__)
DATABASE = os.path.join(os.path.dirname(__file__), 'store.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            image TEXT NOT NULL
        )
    ''')
    # Seed only if table is empty
    existing = db.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    if existing == 0:
        db.executemany(
            'INSERT INTO products (name, price, image) VALUES (?, ?, ?)',
            [
                ("i phone", 49.99, "https://via.placeholder.com/150"),
                ("Smart Watch", 79.99, "https://via.placeholder.com/150"),
                ("Gaming Mouse", 29.99, "https://via.placeholder.com/150"),
            ]
        )
        db.commit()
    db.close()

@app.route('/')
def home():
    db = get_db()
    products = db.execute('SELECT * FROM products').fetchall()
    return render_template("index.html", products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    db = get_db()
    product = db.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    return render_template("product.html", product=product)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
