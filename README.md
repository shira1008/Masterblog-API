# Masterblog-API

This project consists of a backend API built with Flask and a frontend user interface (UI) implemented in JavaScript and flask. The backend API provides endpoints for managing blog posts, including creating new posts, retrieving posts, updating posts, and deleting posts. The frontend UI interacts with the API to display blog posts, allow users to create new posts, and perform other actions such as deleting posts and incrementing post likes.

## Backend API
The backend API is built with Flask, a Python web framework. It provides the following endpoints:

- `GET /api/posts`: Retrieves all blog posts or applies sorting and filtering options.

- `POST /api/posts`: Creates a new blog post.

- `PUT /api/posts/<int:id>`: Updates an existing blog post with the specified ID.

- `DELETE /api/posts/<int:id>`: Deletes the blog post with the specified ID.

- `GET /api/posts/search`: Searches for blog posts based on title, content, author, or date.

- `POST /api/posts/<int:post_id>/likes`: Increments the likes count of a blog post by 1.

- The API stores the blog posts in a JSON file named posts.json. The file is loaded when the API starts, and any modifications to the posts are saved back to the file for data persistence.


## Frontend User Interface
The frontend UI is implemented in JavaScript and interacts with the backend API to perform various actions. The JavaScript code utilizes the Fetch API to send HTTP requests to the API endpoints and update the UI accordingly.
it is also integrated with Flask to serve the UI files and handle routing it allows the UI to be rendered from the backend.

The UI allows users to:

- View all blog posts, sorted and filtered based on selected options.

- Create a new blog post by providing a title, content, author, and date.

- Update an existing blog post by modifying its title, content, author, or date.

- Delete a blog post.

- Search for blog posts by title, content, author, or date.

- Increment the likes count of a blog post by 1.

* The JavaScript code includes error handling to display error messages on the UI in case of any issues with the API requests./
