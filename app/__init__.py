from flask import Flask
from .auth import main as main_blueprint
from .cart import cart as cart_blueprint
from .products import products as products_blueprint
from .checkouts import checkouts as checkout_blueprint

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('../configure.py')

    app.register_blueprint(main_blueprint)
    app.register_blueprint(cart_blueprint)
    #app.register_blueprint(categories)
    app.register_blueprint(products_blueprint)
    app.register_blueprint(checkout_blueprint)
    return app
