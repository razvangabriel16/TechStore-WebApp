import json
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, abort
import os

products = Blueprint('products', __name__, url_prefix='')
PRODUCTS_DB = os.path.join(os.path.dirname(__file__), 'products.json')

def load_products():
    if not os.path.exists(PRODUCTS_DB):
        return {}
    with open(PRODUCTS_DB, 'r') as f:
        return json.load(f)
    
@products.route('/')
def listing_products():
    if 'username' not in session:
        return redirect(url_for('main.login'))
    pr_list = load_products()
    return render_template('products.html', pr_list=pr_list, title = "Catalogul nostru cu produse")

@products.route('/<int:product_id>')
def product_detail(product_id):
    product_list = load_products()
    product = None
    for i in product_list:
        if i['id'] == product_id:
            product = i
            break
    if product is None:
        abort(404)
    return render_template('product_detail.html', product = product)

@products.route('/discounts')
def product_discounts():
    pr_list = load_products()
    new_pr_list = []
    for p in pr_list:
        if p.get('priceo') is not None and p.get('priceo') != p.get('price'):
            new_pr_list.append(p)
    return render_template('products.html', pr_list=new_pr_list, title="Produse cu discount - Grabeste-te!")
