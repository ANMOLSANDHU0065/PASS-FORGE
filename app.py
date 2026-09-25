from flask import Flask, render_template, request, jsonify
import secrets
import string
import json
import os


app = Flask(__name__)

DATA_FILE = "password.json"

# SANDHU
# ---------------------------------------
# LOAD PASSWORD HISTORY
# ---------------------------------------

def load_history():

    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return []
# SANDHU

# ---------------------------------------
# SAVE PASSWORD HISTORY
# ---------------------------------------

def save_history(history):

    with open(DATA_FILE, "w", encoding="utf-8") as file:

        json.dump(
            history,
            file,
            indent=4
        )


# ---------------------------------------
# PASSWORD GENERATOR
# ---------------------------------------

def generate_password(
    length,
    use_uppercase,
    use_lowercase,
    use_numbers,
    use_symbols
):

    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    numbers = string.digits
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    selected = ""

    required = []


    # Select character groups

    if use_uppercase:
        selected += uppercase
        required.append(secrets.choice(uppercase))


    if use_lowercase:
        selected += lowercase
        required.append(secrets.choice(lowercase))

# ANMOL SANHDU
    if use_numbers:
        selected += numbers
        required.append(secrets.choice(numbers))


    if use_symbols:
        selected += symbols
        required.append(secrets.choice(symbols))


    # Nothing selected

    if not selected:

        raise ValueError(
            "Select at least one character type."
        )


    # Length check

    if length < len(required):

        raise ValueError(
            "Password length is too short for the selected options."
        )


    # Fill remaining characters

    while len(required) < length:

        required.append(
            secrets.choice(selected)
        )


    # Secure shuffle

    secrets.SystemRandom().shuffle(required)


    return "".join(required)


# ---------------------------------------
# PASSWORD STRENGTH
# ---------------------------------------

def check_strength(password):

    score = 0


    if len(password) >= 8:
        score += 1

    if len(password) >= 12:
        score += 1

    if len(password) >= 16:
        score += 1

    if any(char.isupper() for char in password):
        score += 1

    if any(char.islower() for char in password):
        score += 1

    if any(char.isdigit() for char in password):
        score += 1

    if any(not char.isalnum() for char in password):
        score += 1


    if score <= 2:

        return {
            "level": "Weak",
            "percentage": 30
        }
# ALL LOVE ANMOL SANDHUH

    elif score <= 4:

        return {
            "level": "Medium",
            "percentage": 60
        }


    else:

        return {
            "level": "Strong",
            "percentage": 100
        }


# ---------------------------------------
# HOME PAGE
# ---------------------------------------

@app.route("/")
def home():

    return render_template("index.html")


# ---------------------------------------
# GENERATE PASSWORD API
# ---------------------------------------

@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json()
# SANDHU

    try:

        length = int(data.get("length", 16))

        use_uppercase = bool(
            data.get("uppercase", True)
        )

        use_lowercase = bool(
            data.get("lowercase", True)
        )

        use_numbers = bool(
            data.get("numbers", True)
        )

        use_symbols = bool(
            data.get("symbols", True)
        )


        # Keep allowed range

        if length < 4 or length > 30:

            return jsonify({
                "success": False,
                "error":
                    "Password length must be between 4 and 30."
            }), 400


        password = generate_password(
            length,
            use_uppercase,
            use_lowercase,
            use_numbers,
            use_symbols
        )


        strength = check_strength(password)


        # Save history

        history = load_history()

        history.append({
            "length": len(password),
            "strength": strength["level"]
        })


        save_history(history)

# SANDHU
        return jsonify({

            "success": True,

            "password": password,

            "strength": strength["level"],

            "percentage":
                strength["percentage"]

        })


    except ValueError as error:

        return jsonify({

            "success": False,

            "error": str(error)

        }), 400


# ---------------------------------------
# STATISTICS API
# ---------------------------------------

@app.route("/stats")
def stats():

    history = load_history()


    return jsonify({

        "total_generated":
            len(history),

        "last_length":
            history[-1]["length"]
            if history else 0,

        "last_strength":
            history[-1]["strength"]
            if history else "None"

    })

# SANDHU
# ---------------------------------------
# RUN SERVER
# ---------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )


