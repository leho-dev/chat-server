from flask import request
import requests
from chat_server import flow, db, app
from chat_server.models import User, Message, Conversation
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


def get_user_by_id_json(u_id):
    user = User.query.filter(User.id.__eq__(u_id)).first()
    obj = {
        'fullname': user.fullname,
        'avatar': user.avatar,
        'id': user.id
    }
    return obj


def get_last_mess_in_conv(c_id):
    last_mess = Message.query.filter(Message.conversation_id.__eq__(c_id)).order_by(desc(Message.created_at)).first()
    if last_mess:
        return last_mess.content
    return ""


def get_list_receiver(u_id):
    query_user = Conversation.query.filter(Conversation.user_1.__eq__(u_id) | Conversation.user_2.__eq__(u_id))

    user_list = []
    for q in query_user:
        obj = {}
        if q.user_1 == u_id:
            obj = get_user_by_id_json(q.user_2)
        else:
            obj = get_user_by_id_json(q.user_1)
        obj['c_id'] = q.id
        obj['last_mess'] = get_last_mess_in_conv(q.id)
        user_list.append(obj)
    return user_list


def get_conv_json(c_id, u_id):
    conv = Conversation.query.filter(Conversation.id.__eq__(c_id)).first()
    obj = {}
    if str(conv.user_1).__eq__(str(u_id)):
        obj = get_user_by_id_json(conv.user_2)
    if str(conv.user_2).__eq__(str(u_id)):
        obj = get_user_by_id_json(conv.user_1)
    return obj


def create_conv(user_1, user_2):
    check = Conversation.query.filter((Conversation.user_1.__eq__(user_1) & Conversation.user_2.__eq__(user_2))
                                      | (Conversation.user_1.__eq__(user_2) & Conversation.user_2.__eq__(
        user_1))).first()
    if check is not None:
        return check
    conv = Conversation(user_1=user_1, user_2=user_2)
    db.session.add(conv)
    db.session.commit()
    return conv


def create_conv_json(user_1, user_2):
    conv = create_conv(user_1, user_2)
    obj = get_conv_json(conv.id, user_1)
    obj['c_id'] = conv.id
    return obj


def get_mess_conv(c_id):
    query = Message.query.filter(Message.conversation_id.__eq__(c_id))
    # query = query.order_by(desc(Message.created_at))
    return query.all()


def get_mess_conv_json(c_id):
    query = get_mess_conv(c_id)
    data = []

    for q in query:
        obj = {
            'c_id': q.conversation_id,
            'sender': q.sender,
            'receiver': q.receiver,
            'content': q.content,
            'created_at': q.created_at
        }
        data.append(obj)
    return data


def create_message(c_id, s_id, r_id, content):
    message = Message(conversation_id=c_id, sender=s_id, receiver=r_id, content=content)
    db.session.add(message)
    db.session.commit()
    return message


def create_message_json(c_id, s_id, r_id, content):
    message = create_message(c_id, s_id, r_id, content)
    obj = {
        'c_id': message.conversation_id,
        'sender': message.sender,
        'receiver': message.receiver,
        'content': message.content,
        'created_at': message.created_at
    }
    return obj


if __name__ == '__main__':
    with app.app_context():
        print(get_mess_conv_json(1))
