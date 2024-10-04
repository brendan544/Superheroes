from flask import Flask
from models import db
from routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)
    register_routes(app)
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # Create tables
    app.run(debug=True)





























































