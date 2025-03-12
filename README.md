# Personal-Blog

This is a personal blog application that allows users to Create,Read,Update and Delete their posts. It features a default home page displaying blog posts, and a dashboard for Creating and editing posts. The blog uses BeanieODM for data management and storage.

Features

- Home Page:
  - Displays a list of all blog posts with their title, excerpt, and an optional image.
  
- Post Page:
  - Showcases the title, author name, blog content, and date published for each post.

- Dashboard:
  - Allows users to Create, Read, Update, Delete blog posts.

Technologies Used
    - Python
    - BeanieODM
    - FastAPI

Project Structure

Personal-Blog/
├── templates/         # HTML templates for the user interface
│   ├── create.html    # Template for creating a blog post
│   ├── home.html      # Template for the homepage listing blog posts
│   ├── post.html      # Template for viewing a single blog post
│   ├── dashboard.html # Template for managing blog posts
│   └── edit.html      # Template for editing a blog post
├── routes.py          # Contains routes for API endpoints
├── database.py        # Database configuration and initialization
├── connection.py      # Manages connections to the database
├── test.db            # Test database
├── blog.db            # Main database
├── requirements.txt   # Lists project dependencies
├── model.py           # Defines the data model for blog posts
└── main.py            # Application entry point

Installation and Setup

1. Clone the Repository
    Open your terminal and run:
    git clone <https://github.com/Miideh/Personal-Blog.git>
    cd "C:\Users\Surface Pro\Desktop\CodeCafe\Personal-Blog"

2. Set Up a Virtual Environment
    Create a virtual environment to manage your project dependencies effectively:
    python -m venv env

    Activate the virtual environment:
    source venv\Scripts\activate

3. Install the Dependencies
    pip install -r requirements.txt

4. Configure the Database
    Your blog uses BeanieODM for data storage.

5. Run the Blog Application
    python main.py

6. Access Your Blog
    Once the application is up and running, open your web browser and go to:
    <http://127.0.0.1:8000>

How to Use

1. Explore Blog Posts:
   - Visit the home page to browse all blog posts.
   - Click on a post title to view the full content.

2. Manage Blog Posts:
   - Visit the dashboard to create new posts or edit existing ones.
   - Delete any post that is no longer needed.

Future Improvements

 convert the blog application to make use of MongoDB instead of BeanieODM
