from flask import Flask, render_template

app = Flask(__name__)

# LOGIN

@app.route("/")
def inicio():
    return render_template("login.html")

# PANEL ADMINISTRADOR

@app.route("/admin")
def admin():
    return render_template("admin.html")

# PANEL DOCTOR

@app.route("/doctor")
def doctor():
    return render_template("doctor.html")

# PANEL ENFERMERO

@app.route("/enfermero")
def enfermero():
    return render_template("enfermero.html")


# EJECUTAR SERVIDOR

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )