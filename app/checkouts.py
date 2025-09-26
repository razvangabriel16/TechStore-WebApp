import json
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, abort
import os
from datetime import datetime
import pytz
from .cart import get_user_cart,  save_user_cart, load_products, get_product_by_id
checkouts = Blueprint('checkouts', __name__, url_prefix='/checkout')

def get_next_order_number():
    counter_file = "./submitted-data/order_counter.txt"
    os.makedirs(os.path.dirname(counter_file), exist_ok=True)
    if not os.path.exists(counter_file):
        with open(counter_file, "w") as f:
            f.write("1")
        return 1
    with open(counter_file, "r+") as f:
        current_number = int(f.read())
        next_number = current_number + 1
        f.seek(0)
        f.write(str(next_number))
        f.truncate()
        return next_number

from datetime import datetime

@checkouts.route('/', methods=['GET', 'POST'])
def checkout():
    if 'username' not in session:
        flash("Trebuie să fii autentificat pentru a plasa o comandă.", "warning")
        return redirect(url_for('main.login'))

    username = session.get('username')
    user_cart = get_user_cart(username)

    if not user_cart or len(user_cart) == 0:
        flash("Cosul tau este gol, adauga produse inainte de a face comanda.", "warning")
        return redirect(url_for('cart.index'))

    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        payment_method = request.form['payment_method']
        products = load_products()
        items = []
        for product_id, quantity in user_cart.items():
            product = get_product_by_id(int(product_id))
            if product:
                items.append({
                    "product_id": int(product_id),
                    "name": product['name'],
                    "price": product['price'],
                    "quantity": quantity
                })

        order_data = {
            "username": username,
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "address": address,
            "payment_method": payment_method,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": items
        }

        order_number_id = get_next_order_number()
        filename = f"./submitted-orders/{order_number_id}.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(order_data, f, indent=4)

        save_user_cart(username, {})

        save_user_cart(username, {})
        session['cart'] = {}
        session.modified = True

        flash(f"Comanda #{order_number_id} a fost plasată cu succes!", "success")
        return redirect(url_for('checkouts.orders'))

    return render_template('checkout.html', cart=user_cart)


@checkouts.route('/orders')
def orders():
    if 'username' not in session:
        flash("Trebuie să fii autentificat pentru a vedea comenzile tale.", "warning")
        return redirect(url_for('main.login'))

    username = session.get('username')
    orders_dir = "./submitted-orders"
    user_orders = []

    if os.path.exists(orders_dir):
        for filename in os.listdir(orders_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(orders_dir, filename)
                with open(filepath, 'r') as f:
                    order = json.load(f)
                    if order.get("username") == username:
                        ts = order.get("timestamp")
                        if ts:
                            try:
                                dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                                dt = pytz.utc.localize(dt)
                                bucharest_time = dt.astimezone(pytz.timezone("Europe/Bucharest"))
                                order["timestamp_local"] = bucharest_time.strftime("%Y-%m-%d %H:%M:%S")
                            except Exception as e:
                                order["timestamp_local"] = ts
                        else:
                            order["timestamp_local"] = "N/A"

                        order['order_id'] = filename.split(".")[0]
                        user_orders.append(order)
    user_orders.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

    return render_template('orders.html', orders=user_orders, username=username)
