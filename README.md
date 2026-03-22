# SQL Injection Demo — Fake CCP Login Page

> **For educational use only.** This app is intentionally vulnerable. Don't deploy it publicly or use it on real systems.

---

## What is this?

A fake Algerian CCP (postal account) login page built with Flask and SQLite, made to demonstrate two common web security issues:

- **SQL Injection** — user input goes directly into a SQL query, no sanitization
- **Credential harvesting** — every login attempt gets saved to the database before it's even validated

I built this to understand how these attacks actually work at the code level, not just theoretically.

---

## The vulnerability

In the `/verify` route, the login query looks like this:

```python
cur.execute(f"SELECT * FROM users WHERE ccp_code = '{code}' AND password = '{password}'")
```

Try logging in with `' OR '1'='1` as the password. It works — because the query becomes:

```sql
SELECT * FROM users WHERE ccp_code = '...' AND password = '' OR '1'='1'
```

The fix is simple — use parameterized queries:

```python
cur.execute("SELECT * FROM users WHERE ccp_code = ? AND password = ?", (code, password))
```

---

## Running it locally

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

pip install -r requirements.txt
python init_db.py   # sets up the database and adds test users
python app.py
```

Then open `http://127.0.0.1:5000`.

**Test credentials:** any of the CCP codes in `init_db.py` with password `pwd`.  
**To test SQL injection:** any CCP code + `' OR '1'='1` as the password.

---

## Project structure

```
├── app.py            # Flask app with the vulnerable routes
├── init_db.py        # Creates the database and seeds test users
├── requirements.txt
└── templates/
    └── phishing.html # The fake login page
```

---

## Disclaimer

This was made for learning purposes. Don't use it on real systems or real users.

If you want to go deeper: [PortSwigger SQL Injection Labs](https://portswigger.net/web-security/sql-injection) are great for hands-on practice.
