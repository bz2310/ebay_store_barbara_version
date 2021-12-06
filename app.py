from __future__ import print_function

from flask import Flask, Response, request, render_template, redirect, url_for
from flask_s3 import FlaskS3
from flask_cors import CORS
from flask_dance.contrib.google import make_google_blueprint, google
import json
import logging
import numpy as np

from application_services.UsersResource.user_service import UserResource
from application_services.ProductsResource import ProductResource

from static.forms import AdminForm,SignupForm,ProductForm
from werkzeug.datastructures import ImmutableMultiDict
import pandas as pd
from middleware.notifications import publish_note
from middleware.security import check_security, check_email
from middleware.context import google_auth_keygen

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__, template_folder='static')
app.config['FLASKS3_BUCKET_NAME'] = 'charitystore'
app.config['AWS_ACCESS_KEY_ID'] = 'AKIAT5PRHNCLBWVMMBRD'
app.config['AWS_SECRET_ACCESS_KEY'] = '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'
app.debug = True
app.secret_key = 'SqIoUWyqYETxs8IPQkRjvSWrDqn/2VSFXzVGRoHW'

import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
client_id, client_secret = google_auth_keygen()
blueprint = make_google_blueprint(client_id=client_id, client_secret=client_secret, scope=['profile','email'])

app.register_blueprint(blueprint, url_prefix='/login')

CORS(app)

s3 = FlaskS3()
def start_app():
    app = Flask(__name__)
    s3.init_app(app)
    return app

@app.route("/login/google/authorized/", methods=['GET'])
def login():
    return redirect(url_for('/signup'))

@app.before_request
def security_before_request():
    security_status = check_security(request, google, app)
    if not security_status:
        return redirect(url_for('google.login'))

@app.route("/", methods=['GET'])
@app.route("/<int:page>", methods=['GET'])
def index(page=1):
    print('page: %s'%page)
    perpage = 3
    products = ProductResource.get_all_product_data()
    max_page = np.ceil(len(products) / perpage)
    print("max page: %s"%max_page)
    print(products)
    paginated_products = products[(page-1)*(perpage):((perpage)*(page))]
    print(paginated_products)
    return render_template('index.html', products = paginated_products, page=page, max_page = max_page)

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    bp = app.blueprints.get('google')
    s = bp.session
    t = s.token

    if request.method == 'POST':

        newform = request.form
        newdict = {}

        for k,v in newform.items():
            if 'submit' not in k and len(v) > 0:
                newdict[k] = v

        ## create a new user number
        res = UserResource.get_all_user_data()
        newdict['user_no'] = str(pd.DataFrame(res).dropna().user_no.astype(int).max() + 1)
        ## check validity of new email
        if not check_email(newdict['email']):
            return json_to_html(None, title='Could not create user, email not valid')

        request.form = ImmutableMultiDict(newdict)
        res = create_and_get_user()
        return json_to_html(res, 'Created following user:')

    form = SignupForm()
    return render_template('signup.html', form=form)

def print_dict(my_dict):
    mystr = ""
    for k,v in my_dict.items():
        mystr += "%s: %s, "%(k,v)
    return mystr


@app.route('/admin_accounts', methods=['GET', 'POST'])
def admin_accounts():

    bp = app.blueprints.get('google')
    s = bp.session
    t = s.token

    action_lookup = {'Sign up':'POST', 'Delete':'DELETE', 'Search':'GET'}
    method_lookup = {'POST':'Created', 'DELETE':'Deleted', 'GET':'Searched for'}

    ## All submissions are POSTs, we need to change it to the
    ## needed action for the create_and_get_user function
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

        ## If desired action is actually a POST, aka creating a user
        ## Then create a new user number and check the email validity
        if request.method == 'POST':
            ## create a new user number
            res = UserResource.get_all_user_data()
            newdict['user_no'] = str(pd.DataFrame(res).dropna().user_no.astype(int).max() + 1)
            ## check validity of new email
            if not check_email(newdict['email']):
                return json_to_html(None, title='Could not create user, email not valid')

        request.form = ImmutableMultiDict(newdict)
        method = method_lookup[request.method]
        res = create_and_get_user()
        if res.status_code > 400:
            return json_to_html(None, title='%s not successful'%method)
        return json_to_html(res, title='%s following user(s):'%method)

    form = AdminForm()
    return render_template('admin_accounts.html', google_auth_token = t, form=form)

