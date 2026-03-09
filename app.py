from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)


def load_posts():
    """Load blog posts from the JSON file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    blog_posts_file = os.path.join(base_dir, "blog_posts.json")

    with open(blog_posts_file, "r", encoding="utf-8") as post_file:
        return json.load(post_file)


def save_posts(posts):
    """Save all blog posts to the JSON file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    blog_posts_file = os.path.join(base_dir, "blog_posts.json")

    with open(blog_posts_file, "w", encoding="utf-8") as post_file:
        json.dump(posts, post_file, indent=4)


def fetch_post_by_id(post_id):
    """Return one post by ID, or None if not found."""
    posts = load_posts()
    for post in posts:
        if post["id"] == post_id:
            return post
    return None


@app.route("/")
def index():
    # Load all blog posts and render the index page
    posts = load_posts()
    return render_template("index.html", posts=posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    # Handle form submission to add a new blog post
    if request.method == "POST":
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")

        posts = load_posts()

        # Generate a new unique ID for the post
        if posts:
            new_id = max(post["id"] for post in posts) + 1
        else:
            new_id = 1

        # Create a new post dictionary
        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }

        posts.append(new_post)
        save_posts(posts)

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete/<int:post_id>")
def delete(post_id):
    posts = load_posts()
    posts = [post for post in posts if post["id"] != post_id]
    save_posts(posts)
    return redirect(url_for("index"))


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    posts = load_posts()
    post = None

    for blog_post in posts:
        if blog_post["id"] == post_id:
            post = blog_post
            break

    if post is None:
        return "Post not found", 404

    if request.method == "POST":
        post["author"] = request.form.get("author")
        post["title"] = request.form.get("title")
        post["content"] = request.form.get("content")

        save_posts(posts)
        return redirect(url_for("index"))

    return render_template("update.html", post=post)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)