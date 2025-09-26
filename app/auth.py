import json
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from .forms import LoginForm, SignUpForm
import os
from .cart import load_carts
from .checkouts import orders

main = Blueprint('main', __name__, url_prefix='/auth')
USER_DB = os.path.join(os.path.dirname(__file__), 'users.json')

def load_users():
    if not os.path.exists(USER_DB):
        return {}
    with open(USER_DB, 'r') as f:
        return json.load(f)

@main.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('products.listing_products'))
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        users = load_users()
        username = form.username.data
        password = form.password.data
        email = form.email.data
        if username in users and users[username]['password'] == password and users[username]['email'] == email:
            flash('Login successful!', 'success')
            session['username'] = username
            return redirect(url_for('products.listing_products'))
        else:
            flash('Invalid field. Maybe you need to register', 'danger')

    return render_template('login.html', form=form)

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        users = load_users()
        username = form.username.data
        password = form.password.data
        email = form.email.data
        id = len(users)

        if username in users:
            flash('Username already exists. Please choose a new one!', 'danger')
            return redirect(url_for('main.signup'))  # fixed here
        
        users[username] = {'password': password, 'email': email, 'userid': id}
        with open(USER_DB, 'w') as f:
            json.dump(users, f)
        flash('Account created successfully! Now you need to login.', 'success')
        return redirect(url_for('main.login'))
    else:
        if request.method == 'POST':
            flash('Please correct the errors in the form. Make a stronger password and complete a real email', 'danger')

    return render_template('signup.html', form=form)



@main.route('/logout')
def logout():
    session.pop('username', None)
    flash("You've been logged out.", "info")
    return redirect(url_for('main.login'))

def compute_order_stats(user_orders):
    total_spent = 0
    total_products = 0
    orders_stats = []

    for order in user_orders:
        order_total_price = 0
        order_total_quantity = 0
        items = order.get("items", [])
        for item in items:
            price = item.get("price", 0)
            quantity = item.get("quantity", 0)
            order_total_price += price * quantity
            order_total_quantity += quantity
        
        orders_stats.append({
            "order_id": order.get("order_id"),
            "total_price": order_total_price,
            "total_quantity": order_total_quantity,
            "timestamp": order.get("timestamp")
        })

        total_spent += order_total_price
        total_products += order_total_quantity

    overall_stats = {
        "total_spent": total_spent,
        "total_products": total_products,
        "average_price_per_product": (total_spent / total_products) if total_products else 0,
        "orders_stats": orders_stats
    }

    return overall_stats


@main.route('/profile')
def profile():
    username = session.get('username')
    if not username:
        flash("Please login first.", "warning")
        return redirect(url_for('main.login'))

    orders_dir = "./submitted-orders"
    user_orders = []

    if os.path.exists(orders_dir):
        for filename in os.listdir(orders_dir):
            if filename.endswith(".json"):
                with open(os.path.join(orders_dir, filename), 'r') as f:
                    order = json.load(f)
                    if order.get("username") == username:
                        order['order_id'] = filename.split(".")[0]

                        for item in order.get("items", []):
                            item['item_total'] = item.get('price', 0) * item.get('quantity', 0)

                        user_orders.append(order)

    user_orders.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

    stats = compute_order_stats(user_orders)
    stats['total_orders'] = len(user_orders)
    stats['total_revenue'] = stats['total_spent']

    order_labels = [o['timestamp'] for o in stats['orders_stats']]
    order_total_prices = [o['total_price'] for o in stats['orders_stats']]
    order_total_quantities = [o['total_quantity'] for o in stats['orders_stats']]

    return render_template(
        'profile.html',
        username=username,
        orders=user_orders,
        stats=stats,
        order_labels=order_labels,
        order_total_prices=order_total_prices,
        order_total_quantities=order_total_quantities
    )