@app.route('/admin_products', methods=['GET', 'POST'])
def admin_products():

    bp = app.blueprints.get('google')
    s = bp.session
    t = s.token

    action_lookup = {'Create':'POST', 'Delete':'DELETE', 'Search':'GET'}
    method_lookup = {'POST':'Created', 'DELETE':'Deleted', 'GET':'Searched for'}

    ## All submissions are POSTs, we need to change it to the
    ## needed action for the create_and_get_user function
    if request.method == 'POST':
        newform = request.form
        newdict = {}
        for k,v in newform.items():
            if 'action' in k:
                request.method = action_lookup[v]
                print("Admin products page new request action: %s" % request.method)
                continue
            if ('submit' not in k) and (len(v) > 0):
                newdict[k] = v

        ## If desired action is actually a POST, aka creating a user
        ## Then create a new user number and check the email validity

        if request.method == 'POST':
            ## create a new product number
            res = ProductResource.get_all_product_data()
            newdict['product_no'] = str(pd.DataFrame(res).dropna().product_no.astype(int).max() + 1)

        request.form = ImmutableMultiDict(newdict)
        method = method_lookup[request.method]
        res = create_and_get_product()

        if res.status_code > 400:
            return json_to_html(None, title='%s not successful'%method)
        return json_to_html(res, title='%s following product(s):'%method)

    form = ProductForm()
    return render_template('admin_products.html', google_auth_token = t, form=form)

def json_to_html(json_result, title):
    if not json_result:
        json_result = "<p>No data</p>"
    else:
        json_result = json_result.data
        json_result = pd.DataFrame(json.loads(json_result)).dropna().to_html(index=False)

    return render_template('table.html', table=json_result, title=title)

@app.route('/api/users/<user_no>', methods = ['GET', 'POST', 'DELETE', 'PUT'])
@app.route('/api/users', methods = ['GET', 'DELETE'])
def create_and_get_user(user_no=None):
    print("Request method in create_and_get_user: %s"%request.method)

    if request.method == 'GET':  # return info for that user

        print(user_no)
        data = request.form.to_dict()

        if user_no:
            res = UserResource.get_select_user_data({'user_no':user_no})
        elif len(data) == 0:
            res = UserResource.get_all_user_data()
        else:
            res = UserResource.get_select_user_data(data)

        print(res)
        if len(res) == 0:
            rsp = Response('User not found', status=404, content_type='application/json')
        else:
            rsp = Response(json.dumps(res), status=200, content_type="application/json")
        return rsp

    elif request.method == 'POST':  # create that user
        data = request.form.to_dict()
        res = UserResource.create_user(data)
        if len(res) == 0:
            rsp = Response("User not created successfully", status=400, content_type='application/json')
        else:
            rsp = Response(json.dumps(res), status=201, content_type="application/json")
            ## send SNS notification for new user
            publish_note("New user created with characteristics %s" % print_dict(data))
        return rsp

    elif request.method == 'DELETE':
        data = request.form.to_dict()
        res = UserResource.delete_user(data)
        rsp = Response(json.dumps(res), status=204, content_type="application/json")
        ## send SNS notification for deleting user
        publish_note("Deleted user with characteristics %s" % print_dict(data))
        return rsp

    elif request.method == "PUT":
        data = request.form.to_dict()
        res = UserResource.delete_user(data)
        res = UserResource.create_user(data)
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
        return rsp

@app.route('/api/products/<product_no>', methods = ['GET', 'POST', 'DELETE', 'PUT'])
@app.route('/api/products', methods = ['GET', 'DELETE'])
def create_and_get_product(product_no=None):
    print("Request method in create_and_get_product: %s"%request.method)

    if request.method == 'GET':  # return info for that product

        print(product_no)
        data = request.form.to_dict()

        if product_no:
            res = ProductResource.get_select_product_data({'product_no':product_no})
        elif len(data) == 0:
            res = ProductResource.get_all_product_data()
        else:
            res = ProductResource.get_select_product_data(data)

        print(res)
        if len(res) == 0:
            rsp = Response('Product not found', status=404, content_type='application/json')
        else:
            rsp = Response(json.dumps(res), status=200, content_type="application/json")
        return rsp

    elif request.method == 'POST':  # create that product
        data = request.form.to_dict()
        res = ProductResource.create_product(data)
        if len(res) == 0:
            rsp = Response("Product not created successfully", status=400, content_type='application/json')
        else:
            rsp = Response(json.dumps(res), status=201, content_type="application/json")
            ## send SNS notification for new product
            publish_note("New product created with characteristics %s" % print_dict(data))

        return rsp

    elif request.method == 'DELETE':
        data = request.form.to_dict()

        res = ProductResource.delete_product(data)
        rsp = Response(json.dumps(res), status=204, content_type="application/json")

        ## send SNS notification for deleting user
        publish_note("Deleted product with characteristics %s" % print_dict(data))

        return rsp

    elif request.method == "PUT":
        data = request.form.to_dict()
        res = ProductResource.delete_product(data)
        res = ProductResource.create_product(data)
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
        return rsp

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
