from db import get_db, close_db

from flask import Flask, render_template, request, redirect, session, url_for, g, flash
from flask_session import Session
from forms import RegisterForm, LoginForm, ProfileForm
from queries import get_all_clients, get_clients_with_project_counts, get_client_by_id, get_all_projects, get_dashboard_data
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = "AmandSecretKey123"

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


app.teardown_appcontext(close_db)

@app.route("/")
@login_required
def index():
    
    data = get_dashboard_data()

    return render_template("index.html", data=data)
    
# AUTH ROUTES

@app.route("/login", methods=["GET", "POST"])
def login():
    # if it's a GET request → show the form
    if request.method == "GET":
        session.clear()

    form = LoginForm()        

    # if it's a POST request → validate and log in
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        # Check if user exists and password is correct
        if user is None or not check_password_hash(user["hash"], password):
            form.username.errors.append("Invalid username or password.")
            return render_template("login.html", form=form)
        
        # Log the user in (store info in session)
        session.clear()
        session["user_id"] = user["id"]
        session["username"] = user["username"]

        return redirect(url_for("index"))

    # if validation fails, re-render the login page with form errors
    return render_template("login.html", form=form)
        

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        # Clear any existing user session
        session.clear()

    # Handle Post request for registration
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Ensure DB connection is established
        db = get_db()

        # Check if username already exists
        existing_user = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()

        if existing_user:
            form.username.errors.append("Username already taken.")
            return render_template("register.html", form=form)
        
        # Hash the password and store user in the database
        hash = generate_password_hash(password)

        # Insert new user into the database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash))
        db.commit()

        return redirect(url_for("login"))
    
    # Render registration page for GET request
    return render_template("register.html", form=form)
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# PROFILE ROUTES

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    form = ProfileForm()
    db = get_db()

    user = db.execute(
        "SELECT * FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()

    # GET → only populate form with current username
    if request.method == "GET":
        form.username.data = user["username"]
        return render_template("profile.html", form=form)

    # POST → first validate form
    if not form.validate_on_submit():
        return render_template("profile.html", form=form)

    new_username = form.username.data.strip()
    new_password = form.new_password.data or ""
    confirmation = form.confirmation.data or ""
    current_password = form.current_password.data or ""

    # 1. Check for username uniqueness
    existing_user = db.execute(
        "SELECT id FROM users WHERE username = ? AND id != ?",
        (new_username, user["id"])
    ).fetchone()

    if existing_user:
        flash("This username is already taken.", "warning")
        return render_template("profile.html", form=form)

    # 2. Change password flow
    password_errors = False

    # If any password field is filled, user wants to change password
    if new_password or confirmation or current_password:

        # new_password is required
        if not new_password:
            form.new_password.errors.append("Enter a new password.")
            password_errors = True

        # confirmation is required
        if not confirmation:
            form.confirmation.errors.append("Confirm the new password.")
            password_errors = True

        # current_password is required
        if not current_password:
            form.current_password.errors.append("Enter your current password.")
            password_errors = True

        # If everything is filled, check if new_password matches confirmation
        if new_password and confirmation and new_password != confirmation:
            form.confirmation.errors.append("Passwords must match.")
            password_errors = True

        # if no errors so far, check if current_password is correct
        if not password_errors:
            if not check_password_hash(user["hash"], current_password):
                form.current_password.errors.append("Current password is incorrect.")
                password_errors = True

        # if any error occurred, re-render the form with errors
        if password_errors:
            return render_template("profile.html", form=form)

        # Update username and password
        new_hash = generate_password_hash(new_password)
        db.execute(
            "UPDATE users SET username = ?, hash = ? WHERE id = ?",
            (new_username, new_hash, user["id"])
        )
        db.commit()

        session["username"] = new_username

        flash("Profile and password updated successfully!", "success")
        return redirect(url_for("profile"))

    # 3. Update only username if it has changed
    if new_username != user["username"]:
        db.execute(
            "UPDATE users SET username = ? WHERE id = ?",
            (new_username, user["id"])
        )
        db.commit()

        session["username"] = new_username
        
        flash("Profile updated successfully!", "success")
    else:
        flash("No changes were made.", "info")

    return redirect(url_for("profile"))


# CLIENT ROUTES

@app.route("/clients")
@login_required
def clients():
    clients = get_clients_with_project_counts()

    return render_template("clients/list.html", clients=clients)

@app.route("/clients/new", methods=["GET", "POST"])
@login_required
def new_client():    
    
    if request.method == "POST":
        name = request.form.get("name")
        company = request.form.get("company")
        email = request.form.get("email")
        phone = request.form.get("phone")
        notes = request.form.get("notes")

        # Create new client entry
        db = get_db()
        db.execute(
            "INSERT INTO clients (name, company, email, phone, notes) VALUES (?, ?, ?, ?, ?)",
            (name, company, email, phone, notes)
        )
        db.commit()

        flash("Client created successfully.", "success")
        return redirect(url_for("clients"))
    
    return render_template("clients/new.html")
    
@app.route("/clients/<int:client_id>")
@login_required
def client_detail(client_id):
    db = get_db()
    
    # Find client by ID
    client = get_client_by_id(client_id)

    if client is None:
        return "Client not found", 404

    projects = db.execute("SELECT * FROM projects WHERE client_id = ?", (client_id,)).fetchall()

    # Count open projects
    open_projects = sum(1 for project in projects if project["status"] == "In Progress")

    return render_template("clients/detail.html", client=client, projects=projects, open_projects=open_projects)
    
@app.route("/clients/<int:client_id>/edit", methods=["GET", "POST"])
@login_required
def edit_client(client_id):
    db = get_db()

    client = get_client_by_id(client_id)
    if client is None:
        return "Client not found", 404

    if request.method == "POST":
        name = request.form.get("name")
        company = request.form.get("company")
        email = request.form.get("email")
        phone = request.form.get("phone")
        notes = request.form.get("notes")

        # Update client data
        db.execute("UPDATE clients SET name = ?, company = ?, email = ?, phone = ?, notes = ? WHERE id = ?", (name, company, email, phone, notes, client_id))

        db.commit()

        flash("Client updated successfully.", "success")
        return redirect(url_for("client_detail", client_id=client_id))

    # GET: show form with existing client data
    return render_template("clients/edit.html", client=client)

@app.route("/clients/<int:client_id>/delete", methods=["POST"])
@login_required
def delete_client(client_id):
    db = get_db()

    client = get_client_by_id(client_id)
    if client is None:
        return "Client not found", 404
    
    # Check if client has associated projects
    row = db.execute("SELECT COUNT(*) AS count FROM projects WHERE client_id = ?", (client_id,)).fetchone()
    project_count = row["count"] if row else 0

    # If there are associated projects, do not delete and redirect back
    if project_count > 0:
        flash("This client cannot be deleted because they still have associated projects.", "warning")
        return redirect(url_for("client_detail", client_id=client_id))
    
    # Delete client from database
    db.execute("DELETE FROM clients WHERE id = ?", (client_id,))
    db.commit()

    # Redirect to clients list
    flash("Client deleted successfully.", "success")
    return redirect(url_for("clients"))


# PROJECT ROUTES

@app.route("/projects")
@login_required
def projects():

    projects = get_all_projects()

    return render_template("projects/list.html", projects=projects)

@app.route("/projects/new", methods=["GET", "POST"])
@login_required
def new_project():

    db = get_db()

    if request.method == "POST":
        name = request.form.get("name")
        selected_client_id = int(request.form.get("client_id"))
        status = request.form.get("status")
        description = request.form.get("description")
        notes = request.form.get("notes")
        start_date = request.form.get("start_date")
        due_date = request.form.get("due_date")


        # Create new project entry
        db.execute("INSERT INTO projects (name, client_id, status, description, notes, start_date, due_date) VALUES (?, ?, ?, ?, ?, ?, ?)", (name, selected_client_id, status, description, notes, start_date, due_date))
        db.commit()


        # Redirect to projects list
        flash("Project created successfully.", "success")
        return redirect(url_for("projects"))

    # GET: show new project form
    clients = get_all_clients()

    client_id = request.args.get("client_id", type=int)
    selected_client = None

    if client_id:
        selected_client = db.execute("SELECT id, name FROM clients WHERE id = ?", (client_id,)).fetchone()

    return render_template("projects/new.html", clients=clients, selected_client=selected_client)

@app.route("/projects/<int:project_id>")
@login_required
def project_detail(project_id):

    db = get_db()

    # Search for project and its client
    project = db.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()

    if project is None:
        return "Project not found", 404
    
    client = db.execute("SELECT * FROM clients WHERE id = ?", (project["client_id"],)).fetchone()
        
    return render_template("projects/detail.html", project=project, client=client)
    


@app.route("/projects/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
def edit_project(project_id):

    db = get_db()
    
    # Find project by ID
    project = db.execute("SELECT projects.*, clients.name AS client_name FROM projects JOIN clients ON projects.client_id = clients.id WHERE projects.id = ?", (project_id,)).fetchone()
    if project is None:
        return "Project not found", 404

    if request.method == "POST":
        # read form data and update project
        name = request.form.get("name")
        status = request.form.get("status")
        description = request.form.get("description")
        notes = request.form.get("notes")
        start_date = request.form.get("start_date")
        due_date = request.form.get("due_date")

        db.execute("UPDATE projects SET name = ?, status = ?, description = ?, notes = ?, start_date = ?, due_date = ? WHERE id = ?", (name, status, description, notes, start_date, due_date, project_id))
        db.commit()

        # redirect to project detail page
        flash("Project updated successfully.", "success")
        return redirect(url_for("project_detail", project_id=project_id))

    # GET: show form with existing project data
    return render_template("projects/edit.html", project=project)

@app.route("/projects/<int:project_id>/delete", methods=["POST"])
@login_required
def delete_project(project_id):

    db  = get_db()
    project = db.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    
    if project is None:
        return "Project not found", 404

    # remover o projeto da lista desse cliente
    db.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    db.commit()

    # Redirect to client detail page
    client = get_client_by_id(project["client_id"])
    flash("Project deleted successfully.", "success")
    return redirect(url_for("client_detail", client_id=client["id"]))
