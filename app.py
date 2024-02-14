from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)

OPEN5E_API_URL = "https://api.open5e.com/v1"
app.secret_key = "testsecret"


def initialize_character():
    character = {"race": None, "class": None, "background": None}
    return character


def update_character(character, key, value):
    try:
        character[key] = value
    except:
        pass


@app.route("/")
def index():
    new_character = initialize_character()
    session["new_character"] = new_character
    return render_template("index.html")


@app.route("/races", methods=["GET", "POST"])
def races():
    if request.method == "POST":
        # Handle form submission
        try:
            race_name = request.form["race"]
        except:
            error_message = "Error: Please select an option"
            response = requests.get(f"{OPEN5E_API_URL}/races/")
            races_data = response.json()["results"]
            races = [race["name"] for race in races_data]
            return render_template(
                "races.html", races=races, error_message=error_message
            )
        character = session.get("new_character")
        update_character(character, "race", race_name)
        session["new_character"] = character
        selection = race_name
        selection_page = "races"
        next_page = "classes"
        url = "choice_review"
        return redirect(
            url_for(
                url,
                selection=selection,
                selection_page=selection_page,
                next_page=next_page,
            )
        )

    # Fetch list of races from Open5e API
    response = requests.get(f"{OPEN5E_API_URL}/races/")
    races_data = response.json()["results"]
    races = [race["name"] for race in races_data]

    return render_template("races.html", races=races)


@app.route("/classes", methods=["GET", "POST"])
def classes():
    if request.method == "POST":
        # Handle form submission
        try:
            class_name = request.form["class_"]
        except:
            error_message = "Error: Please select an option"
            response = requests.get(f"{OPEN5E_API_URL}/classes/")
            classes_data = response.json()["results"]
            classes = [class_["name"] for class_ in classes_data]
            return render_template(
                "classes.html", classes=classes, error_message=error_message
            )
        character = session.get("new_character")
        update_character(character, "class", class_name)
        session["new_character"] = character
        selection = class_name
        selection_page = "classes"
        next_page = "backgrounds"
        url = "choice_review"
        return redirect(
            url_for(
                url,
                selection=selection,
                selection_page=selection_page,
                next_page=next_page,
            )
        )

    # Fetch list of classes from Open5e API
    response = requests.get(f"{OPEN5E_API_URL}/classes/")
    classes_data = response.json()["results"]
    classes = [class_["name"] for class_ in classes_data]

    return render_template("classes.html", classes=classes)


@app.route("/backgrounds", methods=["GET", "POST"])
def backgrounds():
    if request.method == "POST":
        # Handle form submission
        try:
            background_name = request.form["background"]
        except:
            error_message = "Error: Please select an option"
            response = requests.get(f"{OPEN5E_API_URL}/backgrounds/")
            backgrounds_data = response.json()["results"]
            backgrounds = [background["name"] for background in backgrounds_data]
            return render_template(
                "backgrounds.html", backgrounds=backgrounds, error_message=error_message
            )
        character = session.get("new_character")
        update_character(character, "background", background_name)
        session["new_character"] = character
        selection = background_name
        selection_page = "backgrounds"
        next_page = "review"
        url = "choice_review"
        return redirect(
            url_for(
                url,
                selection=selection,
                selection_page=selection_page,
                next_page=next_page,
            )
        )

    # Fetch list of backgrounds from Open5e API
    response = requests.get(f"{OPEN5E_API_URL}/backgrounds/")
    backgrounds_data = response.json()["results"]
    backgrounds = [background["name"] for background in backgrounds_data]

    return render_template("backgrounds.html", backgrounds=backgrounds)


@app.route("/choice_review/<selection>/<selection_page>/<next_page>")
def choice_review(selection, selection_page, next_page):
    # Fetch details of selection and display them for confirmation
    return render_template(
        "choice_review.html",
        selection=selection,
        selection_page=f"/{selection_page}",
        next_page=f"/{next_page}",
    )


@app.route("/description/<category>/<selection>")
def description(category, selection):
    # Retrieve description data from Open5e API based on the selected category and selection
    response = requests.get(f"{OPEN5E_API_URL}/{category}/")
    if response.status_code == 200:
        data = response.json()["results"]
        for result in data:
            if result["name"] == selection:
                description = result["desc"]
        return render_template(
            "description.html",
            category=category,
            selection=selection,
            description=description,
        )
    else:
        return f"Error: Unable to retrieve description for {selection} in category {category}"


@app.route("/review")
def character_review():
    # Fetch details of selected race, class, and background
    character = session.get("new_character")
    race = character["race"]
    class_ = character["class"]
    background = character["background"]

    return render_template(
        "review.html", race=race, class_=class_, background=background
    )


if __name__ == "__main__":
    app.run(debug=True)
