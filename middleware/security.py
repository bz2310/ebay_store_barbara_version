from middleware.context import email_keygen
import requests

security_paths = ['/signup']

def check_security(request, google, app):
    path = request.path
    result_ok = False

    if path in security_paths:

        if google.authorized:
            s = app.blueprints.get("google").session
            t = s.token
            result_ok = t
    else:
        result_ok = True

    return result_ok

def check_email(email):
    apiKey = email_keygen()  # our api key is called via an other file to ensure security
    response = requests.get(
        "https://emailvalidation.abstractapi.com/v1/?api_key=" + apiKey + "&email=" + email)

    print("Email verification result = \n", "Status Code:", response.status_code, "\n", "Content:", response.content.decode('utf-8'))
    email_good = (response.json()['deliverability'] == 'DELIVERABLE')
    return email_good