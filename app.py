from __future__ import print_function

from flask import Flask, Response, request, render_template, redirect, url_for
from flask_cors import CORS
from flask_dance.contrib.google import make_google_blueprint, google
import json
import logging

from application_services.UsersResource.user_service import UserResource
from database_services.RDBService import RDBService as RDBService

from front_end.forms import SearchForm,SignupForm
from werkzeug.datastructures import ImmutableMultiDict
import pandas as pd
from middleware.notifications import publish_note
from middleware.security import check_security, check_email
from middleware.context import google_auth_keygen

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__, template_folder='front_end')
app.debug = True
app.secret_key = 'blah'

import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
client_id, client_secret = google_auth_keygen()
blueprint = make_google_blueprint(client_id=client_id, client_secret=client_secret, scope=['profile','email'])

app.register_blueprint(blueprint, url_prefix='/login')

CORS(app)

@app.route("/login/google/authorized/", methods=['GET'])
def login():
    return redirect(url_for('\signup'))

@app.before_request
def security_before_request():
    security_status = check_security(request, google, app)
    if not security_status:
        return redirect(url_for('google.login'))

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        request.method = 'GET'
        newform = request.form
        newdict = {}
        for k,v in newform.items():
            if 'submit' not in k and len(v) > 0:
                newdict[k] = v
        res = UserResource.get_all_user_data()
        print(res)
        print(newdict)
        request.form = ImmutableMultiDict(newdict)
        res = create_and_get_user()
        return json_to_html(res, 'Search results for users')

    form = SearchForm()
    return render_template('index.html', form=form)

def print_dict(my_dict):
    mystr = ""
    for k,v in my_dict.items():
        mystr += "%s: %s, "%(k,v)
    return mystr

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    bp = app.blueprints.get('google')
    s = bp.session
    t = s.token

    action_lookup = {'Sign up':'POST', 'Delete':'DELETE'}
    method_lookup = {'POST':'create', 'DELETE':'delete'}
    if request.method == 'POST':
        newform = request.form
        newdict = {}
        for k,v in newform.items():
            if 'action' in k:
                request.method = action_lookup[v]
                print("Signup page new request action: %s" % request.method)
                continue
            if ('submit' not in k) and (len(v) > 0):
                newdict[k] = v
        res = UserResource.get_all_user_data()
        newdict['user_no'] = str(pd.DataFrame(res).dropna().user_no.astype(int).max() + 1)

        if not check_email(newdict['email']):
            return json_to_html({}, title='Could not %s user, email not valid' % method)

        publish_note("New user created with characteristics %s"%print_dict(newdict))

        request.form = ImmutableMultiDict(newdict)
        method = method_lookup[request.method]
        res = create_and_get_user()

        request.method='GET'
        res = create_and_get_user()
        return json_to_html(res, title='Successfully %sd user'%method)

    form = SignupForm()
    return render_template('signup.html', google_auth_token=t, form=form)

def json_to_html(json_result, title):
    json_result = json_result.data
    json_result = pd.DataFrame(json.loads(json_result)).dropna().to_html(index=False)
    return render_template('table.html', table=json_result, title=title)

@app.route('/api/users', methods = ['GET', 'POST', 'DELETE', 'PUT'])
def create_and_get_user():
    print("Request method in create_and_get_user: %s"%request.method)
    if request.method == 'GET':  # return info for that user
        data = request.form.to_dict()
        if len(data) == 0:
            res = UserResource.get_all_user_data()
        else:
            res = UserResource.get_select_user_data(data)

        print(res)
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
        return rsp

    elif request.method == 'POST':  # create that user
        data = request.args.to_dict()
        res = UserResource.create_user(data)
        rsp = Response(json.dumps(res), status=201, content_type="application/json")
        return rsp

    elif request.method == 'DELETE':
        data = request.args.to_dict()
        res = UserResource.delete_user(data)
        rsp = Response(json.dumps(res), status=204, content_type="application/json")
        return rsp

    elif request.method == "PUT":
        data = request.args.to_dict()
        res = UserResource.delete_user(data)
        res = UserResource.create_user(data)
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
        return rsp

# need a method for updating a user/product -> UPDATE

# need a method for deleting a user/product -> DELETE

# --- old template code below this line ---


# this probably doesn't work
@app.route('/<db_schema>/<table_name>/<column_name>/<prefix>')
def get_by_prefix(db_schema, table_name, column_name, prefix):
    res = RDBService.get_by_prefix(db_schema, table_name, column_name, prefix)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
