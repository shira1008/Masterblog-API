from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

FILE_NAME = "backend/posts.json"

def load_posts_from_file():
    """Load posts data from the JSON file."""
    try:
        with open(FILE_NAME, "r") as file:
            posts = json.load(file)
        return posts
    except FileNotFoundError:
        return []


def save_posts_to_file(posts):
    try:
        with open(FILE_NAME, 'w') as file:
            json.dump(posts, file, indent=4)
        print("Posts saved to JSON file")
    except Exception as e:
        print("Error saving posts to JSON file:", e)
        return jsonify({"error": "{e}"}), 400

POSTS = load_posts_from_file()



def validate_post_data(data):
    """Check if title, content, author, and date are present and not empty in the data.
    If any of the fields are missing or empty, return False."""
    if "title" not in data or "content" not in data or "author" not in data or "date" not in data:
        return False
    if len(data["title"]) < 1 or len(data["content"]) < 1 or len(data["author"]) < 1 or len(data["date"]) < 1:
        return False
    return True


def find_post_by_id(post_id):
    """ Find the post with the id `post_id`.
    If there is no post with this id, return None. """
    for post in POSTS:
      if post["id"] == post_id:
        return post
    return None


def convert_date_string(date_string):
    """convert the str to a date object"""
    try:
        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()
        return date_object
    except ValueError:
        return None



@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
  # if it's a POST request:
  if request.method == 'POST':
    new_post = request.get_json()
    if not validate_post_data(new_post):
      return jsonify({"error": "Invalid post data, you need to have title and content"}), 400

    # Generate a new ID for the post
    if not POSTS:
      new_id = 1
    else:
      new_id = max(post['id'] for post in POSTS) + 1
    new_post['id'] = new_id

    new_post['date'] = convert_date_string(new_post['date'])
    if new_post['date'] is None:
      return jsonify({"error": "Invalid date format. Expected format: YYYY-MM-DD"}), 400
    else:
      new_post['date'] = new_post['date'].strftime("%Y-%m-%d")
    # Add the new post
    POSTS.append(new_post)
   

    save_posts_to_file(POSTS)
    # print("Post saved to JSON file:", new_post)
    return jsonify(new_post), 201

  # if it's a GET request:
  if request.method == 'GET':
    sort_by = request.args.get('sort')
    direction_by = request.args.get('direction')
    if sort_by:
      if sort_by in ["title", "content", "author", "date" ]:
        sorted_posts = sorted(POSTS, key=lambda post: post[sort_by], reverse=(direction_by == "desc"))
      else:
        return jsonify({"error": "Invalid sort field. Available fields: title, content"}), 400
      if direction_by not in ["asc", "desc"]:
        return jsonify({"error": "Invalid direction value. Available values: asc, desc"}), 400
    else:
      sorted_posts = POSTS

    return jsonify(sorted_posts), 200



@app.route('/api/posts/<int:id>', methods=['DELETE'])
def del_post(id):
  post = find_post_by_id(id)
  # If the post wasn't found, return a 404 error
  if post is None:
    return jsonify({"error": "Post not found"}), 404
  # Remove the post from the list
  POSTS.remove(post)
  # save to storage
  save_posts_to_file(POSTS)
  # Return the deleted post
  return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post = find_post_by_id(id)
    if post is None:
        return jsonify({"error": "Post not found"}), 404

    updated_data = request.get_json()
    if 'title' in updated_data:
        post['title'] = updated_data['title']
    if 'content' in updated_data:
        post['content'] = updated_data['content']
    if 'author' in updated_data:
        post['author'] = updated_data['author']
    if "date" in updated_data:
        date_object = convert_date_string(updated_data["date"])
        if date_object is None:
            return jsonify({"error": "Invalid date format. Expected format: YYYY-MM-DD"}), 400
        post["date"] = date_object.strftime("%Y-%m-%d")
    
    save_posts_to_file(POSTS)
    return jsonify(post), 200



@app.route('/api/posts/search', methods=['GET'])
def search_post():
  title = request.args.get('title')
  content = request.args.get('content')
  author = request.args.get('author')
  date = request.args.get('date')
  filterd_posts = []

  if title:
    filterd_posts += [post for post in POSTS if post["title"].lower() == title.lower()]
    return jsonify(filterd_posts),200

  if content:
    filterd_posts += [post for post in POSTS if post["content"].lower() == content.lower()]
    return jsonify(filterd_posts), 200
  
  if author:
    filterd_posts += [post for post in POSTS if post["author"].lower() == author.lower()]
    return jsonify(filterd_posts), 200

  if date:
    filterd_posts += [post for post in POSTS if post["date"].lower() == date.lower()]
    return jsonify(filterd_posts), 200


  return jsonify(filterd_posts),200

  


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
