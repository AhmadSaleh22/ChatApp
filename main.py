from flask import Flask, render_template, url_for, session, redirect

NAME_KEY = "name"

app = Flask(__name__)

app.secret_key = "hellomynameisahmadsalehfrompalestine"


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop(NAME_KEY, None)
    return redirect(url_for("login"))


@app.route("/home")
def home():
    if NAME_KEY not in session:
        return redirect(url_for("login"))

    name = session[NAME_KEY]
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
