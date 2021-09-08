from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class VocabAddForm(FlaskForm):
    de_word = StringField("German:", validators=[DataRequired()])
    en_transl = StringField("English:", validators=[DataRequired()])
    submit = SubmitField("Submit")
