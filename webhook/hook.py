from flask import Flask, request, Response
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from DB.engine import Session
from flask_httpauth import HTTPBasicAuth
from utils.encryption import enc, dec
from DB.tables import AuthUsers

app = Flask(__name__)
auth = HTTPBasicAuth()


@app.route('/crete_user', methods=['POST'])
def create_user():
    date = request.json
    user = date['user']
    password = enc(date['password'])
    try:
        new_auth_user = AuthUsers(username=user, password=password, is_active=False)
        session = Session()
        session.add(new_auth_user)
        res = new_auth_user.username
        session.commit()
    except IntegrityError:
        res = 'duplicate username'
    except Exception as err:
        res = str(err)
    return Response(res, status=200)


@app.route('/sendMessage', methods=['POST'])
@auth.login_required
def return_response():
    """
    curl -X POST -u my_user0:my_password localhost:5000/sendMessage -H 'Content-Type: application/json'
    '{"chat_id": 12343, "text": "Hello World!", "severity": "Critical"}'
    """
    data = request.json
    severity = data['severity']
    text = data['text']
    chat_id = data['chat_id']
    print(severity, text, chat_id)
    return Response('ok', status=200)


@auth.verify_password
def authenticate(username, password):
    if username and password:
        session = Session()
        user = session.query(AuthUsers).filter_by(username=username).first()
        user_pass = dec(user.password)
        if user.is_active and username == str(user) and password == str(user_pass):
            return True
        else:
            return False
    return False

#
# if __name__ == "__main__":
#     app.run()
