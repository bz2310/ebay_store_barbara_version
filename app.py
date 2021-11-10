from flask import Flask, Response, request
from flask_cors import CORS
import json
import logging

from application_services.imdb_artists_resource import IMDBArtistResource
from application_services.UsersResource.user_service import UserResource
from database_services.RDBService import RDBService as RDBService

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return '<u>Hello World!</u>'

# this works
@app.route('/users')
def get_users():
    res = UserResource.get_all_user_data()
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp

# ---
# new for product info, but use user info for now

# need a method to get all users/products -> done, above

# need a method for creating a user/product -> PUT/POST
@app.route('/users/<user_no>', methods = ['GET', 'POST', 'DELETE', 'PUT'])
def create_and_get_user(user_no):
    if request.method == 'GET':  # return info for that user
        res = UserResource.get_all_user_data()  # fix this later to get only one user data
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
        return rsp

    if request.method == 'POST':  # create that user
        user_no = request.form.get('user_no')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        print(request.form, flush=True)
        # print(request.data, flush=True)
        # pass these to create_user in user_service.py, as if that's the
        # correct name for a file that creates something named UserResource
        # and ONLY UserResource
        res = UserResource.create_user(user_no, first_name, last_name, email)
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
        return rsp

    if request.method == 'DELETE':
        data = request.form
        res = UserResource.delete_user(data)
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
        return rsp

    if request.method == "PUT":
        data = request.form
        res = UserResource.delete_user(data)
        user_no = request.form.get('user_no')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        res = UserResource.create_user(user_no, first_name, last_name, email)
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
        return rsp



# need a method for updating a user/product -> UPDATE

# need a method for deleting a user/product -> DELETE

# --- old template code below this line ---

# this doesn't work
@app.route('/imdb/artists/<prefix>')
def get_artists_by_prefix(prefix):
    res = IMDBArtistResource.get_by_name_prefix(prefix)
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp



# this probably doesn't work
@app.route('/<db_schema>/<table_name>/<column_name>/<prefix>')
def get_by_prefix(db_schema, table_name, column_name, prefix):
    res = RDBService.get_by_prefix(db_schema, table_name, column_name, prefix)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
