from db import get_db

def get_all_clients():
    db = get_db()
    return db.execute("SELECT * FROM clients ORDER BY name").fetchall()

def get_clients_with_project_counts():
    db = get_db()

    return db.execute("SELECT clients.*, COUNT(projects.id) AS project_count FROM clients LEFT JOIN projects ON clients.id = projects.client_id GROUP BY clients.id ORDER BY clients.name").fetchall()

def get_client_by_id(client_id):
    db = get_db()
    return db.execute("SELECT * FROM clients WHERE id = ?", (client_id,)).fetchone()

def get_all_projects():
    db = get_db()
    return db.execute("SELECT projects.*, clients.name AS client_name FROM projects JOIN clients ON projects.client_id = clients.id ORDER BY projects.due_date").fetchall()

def get_dashboard_data():
    db = get_db()

    # Fech total clients
    total_clients = db.execute("SELECT COUNT(*) AS total FROM clients").fetchone()["total"]

    # Fetch total projects
    total_projects = db.execute("SELECT COUNT(*) AS total FROM projects").fetchone()["total"]

    # Fetch projects by status
    status_count = db.execute("SELECT status, COUNT(*) AS count FROM projects GROUP BY status").fetchall()

    completed = in_progress = pending = 0
    for row in status_count:
        if row["status"] == "Completed":
            completed = row["count"]
        elif row["status"] == "In Progress":
            in_progress = row["count"]
        elif row["status"] == "Pending":
            pending = row["count"]

    # Upcoming projects (next 7 days)
    upcoming_projects = db.execute("SELECT projects.id, projects.name, projects.client_id, projects.due_date, projects.status, clients.name AS client_name FROM projects JOIN clients ON projects.client_id = clients.id WHERE projects.due_date IS NOT NULL AND projects.due_date != '' ORDER BY projects.due_date ASC LIMIT 5").fetchall()

    # Top clients by number of projects
    top_clients = db.execute("SELECT clients.id, clients.name, clients.company, COUNT(projects.id) AS total_projects FROM clients LEFT JOIN projects ON clients.id = projects.client_id GROUP BY clients.id ORDER BY total_projects DESC LIMIT 5").fetchall()

    return {
        "total_clients": total_clients,
        "total_projects": total_projects,
        "completed": completed,
        "in_progress": in_progress,
        "pending": pending,
        "upcoming_projects": upcoming_projects,
        "top_clients": top_clients
    }