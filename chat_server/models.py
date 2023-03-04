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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # a = User(fullname='Nguyễn Văn A')
        # b = User(fullname="Lê B")
        # db.session.add_all([a, b])
        # db.session.commit()

