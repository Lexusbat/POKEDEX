from flask import Flask, render_template, request
import pypokedex

TYPE_COLORS = {
    "normal": "#A8A77A",
    "fire": "#EE8130",
    "water": "#6390F0",
    "electric": "#F7D02C",
    "grass": "#7AC74C",
    "ice": "#96D9D6",
    "fighting": "#C22E28",
    "poison": "#A33EA1",
    "ground": "#E2BF65",
    "flying": "#A98FF3",
    "psychic": "#F95587",
    "bug": "#A6B91A",
    "rock": "#B6A136",
    "ghost": "#735797",
    "dragon": "#6F35FC",
    "dark": "#705746",
    "steel": "#B7B7CE",
    "fairy": "#D685AD",
}

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    pokemon = None
    header_style = ""

    if request.method == "POST":
        name = request.form["pokemon"]

        try:
            pokemon = pypokedex.get(name=name.lower())

            # Primary type colour
            color1 = TYPE_COLORS[pokemon.types[0].lower()]

            # Secondary type colour (if it exists)
            if len(pokemon.types) > 1:
                color2 = TYPE_COLORS[pokemon.types[1].lower()]
            else:
                color2 = color1

            # Build CSS gradient
            header_style = (
                f"background: linear-gradient(135deg, {color1}, {color2});"
            )
            print(header_style)

        except Exception:
            pokemon = None

    return render_template(
        "home.html",
        pokemon=pokemon,
        header_style=header_style,
    )


if __name__ == "__main__":
    app.run(debug=True)