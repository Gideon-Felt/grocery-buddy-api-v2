from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
from environs import Env
import os


app = Flask(__name__)
CORS(app)
heroku = Heroku(app)

env = Env()
env.read_env()
# DATABASE_URL = env("DATABASE_URL")

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
# app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL


db = SQLAlchemy(app)
ma = Marshmallow(app)

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.String(50))
    product_name = db.Column(db.String(500))
    price = db.Column(db.Integer)

    def __init__(self, product_name, store_id, price):
        self.store_id = store_id
        self.product_name = product_name
        self.price = price

# class Product(db.Model):
#     __tablename__ = "products"
#     id = db.Column(db.Integer, primary_key=True)
#     store = db.Column(db.Integer, db.ForeignKey('stores.id'))
#     product_name = db.Column(db.String())
#     price = db.Column(db.Integer())

#     def __init__(self, store, product_name, price):
#         self.store = store
#         self.product_name = product_name
#         self.price = price

#     def json_products(self):
#         data = {
#             "store": self.store,
#             "product_name": self.product_name,
#             "price": self.price
#         }

#         return jsonify(data)

class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "store_id", "product_name", "price")

# class ProductSchema(ma.Schema):
#     class Meta:
#         fields = ("id", "store", "product_name", "price")

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# product_schema = ProductSchema()
# products_schema = ProductSchema(many=True)

@app.route("/")
def greeting():

    return "<h1>Grocery Buddy API</h1>"

# POST
@app.route("/add-product", methods=["POST"])
def add_product():
    store_id = request.json["store_id"]
    product_name = request.json["product_name"]
    price = request.json["price"]
    
    new_product = Product(store_id, product_name, price)
    
    db.session.add(new_product)
    db.session.commit()

    return jsonify("product POSTED")

# GET
@app.route("/products", methods=["GET"])
def get_products():

    all_products = Product.query.all()
    result = products_schema.dump(all_products)

    return jsonify(result)

# GET BY ID
@app.route("/product/<id>", methods=["GET"])
def get_product(id):

    product = Product.query.get(id)

    return product_schema.jsonify(product)

# PUT
# @app.route("/store/<id>", methods=["PUT"])
# def update_store(id):
#     store = Store.query.get(id)
#     new_products = request.json["products"]
#     new_address = request.json["address"]
#     new_city = request.json["city"]
#     new_state = request.json["state"]
#     new_zip_code = request.json["zip_code"]

#     store.products = new_products
#     store.address = new_address
#     store.city = new_city
#     store.state = new_state
#     store.zip_code = new_zip_code

#     db.session.commit()

#     return store_schema.jsonify(store)

# PATCH
@app.route("/product/<id>", methods=["PATCH"])
def update_product(id):
    product = Product.query.get(id)
    new_products = request.json["products"]

    db.session.commit()

    return product_schema.jsonify(product)

# DELETE
@app.route("/delete-product/<id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)

    db.session.delete(product)

    db.session.commit()

    return jsonify("Product DELETED")

# POST
# @app.route("/add-product", methods=["POST"])
# def add_product():
#     store = request.json["store"]
#     product_name = request.json["product_name"]
#     price = request.json["price"]
    
#     new_product = Product(store, product_name, price)

#     db.session.add(new_product)
#     db.session.commit()

#     return jsonify("product POSTED")


if __name__ == "__main__":
    app.debug = True
    app.run()