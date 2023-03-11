from flask import request
import requests
from chat_server import flow, db, app
from chat_server.models import User, Message
from pip._vendor import cachecontrol
import google.auth.transport.requests
from google.oauth2 import id_token
import os
from dotenv import load_dotenv
from sqlalchemy import func, desc, asc, extract, and_, distinct

load_dotenv()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_user_oauth():
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    user_oauth = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=os.getenv("OAUTH_CLIENT_ID")
    )
    return user_oauth


def create_user(fullname, email, avatar):
    user = User(fullname=fullname, email=email, avatar=avatar)
    db.session.add(user)
    db.session.commit()
    return user


def get_list_user_by_text(text):
    filter_list = User.query.filter(User.fullname.contains(text) | User.email.__eq__(text))
    user_list = []
    for f in filter_list:
        obj = {
            'fullname': f.fullname,
            'avatar': f.avatar,
            'id': f.id
        }
        user_list.append(obj)
    return user_list


def get_list_receiver(u_id):
    q = db.session.query(Message.content, Message.is_seen, User.id, User.fullname, User.avatar) \
        .join(User, User.id.__eq__(Message.sender)).filter(Message.receiver.__eq__(u_id))\
        .order_by(desc(Message.created_at))
    user_list = []

    return q.all()


if __name__ == '__main__':
    with app.app_context():
        print(get_list_receiver(18))
