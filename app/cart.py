import json
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
import os
#from .auth import load_users

cart = Blueprint('cart', __name__, url_prefix='/cart')
USER_DB = os.path.join(os.path.dirname(__file__), 'users.json')
CART_DB = os.path.join(os.path.dirname(__file__), 'carts.json')
PRODUCTS_DB = os.path.join(os.path.dirname(__file__), 'products.json')

def load_users():
    if not os.path.exists(USER_DB):
        return {}
    with open(USER_DB, 'r') as f:
        return json.load(f)

def get_session_cart():
    if 'cart' not in session:
        session['cart'] = {}
    return session['cart']

def save_session_cart(cart_data):
    session['cart'] = cart_data
    session.modified = True

def load_carts():
    if not os.path.exists(CART_DB):
        with open(CART_DB, 'w') as f:
            json.dump({}, f)
        return {}
    with open(CART_DB, 'r') as f:
        return json.load(f)

def save_carts(carts_data):
    with open(CART_DB, 'w') as f:
        json.dump(carts_data, f)

def load_products():
    if not os.path.exists(PRODUCTS_DB):
        return {}
    with open(PRODUCTS_DB, 'r') as f:
        return json.load(f)

def get_product_by_id(product_id):
    products = load_products()
    for product in products:
        if product['id'] == product_id:
            return product
    return None

def get_user_cart(username):
    if username:
        users = load_users()
        carts = load_carts()
        
        if username in users:
            user_id = str(users[username].get('userid'))
            if user_id not in carts:
                carts[user_id] = {}
                save_carts(carts)
            return carts[user_id]
    
    return get_session_cart()

def save_user_cart(username, cart_data):
    if username:
        users = load_users()
        if username in users:
            carts = load_carts()
            user_id = str(users[username].get('userid'))
            carts[user_id] = cart_data
            save_carts(carts)
    else:
        save_session_cart(cart_data)

def calculate_total(cart_items):
    total = 0
    products = load_products()
    
    for product_id, quantity in cart_items.items():
        product = get_product_by_id(int(product_id))
        if product:
            total += product['price'] * quantity
    
    return total

@cart.route('/')
def index():
    username = session.get('username')
    user_cart = get_user_cart(username)
    
    cart_items = []
    total_price = 0
    
    for product_id, quantity in user_cart.items():
        product = get_product_by_id(int(product_id))
        if product:
            item_total = product['price'] * quantity
            total_price += item_total
            cart_items.append({
                'id': product_id,
                'name': product['name'],
                'price': product['price'],
                'quantity': quantity,
                'item_total': item_total
            })
    
    return render_template('cart.html', 
                          username=username, 
                          cart_items=cart_items, 
                          total_price=total_price)
@cart.route('/add-item/')
def add_item():
    products = load_products()
    product_id = request.args.get('id')
    if not product_id:
        flash('Product ID is required', 'danger')
        return redirect(url_for('products.listing_products'))
    
    product = get_product_by_id(int(product_id))
    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('products.listing_products'))
    
    username = session.get('username')
    user_cart = get_user_cart(username)
    
    if product['stock'] <= 0:
        flash(f'Sorry, {product["name"]} is out of stock', 'danger')
        return redirect(url_for('products.listing_products'))

    if product_id in user_cart:
        user_cart[product_id] += 1
    else:
        user_cart[product_id] = 1

    product['stock'] -= 1

    for i, p in enumerate(products):
        if p['id'] == product['id']:
            products[i] = product
            break
    
    with open(PRODUCTS_DB, 'w') as f:
        json.dump(products, f, indent=2)
    
    save_user_cart(username, user_cart)
    flash(f'{product["name"]} added to your cart', 'success')
    
    return redirect(url_for('cart.index'))


@cart.route('/remove-item')
def remove_item():
    product_id = request.args.get('id')
    if not product_id:
        flash('Product ID is required', 'danger')
        return redirect(url_for('cart.index'))
    
    username = session.get('username')
    user_cart = get_user_cart(username)
    
    if product_id in user_cart:
        del user_cart[product_id]
        save_user_cart(username, user_cart)
        flash('Item removed from cart', 'success')
    
    return redirect(url_for('cart.index'))

@cart.route('/update-quantity')
def update_quantity():
    product_id = request.args.get('id')
    quantity = request.args.get('quantity', type=int)
    
    if not product_id or quantity is None:
        flash('Product ID and quantity are required', 'danger')
        return redirect(url_for('cart.index'))
    
    if quantity <= 0:
        return redirect(url_for('cart.remove_item', id=product_id))
    
    username = session.get('username')
    user_cart = get_user_cart(username)
    
    if product_id in user_cart:
        user_cart[product_id] = quantity
        save_user_cart(username, user_cart)
        flash('Cart updated', 'success')
    
    return redirect(url_for('cart.index'))

