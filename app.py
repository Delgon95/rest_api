import pymongo
from flask import Flask, request, g

from models import User, Login, Ship, Cargo, Product, Cruise
from utils import get_request_data, json_response
from db import list_all, delete_one_response, \
        find_one_response, find_one, delete_many

BASE_URL = 'localhost'
HOST = '127.0.0.1:5000'

app = Flask(__name__)
client = pymongo.MongoClient()
db = client.ship_transport

@app.before_request
def before_request():
    if request.method == 'PUT':
        if not request.form and not request.data:
            return json_response({"Error": "Missing request body"}, 400)

    if request.method == 'PUT' and not request.headers.get('If-Match'):
        return json_response({"Error": "Missing If-Match header"}, 428)

    if request.endpoint == 'token' and request.method == 'POST':
        return

    if 'u' == request.endpoint[0] and (request.method == 'POST' or request.method == 'PUT'):
        return

    token_id = request.headers.get('Login-Token')
    token = find_one(db.tokens, token_id)
    g.token = token
    if token is None:
        return json_response({"Error": "Could not find session. Not authorized"}, 401)

##########
# Token
##########

@app.route('/token', methods=['POST'])
def user_login():
    login_data = Login(**get_request_data(request))

    if not login_data.validate():
        return json_response({"Error": "Missing login or password"}, 400)

    return login_data.login_response(db.users, db.tokens)

##########
# User
##########

@app.route('/users', methods=['POST'])
def users():
    if request.method == 'POST':
        user_data = User()
        return user_data.create(db.users)

@app.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def user(user_id):
    if request.method == 'PUT':
        user_data = User(**get_request_data(request))
        user_data.edit_token = request.headers.get('If-Match')
        if not user_data.validate():
            return json_response({"Error": "User form is invalid"}, 400)

        return user_data.update(db.users, user_id)
    elif request.method == 'GET':
        return find_one_response(db.users, user_id)
    else:
        return delete_one_response(db.users, user_id)

##########
# Ship
##########

@app.route('/ships', methods=['POST', 'GET'])
def ships():
    if request.method == 'POST':
        ship_data = Ship()
        return user_data.create(db.ships)
    return list_all(db.ships, arguments=request.args)

@app.route('/ships/<ships_id>', methods=['GET', 'PUT', 'DELETE'])
def ship(ship_id):
    if request.method == 'PUT':
        ship_data = Ship(**get_request_data(request))
        ship_data.edit_token = request.headers.get('If-Match')
        if not ship_data.validate():
            return json_response({"Error": "Ship form is invalid"}, 400)

        return ship_data.update(db.ships, ship_id)
    elif request.method == 'GET':
        return find_one_response(db.ships, ship_id)
    else:
        return delete_one_response(db.ships, ship_id)

##########
# Cargo
##########

@app.route('/cargos', methods=['POST', 'GET'])
def cargos():
    if request.method == 'POST':
        cargo_data = Cargo()
        return cargo_data.create(db.cargos)
    return list_all(db.cargos, arguments=request.args)

@app.route('/cargos/<cargo_id>', methods=['GET', 'PUT', 'DELETE'])
def cargo(cargo_id):
    if request.method == 'PUT':
        cargo_data = Cargo(**get_request_data(request))
        cargo_data.edit_token = request.headers.get('If-Match')
        if not cargo_data.validate():
            return json_response({"Error": "Cargo form is invalid"}, 400)

        return cargo_data.update(db.cargos, cargo_id)
    elif request.method == 'GET':
        return find_one_response(db.cargos, cargo_id)
    else:
        return delete_one_response(db.cargos, cargo_id)

##########
# Product
##########

@app.route('/cargos/<cargo_id>/products', methods=['POST', 'GET'])
def products(cargo_id):
    cargo = find_one(db.cargos, cargo_id);
    if cargo is None:
        return json_response({"Error": "Cargo not found"}, 404)

    if request.method == 'POST':
        product_data = Product()
        product.cargo_id = cargo_id
        return product_data.create(db.products)
    return list_all(db.products, filtrs={"cargo_id": cargo_id}, arguments=request.args)

@app.route('/cargos/<cargo_id>/products/<product_id>', methods=['GET', 'PUT', 'DELETE'])
def product(cargo_id, product_id):
    cargo = find_one(db.cargos, cargo_id);
    if cargo is None:
        return json_response({"Error": "Cargo not found"}, 404)

    if request.method == 'PUT':
        product_data = Product(**get_request_data(request))
        product_data.edit_token = request.headers.get('If-Match')
        product_data.cargo_id = cargo_id
        if not cargo_data.validate():
            return json_response({"Error": "Cargo form is invalid"}, 400)

        return product_data.update(db.products, product_id)
    elif request.method == 'GET':
        return find_one_response(db.products, product_id)
    else:
        return delete_one_response(db.products, product_id)


##########
# Cruise
##########
