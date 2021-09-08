from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema
from flask_login import UserMixin


db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))


class VocabItem(db.Model):
    __tablename__ = "vocab"
    id = db.Column(db.Integer, primary_key=True)
    de_word = db.Column(db.String(200), index=True, unique=True)
    en_transl = db.Column(db.String(200), index=True, unique=True)

    def __repr__(self):
        return str(id)


class VocabSchema(SQLAlchemySchema):
    id = fields.Number(dump_only=True)
    de_word = fields.String(required=True)
    en_transl = fields.String(required=True)

    class Meta(SQLAlchemySchema.Meta):
        model = VocabItem
        sqla_session = db.session


def init_db():
    """
    Migrate any new models that may have been created.
    """

    db.create_all()
    db.session.commit()


init_db()
