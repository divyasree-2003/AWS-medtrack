from flask import Flask, render_template, request, redirect, url_for, session, flash
import json, os

app = Flask(__name__)
app.secret_key = "your_secret_key"

USER_FILE = "users.json"

# Load users from file
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

# Save users to file
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about-us")
def aboutus():
    return render_template("aboutus.html")

@app.route("/contact-us", methods=["GET", "POST"])
def contactus():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        return render_template("thankyou.html", name=name)
    return render_template("contactus.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    users = {}  # or load_users() if you're using a file
    if request.method == "POST":
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not fullname or not email or not password or not confirm_password:
            flash("All fields are required.")
            return redirect(url_for("signup"))

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("signup"))

        # Save user if needed
        flash("Signup successful! Please login.")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Accept any email and password
        session["user"] = email.split('@')[0].capitalize()
        return redirect(url_for("dashboard"))

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])

@app.route("/create-appointment", methods=["GET", "POST"])
def create_appointment():
    if "user" not in session:
        flash("Please log in to book an appointment.")
        return redirect(url_for("login"))

    if request.method == "POST":
        doctor = request.form.get("doctor")
        date = request.form.get("date")
        time = request.form.get("time")
        symptoms = request.form.get("symptoms")
        return render_template("appointment_status.html", doctor=doctor, date=date, time=time, symptoms=symptoms)

    return render_template("appointment.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
