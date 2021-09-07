from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


def create_app():
    app = Flask(
        __name__,
        instance_relative_config=False
    )
    app.config.from_object("config.Config")
    with app.app_context():
        from .main import routes
        app.register_blueprint(routes.main_blueprint)
        app.register_blueprint(routes.auth_blueprint)
  
        login_manager = LoginManager()
        login_manager.login_view = "auth_blueprint.login"
        login_manager.init_app(app)

        from de_en_vocab.main.models import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        return app


app = create_app()

db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.init_app(app)

if __name__ == "__main__":
    app.run(debug=False)
