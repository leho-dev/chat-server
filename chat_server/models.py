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

        # c1 = Conversation(user_1=1, user_2=2)
        # c2 = Conversation(user_1=1, user_2=3)
        # c3 = Conversation(user_1=2, user_2=3)
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()

        # m1 = Message(content="Test 1", conversation_id=1, sender=1, receiver=2)
        # m2 = Message(content="Rep Test 1", conversation_id=1, sender=2, receiver=1)
        # m3 = Message(content="Test 2", conversation_id=1, sender=1, receiver=2)
        # m4 = Message(content="Rep Test 2", conversation_id=1, sender=2, receiver=1)
        # m5 = Message(content="Test 3", conversation_id=2, sender=1, receiver=3)
        # m6 = Message(content="Test 4", conversation_id=2, sender=1, receiver=3)
        # m7 = Message(content="Test 5", conversation_id=2, sender=1, receiver=3)
        # m8 = Message(content="Test 6", conversation_id=2, sender=3, receiver=1)
        # db.session.add_all([m1, m2, m3, m4, m5, m6, m7, m8])
        # db.session.commit()

        pass

