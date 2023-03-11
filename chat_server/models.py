import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Enum, DateTime, Time, Float
from chat_server import app, db
from flask_login import UserMixin


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class User(BaseModel, UserMixin):
    email = Column(String(50), nullable=False)
    fullname = Column(String(50), nullable=False)
    avatar = Column(String(100))

    def __str__(self):
        return self.fullname


class Conversation(BaseModel):
    user_1 = Column(Integer, ForeignKey(User.id), nullable=False)
    user_2 = Column(Integer, ForeignKey(User.id), nullable=False)
    create_at = Column(DateTime, default=datetime.datetime.now())


class Message(BaseModel):
    sender = Column(Integer, ForeignKey(User.id), nullable=False)
    receiver = Column(Integer, ForeignKey(User.id), nullable=False)
    conversation_id = Column(Integer, ForeignKey(Conversation.id), nullable=False)
    content = Column(Text)
    is_seen = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now())

    def __str__(self):
        return self.content


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # a = User(fullname='Nguyễn Văn A')
        # b = User(fullname="Lê B")
        # db.session.add_all([a, b])
        # db.session.commit()

        c1 = Conversation()

        # m1 = Message(content="Test 1", sender=18, receiver=19)
        # m2 = Message(content="Rep Test 1", sender=19, receiver=18)
        # m3 = Message(content="Test 2", sender=18, receiver=19)
        # m4 = Message(content="Rep Test 2", sender=19, receiver=19)
        # m5 = Message(content="Test 3", sender=20, receiver=18)
        # m6 = Message(content="Test 4", sender=20, receiver=18)
        # m7 = Message(content="Test 5", sender=21, receiver=18)
        # m8 = Message(content="Test 6", sender=22, receiver=18)
        # m9 = Message(content="Test 47", sender=20, receiver=18)
        # db.session.add_all([m9])
        # db.session.commit()

