from random import randint
from flask import render_template, redirect, request, session
from flask_login import login_user, logout_user
from chat_server.decorators import login_required, not_auth
from chat_server import flow, dao, mail
from flask_mail import Message
from chat_server.models import User

listOTP = []

@not_auth
def login():
    return render_template('index.html')


def login_oauth():
    authorization_url, state = flow.authorization_url()
    return redirect(authorization_url)


def oauth_callback():
    try:
        global listOTP
        user_oauth = dao.get_user_oauth()
        print(user_oauth)
        email = user_oauth['email']
        session['email'] = email
        otp = str(randint(000000, 999999))
        msg = Message('OTP FROM CHAT OU', sender='cloneg2001@gmail.com', recipients=[email])
        msg.body = otp
        mail.send(msg)
        obj = {
            'otp': otp,
            'email': email,
            'fullname': user_oauth['name'],
            'avatar': user_oauth['picture'],
        }
        listOTP.append(obj)
        print(listOTP)
        return redirect('/verify')
    except:
        return redirect("/auth")

@not_auth
def verify():
    global listOTP
    if request.method == 'GET':
        return render_template('verify.html')
    if request.method == 'POST':
        data = request.get_json()
        otp_user = data['otp']
        email_user = data['email']
        obj_data = None
        for obj in listOTP:
            if obj['otp'] == otp_user:
                obj_data = obj
                break
        if obj_data is not None and email_user == obj_data['email']:
            user = User.query.filter_by(email=email_user).first()
            if user is None:
                fullname = obj_data['fullname']
                avatar = obj_data['avatar']
                user = dao.create_user(fullname, email_user, avatar)
            login_user(user)
            listOTP = list(filter(lambda x: x['otp'] != otp_user, listOTP))
            print(listOTP)
            return {
                "status": 200,
            }
        return {
            "status": 400,
            "message": "Invalid OTP"
        }

@login_required
def home():
    return render_template('home.html')


def search_user():
    data = request.get_json()
    user_list = dao.get_list_user_by_text(text=data['text'])
    return {
        "status": 200,
        "data": user_list
    }


def get_list_receiver(u_id):
    data = dao.get_list_receiver(u_id)
    return {
        "status": 200,
        "data": data
    }


def add_conversation():
    data = request.get_json()
    conv = dao.create_conv_json(data['user_1'], data['user_2'])
    return {
        "status": 200,
        "data": conv
    }


def get_mess_conv(c_id):
    data = dao.get_mess_conv_json(c_id)
    return {
        "status": 200,
        "data": data
    }

def create_message():
    data = request.get_json()
    mess = dao.create_message_json(data['c_id'], data['s_id'], data['r_id'], data['content'])
    return {
        "status": 200,
        "data": mess
    }


def logout():
    logout_user()
    session.clear()
    return redirect('/auth')
