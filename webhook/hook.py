from flask import Flask, request, Response
import requests

import config
from sqlalchemy.exc import IntegrityError
from DB.engine import Session
from flask_httpauth import HTTPBasicAuth
from utils.encryption import enc, dec
from utils.db_func import get_pri_errors, get_chat_ids
from DB.tables import AuthUsers, User

app = Flask(__name__)
auth = HTTPBasicAuth()


def get_users(pri):
    session = Session()
    users_chatid = get_chat_ids(get_pri_errors(session, pri))
    return users_chatid


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
    '{"text": "Hello World!", "severity": "Critical"}'
    """
    try:
        data = request.json
        severity = data['severity']
        if 'flat' in data:
            if data['flat'].lower() == 'ture':
                text = request.data
        else:
            text = request.data
            # st = text['alerts'][0]['status']
            # desc = text['alerts'][0]['annotations']['description']
            # target = text['commonLabels']['instance']
            # host = text['commonLabels']['host']
            # txt = str('status: {}\n{}'.format(st, desc))
    except Exception as err:
        text = request.data
        severity = 'info'

    ids = get_users(severity)
    print(ids)
    for chat_id in ids:
        data = dict(chat_id=chat_id, text=text)
        requests.post('%sbot%s/sendMessage' % (config.base_url, config.token), data=data)
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
