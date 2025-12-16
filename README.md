# StudioFlow

## Video Demo
<INSERT YOUR VIDEO LINK HERE>

## Description

StudioFlow is a web application developed with Flask and SQLite as my Final Project for CS50.

The goal of this project was to create a practical tool for managing clients and projects, inspired by real needs of creative studios and freelancers. The application allows users to register and log in securely, manage clients and projects, and visualize key information through a dashboard.

StudioFlow includes features such as project status tracking, upcoming deadlines, prevention of invalid deletions, and real-time search using JavaScript and REST-style endpoints. Passwords are securely hashed, and all sensitive routes are protected.

Through this project, I applied concepts learned in CS50 such as web development with Flask, SQL queries, authentication, session management, and clean code organization. The project reflects a real-world use case and emphasizes usability and maintainability.


---

## Features

### Authentication
- User registration and login
- Secure password hashing
- Session-based authentication
- Protected routes using a custom `login_required` decorator

### User Profile
- Update username
- Optional password change
- Strong validation rules
- User feedback through flash messages

### Dashboard
- Total number of clients
- Total number of projects
- Project status breakdown (Completed, In Progress, Pending)
- Upcoming projects sorted by due date
- Top clients ranked by number of projects

### Clients Management
- Create, edit, list, and view clients
- Automatic project count per client
- Prevents deletion of clients with associated projects
- Real-time client search (no form submission)

### Projects Management
- Create, edit, list, and view projects
- Each project must belong to a client
- Project status and deadlines
- Real-time project search

### Live Search API
- REST-style endpoints (`/api/clients`, `/api/projects`)
- Dynamic filtering while typing
- Case-insensitive search
- Instant UI updates using JavaScript and Fetch API

---

## Technologies Used

- Python
- Flask
- SQLite
- Jinja2
- WTForms
- Bootstrap 5
- JavaScript (Fetch API)
- HTML / CSS

---

## Project Structure

studioflow/
│
├── app.py
├── db.py
├── forms.py
├── helpers.py
├── init_db.py
├── queries.py
├── schema.sql
│
├── templates/
│ ├── auth_layout.html
│ ├── index.html
│ ├── layout.html
│ ├── login.html
│ ├── profile.html
│ ├── register.html
│ ├── clients/
│ │   ├── detail.html
│ │   ├── edit.html
│ │   ├── list.html
│ │   └── new.html
│ └── projects/
│     ├── detail.html
│     ├── edit.html
│     ├── list.html
│     └── new.html
│
├── static/
│ ├── css/
│ │   └── style.css
│ ├── img/
│ │   └── studio_bg.png
│ └── js/
│     └── search.js
│
├── README.md
└── requirements.txt

---

## How to Run

1. Create and activate a virtual environment  
2. Install dependencies  

```bash
pip install -r requirements.txt
```

3. Initialize the database  
4. Run the Flask server  

```bash
flask run
```

## Author
Studio Flow was developed by Amanda Falcão da Silva as the final project for CS50 - Introduction to Computer Science
