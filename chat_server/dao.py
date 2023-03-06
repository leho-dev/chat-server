from flask import request
import requests
from chat_server import flow, db
from chat_server.models import User
from pip._vendor import cachecontrol
import google.auth.transport.requests
from google.oauth2 import id_token
import os
from dotenv import load_dotenv

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
