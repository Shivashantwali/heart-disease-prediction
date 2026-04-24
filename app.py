from flask import Flask, render_template, request, redirect, url_for, session
import pickle
import numpy as np

app = Flask(__name__)
app.secret_key = "secret123"

model = pickle.load(open("heart_model.pkl", "rb"))

# USERS
users = {
    "admin": "1234",
    "shivashant": "wali@1234"
}

# LOGIN
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


# LOGOUT
@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


# MAIN
@app.route("/", methods=["GET","POST"])
def index():
    if "user" not in session:
        return redirect(url_for("login"))

    result = None
    risk = 0
    data = []

    if request.method == "POST":
        try:
            data = [
                int(request.form["age"]),
                int(request.form["sex"]),
                int(request.form["cp"]),
                int(request.form["trestbps"]),
                int(request.form["chol"]),
                int(request.form["fbs"]),
                int(request.form["restecg"]),
                int(request.form["thalach"]),
                int(request.form["exang"]),
                float(request.form["oldpeak"]),
                int(request.form["slope"]),
                int(request.form["ca"]),
                int(request.form["thal"])
            ]

            final_data = np.array([data])
            prediction = model.predict(final_data)[0]

            try:
                prob = model.predict_proba(final_data)[0][1]
                risk = round(prob * 100, 2)
            except:
                risk = 50

            if prediction == 1:
                result = f"⚠️ High Risk ({risk}%)"
            else:
                result = f"✅ Low Risk ({risk}%)"

        except:
            result = "❌ Error in input"

    return render_template(
        "index.html",
        prediction_text=result,
        risk=risk,
        data=data
    )


if __name__ == "__main__":
    app.run(debug=True)