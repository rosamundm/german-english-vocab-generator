from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate


def create_app():
    app = Flask(
        __name__,
        instance_relative_config=False
    )
    app.config.from_object("config.Config")
    with app.app_context():
        from .main import routes
        app.register_blueprint(routes.main_blueprint)
        return app


app = create_app()

db = SQLAlchemy(app)
# migrate = Migrate(app, db)
db.init_app(app)

if __name__ == "__main__":
    app.run(debug=False)
