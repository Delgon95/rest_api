import secrets
import uuid
import datetime

from bson import ObjectId
from bson.errors import InvalidId
from utils import json_response

class LoginToken:
    def __init__(self, **kwargs):
        self._id = kwargs.get('_id')
        self.user_id = kwargs.get('user_id')
    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}

def create_new_token(user_id, collection):
    #token = LoginToken(**dict([("user_id", user_id), ("login_date", str(datetime.datetime.now()))]))
    token = LoginToken()
    token.user_id = user_id
    token_id = str(collection.save(token.to_dict()))
    return token_id

def object_save(collection, object_data, location=""):
    headers = {}
    found = collection.find_one({"flag_create": False,
                                 "token_create": object_data.token_create})
    if found is not None:
        headers['Location'] = "/" + location + "/" + str(found.get('_id'))  # f"/{location}/{key}"
        headers['ETag'] = found.get('edit_token')
        return json_response("", 201, headers)

    key = str(collection.save(object_data.to_dict()))
    headers['Location'] = "/" + location + "/" + str(key)  # f"/{location}/{key}"
    headers['ETag'] = object_data.edit_token
    return json_response("", 201, headers);

def object_update(collection, modified_object_data):
    headers = {}
    modified_object_data.flag_create = True
    modified_object_data.edit_token = str(uuid.uuid4())
    key = str(collection.save(modified_object_data.to_dict()))
    status = 204
    headers['ETag'] = modified_object_data.edit_token
    return json_response("", status, headers);

def find_one(collection, object_id, filter_key='_id'):
    if filter_key == '_id':
        key = ObjectId(object_id)
    else:
        key = object_id
    try:
        return collection.find_one({filter_key: key})
    except InvalidId:
        return None

def find_one_response(collection, object_id, filter_key='_id'):
    data = find_one(collection, object_id, filter_key)
    headers = {}

    if data is None:
        return json_response({"Error": "Could not find entry"}, 404)
    data['_id'] = str(data['_id'])
    if 'edit_token' in data:
        headers['ETag'] = data['edit_token']
        data.pop('edit_token')

#    for k, v in data.items():
#        if isinstance(v, bytes):
#            data[k] = v.decode('utf-8')
#        if 'hash' in k:
#            data[k] = "***"

    return json_response(data, 200, headers)

def list_all(collection, filters=None, arguments=None):
    if filters is None:
        filters = {}
    filters["flag_create"] = True

    page = 0
    if arguments.get('page') is not None:
        page = int(arguments.get('page'))
    items = 15
    if arguments.get('items') is not None:
        items = int(arguments.get('items'))
    for argument in arguments:
        if argument not in ['page', 'items']:
            filters[argument] = arguments[argument]

    count = collection.find(filters).count()
    data = collection.find(filters).skip(page * items).limit(items)

    entries = [x for x in data]
    for x in entries:
        x['_id'] = str(x['_id'])
        if 'edit_token' in x:
            x.pop('edit_token')
    headers = {"All-Entries-Count": count, "Current-Entries-Count": entries}
    return json_response({"entries": entries}, 200, headers)

def delete_one_response(collection, object_id,  filter_key='_id'):
    if find_one(collection, object_id, filter_key) is None:
        return json_response({"Error": "Could not find entry"}, 404)

    if filter_key == '_id':
        key = ObjectId(object_id)
    else:
        key = object_id

    collection.delete_one({filter_key: key})
    return json_response("", 204)

def delete_many(collection, filters):
    collection.delete_many(filters)
    return json_response("", 204)

