from flask import Blueprint, render_template, request, redirect, session
from config import get_db_connection

user_bp = Blueprint('user', __name__)

# ---------------- REGISTER ----------------
@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO users (name, email, phone, password)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (name, email, phone, password))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGIN ----------------
@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM users WHERE email=%s AND password=%s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session["user_id"] = user["user_id"]
            session["user_name"] = user["name"]
            return redirect("/dashboard")
        else:
            return "Invalid Credentials"

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@user_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    return f"Welcome {session['user_name']} | <a href='/logout'>Logout</a>"


# ---------------- ADD VEHICLE ----------------
@user_bp.route("/add_vehicle", methods=["GET", "POST"])
def add_vehicle():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        vehicle_number = request.form["vehicle_number"]
        vehicle_type = request.form["vehicle_type"]
        model = request.form["model"]

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO vehicles (user_id, vehicle_number, vehicle_type, model)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (session["user_id"], vehicle_number, vehicle_type, model))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/view_vehicles")

    return render_template("add_vehicle.html")


# ---------------- VIEW VEHICLES ----------------
@user_bp.route("/view_vehicles")
def view_vehicles():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM vehicles WHERE user_id=%s"
    cursor.execute(query, (session["user_id"],))
    vehicles = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("view_vehicles.html", vehicles=vehicles)


# ---------------- LOGOUT ----------------
@user_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
