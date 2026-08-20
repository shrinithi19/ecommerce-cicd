from flask import Flask, render_template, g, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-this'  # needed for sessions
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

@app.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    cart = session.get('cart', {})
    product_id = str(product_id)
    cart[product_id] = cart.get(product_id, 0) + 1
    session['cart'] = cart
    return redirect(request.referrer or url_for('home'))

@app.route('/cart/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        del cart[product_id]
    session['cart'] = cart
    return redirect(url_for('view_cart'))

@app.route('/cart/update/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    cart = session.get('cart', {})
    product_id = str(product_id)
    quantity = int(request.form.get('quantity', 1))
    if quantity <= 0:
        cart.pop(product_id, None)
    else:
        cart[product_id] = quantity
    session['cart'] = cart
    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    db = get_db()
    items = []
    total = 0
    for product_id, quantity in cart.items():
        product = db.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
        if product:
            subtotal = product['price'] * quantity
            total += subtotal
            items.append({
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'image': product['image'],
                'quantity': quantity,
                'subtotal': subtotal
            })
    return render_template("cart.html", items=items, total=total)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
