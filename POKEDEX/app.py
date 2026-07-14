from flask import Flask, render_template, request
import pypokedex

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    pokemon = None

    if request.method == "POST":
        name = request.form["pokemon"]

        try:
            pokemon = pypokedex.get(name=name.lower())
        except:
            pokemon = None

    return render_template("home.html", pokemon=pokemon)


if __name__ == "__main__":
    app.run(debug=True)