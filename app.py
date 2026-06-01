from flask import Flask, render_template, request, redirect, session
import mysql.connector
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# SECRET KEY
app.secret_key = "askdeveloperssecret"

# ===============================
# CLOUDINARY CONFIG
# ===============================

cloudinary.config(
    cloud_name="dxmrryscc",
    api_key="645264287494442",
    api_secret="QCKA85NtFbSRUVrXZIfHU6qvoS0"
)

# ===============================
# MYSQL CONNECTION
# ===============================

def get_db():
    return mysql.connector.connect(
        host="srv1951.hstgr.io",
        user="u892008390_askdev_user",
        password="Askdev@12345",
        database="u892008390_askdev_db"
    )

# ===============================
# HOME PAGE
# ===============================

@app.route("/")
def home():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()

    db.close()

    return render_template("index.html", projects=projects)
# ===============================
# ADMIN LOGIN PAGE
# ===============================

@app.route("/admin-login")
def admin_login():
    return render_template("login.html")

# ===============================
# LOGIN CHECK
# ===============================



# ===============================
# ADMIN PAGE
# ===============================
@app.route("/admin")
def admin():
    if "admin" not in session:
        return redirect("/admin-login")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()

    db.close()

    return render_template("admin.html", projects=projects)
# ===============================
# ADD PROJECT
# ===============================

@app.route("/add-project", methods=["POST"])
def add_project():

    if "admin" not in session:
        return redirect("/admin-login")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    company_name = request.form.get("company_name")
    project_type = request.form.get("project_type")
    description = request.form.get("description")
    category = request.form.get("category")

    image = request.files.get("image")

    image_url = ""

    if image and image.filename != "":
        upload_result = cloudinary.uploader.upload(image)
        image_url = upload_result["secure_url"]

    sql = """
    INSERT INTO projects
    (company_name, project_type, description, image, category)
    VALUES (%s,%s,%s,%s,%s)
    """

    cursor.execute(sql, (
        company_name,
        project_type,
        description,
        image_url,
        category
    ))

    db.commit()
    db.close()

    return redirect("/")

# ===============================
# DELETE PROJECT
# ===============================

@app.route("/delete-project/<int:id>")
def delete_project(id):

    if "admin" not in session:
        return redirect("/admin-login")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("DELETE FROM projects WHERE id=%s", (id,))
    db.commit()
    db.close()

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