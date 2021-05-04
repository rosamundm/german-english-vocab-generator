import random
from flask import Blueprint, render_template, jsonify, make_response
from de_en_vocab.main.models import VocabItem, VocabSchema


main_blueprint = Blueprint(
    "main_blueprint", __name__,
    template_folder="templates",
    static_folder="static"
)


@main_blueprint.route("/", methods=["GET"])
def get_random_pair():
    vocab = VocabItem.query.all()
    random_record = random.choice(vocab)
    random_german_word = random_record.de_word
    english_translation = random_record.en_transl
    number_of_records = len(vocab)

    return render_template(
        "index.html",
        random_german_word=random_german_word,
        english_translation=english_translation,
        number_of_records=number_of_records
    )


"""
API TODO:
- move to another file
- display IDs on index as int not float
- fix encoding for German special characters
"""

@main_blueprint.route('/api/v1/index', methods=['GET'])
def get_vocab():
    all_vocab = VocabItem.query.all()
    vocab_schema = VocabSchema(many=True)
    vocab = vocab_schema.dump(all_vocab)
    return make_response(jsonify({"vocab": vocab}))


@main_blueprint.route('/api/v1/<int:id>', methods=['GET'])
def get_vocab_by_id(id):
    vocab_item = VocabItem.query.get(id)
    vocab_schema = VocabSchema()
    vocab = vocab_schema.dump(vocab_item)
    return make_response(jsonify({"vocab": vocab}))