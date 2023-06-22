from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_post_data(data):
    """Check if content ot title in the data and that they are not empty,
   if they are not in the data, return False """
    if "title" not in data or "content" not in data:
        return False
    if len(data["title"]) < 1 or len(data["content"]) < 1:
        return False
    return True

def find_post_by_id(post_id):
    """ Find the post with the id `post_id`.
    If there is no post with this id, return None. """
    for post in POSTS:
      if post["id"] == post_id:
        return post
    return None


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
  # if it's a POST request:
  if request.method == 'POST':
    new_post = request.get_json()
    if not validate_post_data(new_post):
      return jsonify({"error": "Invalid post data, you need to have title and content"}), 400

    # Generate a new ID for the post
    new_id = max(post['id'] for post in POSTS) + 1
    new_post['id'] = new_id

    # Add the new post
    POSTS.append(new_post)

    return jsonify(new_post), 201

  # if it's a GET request:
  if request.method == 'GET':
    sort_by = request.args.get('sort')
    direction_by = request.args.get('direction')
    if sort_by:
      if sort_by == "title":
        sorted_posts = sorted(POSTS, key=lambda post: post["title"], reverse=(direction_by == "desc"))
      elif sort_by == "content":
        sorted_posts = sorted(POSTS, key=lambda post: post["content"], reverse=(direction_by == "desc"))
      else:
        return jsonify({"error": "Invalid sort field. Available fields: title, content"}), 400
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
  # Return the deleted post
  return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
  post = find_post_by_id(id)
  if post is None:
    return jsonify({"error": "Post not found"}), 404

  updated_data = request.get_json()
  post.update(updated_data)

  return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_post():
  title = request.args.get('title')
  content = request.args.get('content')
  filterd_posts = []

  if title:
    filterd_posts += [post for post in POSTS if post["title"].lower() == title.lower()]
    return jsonify(filterd_posts),200

  if content:
    filterd_posts += [post for post in POSTS if post["content"].lower() == content.lower()]
    return jsonify(filterd_posts), 200

  return jsonify(filterd_posts),200

  


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
