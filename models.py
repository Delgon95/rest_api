import datetime
import uuid
import bcrypt
import rfc3339

from bson import ObjectId
from dateutil import parser
from db import create_new_token, find_one, object_save, object_update, list_all
from utils import json_response

##########
# Token
##########

##########
# User
##########

class User:
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id')
        self.login = kwargs.get('login')
        self.password = kwargs.get('password')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.edit_token = kwargs.get('edit_token', str(uuid.uuid4()))
        self.flag_create = kwargs.get('flag_create', False)
        self.token_create = kwargs.get('token_create')

    def get_id(self):
        return self._id

    def validate(self):
        for field in [self.login, self.password, self.first_name, self.last_name]:
            if field is None:
                return False
        return True

    def authenticate(self, collection, password):
        if password != self.password:
            return json_respone({"Error": "Could not find matching password and login"}, 401)

        token = create_new_token(self._id, collection)

        return json_response("", 204, {"Etag": token})

    def create(self, collection):
        return object_save(collection, self, "users")

    def update(self, collection, id_):
        user = find_one(collection, id_, '_id')
        if user is None:
            return json_response({"Error": "User does not exist"}, 404)

        user = User(**user)
        if user.edit_token != self.edit_token:
            return json_response({"Error": "ETag header was invalidated"}, 428)

        self._id = user._id

        return object_update(collection, self)

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}

##########
# Ship
##########

class Ship:
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id')
        self.name = kwargs.get('name')
        self.crew_count = kwargs.get('crew_count')
        self.capacity = kwargs.get('capacity')

        self.edit_token = kwargs.get('edit_token', str(uuid.uuid4()))
        self.flag_create = kwargs.get('flag_create', False)
        self.token_create = kwargs.get('token_create')

    def get_id(self):
        return self._id

    def validate(self):
        for field in [self.name, self.crew_count, self.capacity]:
            if field is None:
                return False
        return True

    def create(self, collection):
        return object_save(collection, self, "ships")

    def update(self, collection, id_):
        ship = find_one(collection, id_, '_id')
        if ship is None:
            return json_response({"Error": "Ship does not exist"}, 404)

        ship = Ship(**ship)
        if ship.edit_token != self.edit_token:
            return json_response({"Error": "ETag header was invalidated"}, 428)

        self._id = ship._id

        return object_update(collection, self)

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}

##########
# Cargo
##########

class Cargo:
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id')
        self.capacity = kwargs.get('capacity')
        self.size = kwargs.get('size')

        self.edit_token = kwargs.get('edit_token', str(uuid.uuid4()))
        self.flag_create = kwargs.get('flag_create', False)
        self.token_create = kwargs.get('token_create')

    def get_id(self):
        return self._id

    def validate(self):
        for field in [self.capacity, self.size]:
            if field is None:
                return False
        return True

    def create(self, collection):
        return object_save(collection, self, "cargos")

    def update(self, collection, id_):
        cargo = find_one(collection, id_, '_id')
        if user is None:
            return json_response({"Error": "Cargo does not exist"}, 404)

        cargo = Cargo(**cargo)
        if cargo.edit_token != self.edit_token:
            return json_response({"Error": "ETag header was invalidated"}, 428)

        self._id = cargo._id

        return object_update(collection, self)

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}

##########
# Product
##########

class Product:
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id')
        self.cargo_id = kwargs('cargo_id')
        self.name = kwargs.get('name')
        self.price = kwargs.get('price')
        self.weight = kwargs.get('weight')
        self.size = kwargs.get('size')

        self.edit_token = kwargs.get('edit_token', str(uuid.uuid4()))
        self.flag_create = kwargs.get('flag_create', False)
        self.token_create = kwargs.get('token_create')

    def get_id(self):
        return self._id

    def validate(self):
        for field in [self.cargo_id, self.name, self.price, self.weight, self.size]:
            if field is None:
                return False
        return True

    def create(self, collection):
        return object_save(collection, self, "cargos")

    def update(self, collection, id_):
        product = find_one(collection, id_, '_id')
        if user is None:
            return json_response({"Error": "Product does not exist"}, 404)

        product = Product(**cargo)
        if product.edit_token != self.edit_token:
            return json_response({"Error": "ETag header was invalidated"}, 428)

        self._id = product._id

        return object_update(collection, self)

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}

##########
# Cruise
##########

class Cruise:
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id')
        self.destination = kwargs.get('destination')
        self.start_location = kwargs.get('start_location')
        self.ship_id = kwargs.get('ship_id')
        self.cargos = kwargs.get('cargos')

        self.edit_token = kwargs.get('edit_token', str(uuid.uuid4()))
        self.flag_create = kwargs.get('flag_create', False)
        self.token_create = kwargs.get('token_create')

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}

##########
# Login
##########

class Login:
    def __init__(self, **kwargs):
        self.login = kwargs.get('login')
        self.password = kwargs.get('password')

    def validate(self):
        if self.login is None or self.password is None:
            return False
        return True

    def login_response(self, users_collection, token_collection):
        user = find_one(users_collection, self.login, 'login')
        if user is None:
            return json_response({"Error": "User do not exist"}, 404)
        user = User(**user)

        return user.authenticate(token_collection, self.password)

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}
