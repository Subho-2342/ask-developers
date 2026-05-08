from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os

app = Flask(__name__)

# SECRET KEY
app.secret_key = "askdeveloperssecret"

# ===============================
# UPLOAD FOLDER
# ===============================

UPLOAD_FOLDER = 'static/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# AUTO CREATE uploads FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ===============================
# MYSQL CONNECTION
# ===============================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ask_developers"
)

cursor = db.cursor(dictionary=True)

# ===============================
# HOME PAGE
# ===============================

@app.route("/")
def home():

    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()

    return render_template(
        "index.html",
        projects=projects
    )

# ===============================
# ADMIN LOGIN PAGE
# ===============================

@app.route("/admin-login")
def admin_login():
    return render_template("login.html")

# ===============================
# LOGIN CHECK
# ===============================

@app.route("/login", methods=["POST"])
def login():

    username = request.form.get("username")
    password = request.form.get("password")

    print(username)
    print(password)

    sql = """
    SELECT * FROM admin
    WHERE username=%s AND password=%s
    """

    values = (username, password)

    cursor.execute(sql, values)

    admin = cursor.fetchone()

    print(admin)

    if admin:

        session["admin"] = username

        return redirect("/admin")

    return "Invalid Username or Password"

# ===============================
# ADMIN PAGE
# ===============================

@app.route("/admin")
def admin():

    if "admin" not in session:
        return redirect("/admin-login")

    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()

    return render_template(
        "admin.html",
        projects=projects
    )

# ===============================
# ADD PROJECT
# ===============================

@app.route("/add-project", methods=["POST"])
def add_project():

    if "admin" not in session:
        return redirect("/admin-login")

    company_name = request.form.get("company_name")
    project_type = request.form.get("project_type")
    description = request.form.get("description")
    category = request.form.get("category")

    image = request.files.get("image")

    filename = ""

    # SAVE IMAGE
    if image and image.filename != "":

        filename = image.filename

        image_path = os.path.join(
            app.config['UPLOAD_FOLDER'],
            filename
        )

        image.save(image_path)

    # INSERT INTO DATABASE
    sql = """
    INSERT INTO projects
    (company_name, project_type, description, image, category)

    VALUES (%s,%s,%s,%s,%s)
    """

    values = (
        company_name,
        project_type,
        description,
        filename,
        category
    )

    cursor.execute(sql, values)
    db.commit()

    return redirect("/")

# ===============================
# DELETE PROJECT
# ===============================

@app.route("/delete-project/<int:id>")
def delete_project(id):

    if "admin" not in session:
        return redirect("/admin-login")

    # GET IMAGE NAME
    cursor.execute(
        "SELECT image FROM projects WHERE id=%s",
        (id,)
    )

    project = cursor.fetchone()

    # DELETE IMAGE FILE
    if project:

        image_path = os.path.join(
            app.config['UPLOAD_FOLDER'],
            project["image"]
        )

        if os.path.exists(image_path):
            os.remove(image_path)

    # DELETE DB DATA
    cursor.execute(
        "DELETE FROM projects WHERE id=%s",
        (id,)
    )

    db.commit()

    return redirect("/admin")

# ===============================
# LOGOUT
# ===============================

@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect("/admin-login")

# ===============================
# RUN APP
# ===============================

if __name__ == "__main__":
    app.run(debug=True)