from flask import Flask

def init_app():
    app = Flask(__name__)
    # app.config.from_object("config.Config")

    with app.app_context():
        from . import routes

        from .plotlydash.dashboard import create_dashboard
        app = create_dashboard(app)

    return app