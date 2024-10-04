from flask import jsonify, request
from models import db, User, Post
from schemas import UserSchema, PostSchema
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError

user_schema = UserSchema()
post_schema = PostSchema()
users_schema = UserSchema(many=True)
posts_schema = PostSchema(many=True)

def register_routes(app):
    @app.route('/users', methods=['POST'])
    def create_user():
        try:
            user_data = user_schema.load(request.json)
            new_user = User(**user_data)
            db.session.add(new_user)
            db.session.commit()
            return user_schema.dump(new_user), 201  # HTTP 201 Created
        except ValidationError as err:
            return jsonify(err.messages), 400  # HTTP 400 Bad Request
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "User already exists."}), 409  # HTTP 409 Conflict

    @app.route('/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = User.query.get(user_id)
        if user:
            return user_schema.dump(user), 200  # HTTP 200 OK
        return jsonify({"error": "User not found."}), 404  # HTTP 404 Not Found

    @app.route('/posts', methods=['POST'])
    def create_post():
        try:
            post_data = post_schema.load(request.json)
            new_post = Post(**post_data)
            db.session.add(new_post)
            db.session.commit()
            return post_schema.dump(new_post), 201  # HTTP 201 Created
        except ValidationError as err:
            return jsonify(err.messages), 400  # HTTP 400 Bad Request

    @app.route('/posts/<int:post_id>', methods=['GET'])
    def get_post(post_id):
        post = Post.query.get(post_id)
        if post:
            return post_schema.dump(post), 200  # HTTP 200 OK
        return jsonify({"error": "Post not found."}), 404  # HTTP 404 Not Found