from flask import Flask, render_template, request
import requests
import pypokedex

app = Flask(__name__)

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
def get_description(dex):

    url = f"https://pokeapi.co/api/v2/pokemon-species/{dex}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        for entry in data["flavor_text_entries"]:
            if entry["language"]["name"] == "en":
                return entry["flavor_text"].replace("\n", " ").replace("\f", " ")

    return "No description available."
@app.route("/", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def home():

    print("HOME FUNCTION CALLED")

    pokemon = None
    pokemon_list = []
    header_style = ""
    description = ""

    if request.method == "POST":

        action = request.form["action"]

        if action == "search":

            name = request.form["pokemon"]
            print("Searching for:", name)

            try:
                pokemon = pypokedex.get(name=name.lower())
                print("Pokemon found:", pokemon.name)

                description = get_description(pokemon.dex)
                print("Description:", description[:50])

                color1 = TYPE_COLORS[pokemon.types[0].lower()]

                if len(pokemon.types) > 1:
                    color2 = TYPE_COLORS[pokemon.types[1].lower()]
                else:
                    color2 = color1

                header_style = (
                    f"background: linear-gradient(135deg, {color1}, {color2});"
                )

                print("Header Style:", header_style)
                print("Render successful!")

            except Exception as e:
                print("ERROR:", e)
                raise

        elif action == "all":

            print("Loading all Pokémon...")

            for dex in range(1, 152):
                pokemon_list.append(
                    pypokedex.get(dex=dex)
                )

            print(f"Loaded {len(pokemon_list)} Pokémon.")

    return render_template(
        "home.html",
        pokemon=pokemon,
        pokemon_list=pokemon_list,
        header_style=header_style,
        description=description
    )

if __name__ == "__main__":
    app.run(debug=True)