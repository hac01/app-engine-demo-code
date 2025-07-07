from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = "change_this_secret_key"

login_manager = LoginManager()
login_manager.login_view = "unauthorized"
login_manager.init_app(app)

# Dummy internal employee directory
EMPLOYEES = {
    "ayush@shopgigantic.com": {"name": "Ayush Singh", "role": "Security Analyst"},
    "samir@shopgigantic.com": {"name": "Samir Amin", "role": "DevOps"},
    "jason@shopgigantic.com": {"name": "Jason Smith", "role": "Product Manager"},
}

class User(UserMixin):
    def __init__(self, email):
        self.id = email
        self.name = EMPLOYEES[email]["name"]
        self.role = EMPLOYEES[email]["role"]

@login_manager.user_loader
def load_user(user_id):
    if user_id in EMPLOYEES:
        return User(user_id)
    return None

@app.before_request
def auto_login_from_iap():
    if not current_user.is_authenticated:
        user_email = request.headers.get("X-Goog-Authenticated-User-Email")
        if user_email:
            email = user_email.split(":")[-1]  # Strip "accounts.google.com:"
            if email in EMPLOYEES:
                user = User(email)
                login_user(user)

@app.route("/")
#@login_required
def index():
    return redirect("/dashboard")

@app.route("/dashboard")
#@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

@app.route("/team")
#@login_required
def team():
    return render_template("team.html", employees=EMPLOYEES)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("unauthorized"))

@app.route("/unauthorized")
def unauthorized():
    return render_template("login.html"), 403

if __name__ == "__main__":
    app.run(debug=True)
