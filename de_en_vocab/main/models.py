from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
# from marshmallow_sqlalchemy import ModelSchema, SQLAlchemySchema


db = SQLAlchemy(app)


class VocabItem(db.Model):
    __tablename__ = "vocab"
    id = db.Column(db.Integer, primary_key=True)
    de_word = db.Column(db.String(200), index=True, unique=True)
    en_transl = db.Column(db.String(200), index=True, unique=True)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def __repr__(self):
        return str(id)

"""
class VocabSchema(SQLAlchemySchema):
    id = fields.Number(dump_only=True)
    de_word = fields.String(required=True)
    en_transl = fields.String(required=True)

    class Meta(ModelSchema.Meta):
        model = VocabItem
        sqla_session = db.session
"""

