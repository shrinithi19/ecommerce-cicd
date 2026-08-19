from flask import Flask, render_template

app = Flask(__name__)

# Sample products
products = [
    {"id": 1, "name": "i phone", "price": "$49.99", "image": "https://via.placeholder.com/150"},
    {"id": 2, "name": "Smart Watch", "price": "$79.99", "image": "https://via.placeholder.com/150"},
    {"id": 3, "name": "Gaming Mouse", "price": "$29.99", "image": "https://via.placeholder.com/150"},
]

@app.route('/')
def home():
    return render_template("index.html", products=products)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
