import random

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    jsonify,
    make_response,
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

from de_en_vocab.main.models import User, VocabItem, VocabSchema


main_blueprint = Blueprint(
    "main_blueprint",
    __name__,
    template_folder="templates",
    static_folder="static"
)

auth_blueprint = Blueprint(
    "auth_blueprint",
    __name__,
    template_folder="templates",
    static_folder="static"
)


@main_blueprint.route("/", methods=["GET"])
def get_random_pair():  # TODO: rename
    vocab = VocabItem.query.all()
    random_record = random.choice(vocab)
    random_german_word = random_record.de_word
    english_translation = random_record.en_transl
    number_of_records = len(vocab)

    return render_template(
        "index.html",
        random_german_word=random_german_word,
        english_translation=english_translation,
        number_of_records=number_of_records,
    )


@main_blueprint.route("/admin")
@login_required
def admin():
    return render_template("admin.html")


@auth_blueprint.route("/login")
def login():
    return render_template("login.html")


@auth_blueprint.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(username=username).first()

    if not (user or check_password_hash(user.password, password)):
        flash("Please try again")
        return redirect(url_for("auth_blueprint.login"))

    login_user(user, remember=remember)

    return redirect(url_for("main_blueprint.admin"))


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main_blueprint.get_random_pair"))


"""
API TODO:
- move to another file
- display IDs on index as int not float
- fix encoding for German special characters
"""


@main_blueprint.route("/api/v1/index/", methods=["GET"])
def get_vocab():
    all_vocab = VocabItem.query.all()
    vocab_schema = VocabSchema(many=True)
    vocab = vocab_schema.dump(all_vocab)
    return make_response(jsonify({"vocab": vocab}))


@main_blueprint.route("/api/v1/<int:id>", methods=["GET"])
def get_vocab_by_id(id):
    vocab_item = VocabItem.query.get(id)
    vocab_schema = VocabSchema()
    vocab = vocab_schema.dump(vocab_item)
    return make_response(jsonify({"vocab": vocab}))
