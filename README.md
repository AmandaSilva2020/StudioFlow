# StudioFlow

## Video Demo
https://youtu.be/UA10d_W31Ww

---

## Description

StudioFlow is a web application developed with Flask and SQLite as my Final Project for CS50: Introduction to Computer Science.

The main goal of this project was to create a practical and simple tool to help freelancers to manage clients and projects in an organized way. The idea came from my real needs as a freelancer: keeping track of clients, monitoring project status, and avoiding common mistakes such as deleting important data by accident.

At first, StudioFlow started as a much simpler idea. However, since I plan to use this application in my own workflow, I gradually expanded it and made it more robust over time. This allowed me to apply many concepts learned throughout the course while building something useful in a real-world scenario.

The application allows users to register and log in securely, manage clients and projects, and visualize key information through a dashboard. All sensitive routes are protected, passwords are securely hashed, and the interface is designed to be clear and easy to use.

---

## Features

### Authentication
- User registration and login
- Secure password hashing using Werkzeug
- Session-based authentication
- Protected routes using a custom `login_required` decorator (Inspired by CS50's Finance app)

### User Profile
- Update username
- Optional password change
- Strong validation rules for passwords using Wtforms
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
- Prevents deletion of clients that still have associated projects
- Real-time client search without form submission

### Projects Management
- Create, edit, list, and view projects
- Each project must belong to a client
- Project status tracking and deadlines
- Real-time project search

### Live Search API
- REST-style endpoints (`/api/clients` and `/api/projects`)
- Dynamic filtering while typing
- Case-insensitive search
- Instant UI updates using JavaScript and the Fetch API

---

## Technologies Used

- Python
- Flask
- SQLite
- Jinja2
- WTForms
- Bootstrap 5
- JavaScript (Fetch API)
- HTML and CSS

---

## Project Structure and Files

The project is organized to keep the code clean and easy to understand:

- **app.py**  
  The main application file. It defines all routes, handles requests, manages sessions, and connects the different parts of the application.

- **db.py**  
  Responsible for database connection management. It centralizes the logic for opening and closing the SQLite database using Flask’s `g` object.

- **helpers.py**  
  Contains one helper function: `login_required` decorator, which protects routes that should only be accessible to logged-in users.

- **forms.py**  
  Defines all WTForms used in the application, including validation rules for login, registration, and profile editing.

- **schema.sql**  
  Contains the SQL schema used to create the database tables.

- **init_db.py**  
  Script used to initialize the database using the schema file.

- **queries.py**  
  A file with reusable SQL query functions (for clients, projects, and dashboard metrics), so I don’t repeat the same queries inside routes.

- **templates/**  
  Contains all HTML templates. Templates are organized into subfolders for clients and projects to keep things structured.

- **static/**  
  Includes CSS, JavaScript, and image files. The `search.js` file handles the real-time search functionality.

---

## Design Decisions

Several design decisions were made during development:

- **Flask and SQLite** were chosen because I liked to work with them in CS50. They are lightweight, easy to understand, and well-suited for a beginner-friendly project.
- **No ORM was used**. Instead, raw SQL queries were written to practice SQL directly, as taught in CS50.
- **Client deletion is restricted** if there are associated projects. This prevents accidental data loss and reflects real-world constraints.
- **Live search** was implemented using JavaScript and API routes, allowing results to update dynamically while the user types and avoiding unnecessary page reloads, as is common in modern web applications.
- **Code separation** into multiple files was done to keep the application more readable and maintainable as it grew.

---

## How to Run

1. Create and activate a virtual environment  
2. Install dependencies:

```bash
pip install -r requirements.txt
```
3. Initialize the database
4. Run the Flask server:

```bash
flask run
```

## Author
StudioFlow was developed by Amanda Falcão da Silva as the Final Project for CS50 – Introduction to Computer Science.