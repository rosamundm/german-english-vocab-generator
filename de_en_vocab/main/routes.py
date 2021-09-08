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
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

from de_en_vocab.main.forms import VocabAddForm
from de_en_vocab.main.models import db, User, VocabItem, VocabSchema


VOCAB_ITEMS = VocabItem.query.all()

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
def index():
    """
    Create context to show random vocab pair on index page.
    """
    random_record = random.choice(VOCAB_ITEMS)
    random_german_word = random_record.de_word
    english_translation = random_record.en_transl
    number_of_records = len(VOCAB_ITEMS)

    return render_template(
        "index.html",
        random_german_word=random_german_word,
        english_translation=english_translation,
        number_of_records=number_of_records,
    )


@main_blueprint.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    """
    Default admin view for adding new vocab pair.
    """

    vocab_add_form = VocabAddForm()

    if vocab_add_form.validate_on_submit:
        vocab_item = VocabItem(
            de_word=vocab_add_form.de_word.data,
            en_transl=vocab_add_form.en_transl.data
        )

        db.session.add(vocab_item)
        db.session.commit()
        flash("Item created")

        if db.session.commit():
            return redirect(url_for("main_blueprint.admin_list"))

    return render_template(
        "admin/create.html",
        vocab_add_form=vocab_add_form,
        vocab_item=vocab_item
    )


@main_blueprint.route("/admin/list/", methods=["GET", "POST"])
@login_required
def admin_list():
    return render_template("admin/list.html", VOCAB_ITEMS=VOCAB_ITEMS)


@main_blueprint.route("/admin/list/<int:id>/", methods=["GET", "POST"])
@login_required
def admin_detail(id):
    vocab_item = [vocab_item for vocab_item in VOCAB_ITEMS if vocab_item.id == id][0]
    return render_template("admin/detail.html", vocab_item=vocab_item)


@main_blueprint.route("/admin/list/<int:id>/edit/", methods=["GET", "POST"])
@login_required
def admin_detail_edit(id):
    vocab_item = VocabItem.query.get_or_404(id)
    return render_template("admin/edit_detail.html", vocab_item=vocab_item)


@main_blueprint.route("/admin/list/<int:id>/delete/", methods=["GET", "POST"])
@login_required
def admin_detail_delete(id):
    vocab_item = VocabItem.query.get_or_404(id)
    db.session.delete(vocab_item)
    db.session.commit()
    return redirect(url_for("main_blueprint.admin_list"))


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
