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


@app.route("/add", methods=["GET", "POST"])
def add():
    # Handle form submission to add a new blog post
    if request.method == "POST":
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")

        posts = load_posts()

        # create new unique post ID
        if posts:
            new_id = max(post["id"] for post in posts) + 1
        else:
            new_id = 1

       # create new post dictionary
        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }

        # add new post to the list and save json
        posts.append(new_post)
        save_posts(posts)

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/")
def index():
    posts = load_posts()
    return render_template("index.html", posts=posts)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)