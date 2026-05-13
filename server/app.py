from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


CORS(app)
app.secret_key = "sehtrsdyhndtejdydunuyehbdrvteryhe"


# MODELS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)

    posts = db.relationship("Post", backref='user')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id") )
    comments = db.relationship("Comment", backref='post')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)

    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))


# ==================================== CRUD POST ================================================================
# READ
@app.route("/posts")
def fetch_posts():
    # fetching data in sqlalchemy
    posts = Post.query.all()
    
    results = []

    for post in posts:
        results.append({
            "id":post.id,
            "title": post.title,
            "content": post.content}
        )
    return jsonify(results), 200

# POST DATA/ADD
# READ 1
# UPDATE
# DELETE

# ADD
@app.route("/posts", methods=["POST"])
def add_post():
    data = request.get_json()

    new_post = Post(
        title=data["title"],
        content=data["content"]
    )

    db.session.add(new_post)
    db.session.commit()

    return jsonify({"success": "Post created successfully"}), 201


# read one post
@app.route("/posts/<int:post_id>")
def fetch_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post does not exists"}), 404
    
    my_post = {
        "id": post.id,
        "title": post.title,
        "content": post.content
    }
    return jsonify(my_post), 200


# -0---UPDATE
@app.route("/posts/<int:id>", methods=["PUT"])
def update_post(id):
    # fetch the post
    post = Post.query.get(id)
    # if post doesn't exists give an error
    if not post:
        return jsonify({"error": "Post does not exists"}), 404
    

    data = request.get_json()

    post.title = data.get("title", post.title)
    post.content = data.get("content", post.content)

    db.session.commit()

    return jsonify({"success": "Post updated successfully"}), 200


# DELETE
@app.route("/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    # fetch the post
    post = Post.query.get(id)
    # if post doesn't exists give an error
    if not post:
        return jsonify({"error": "The post you want to delete does not exists"}), 404

    db.session.delete(post)
    db.session.commit()

    return jsonify({"success": "Post deleted successfully"}), 200

# export FLASK_APP=app.py
# export FLASK_DEBUG=1

# ==================================== CRUD POST ================================================================