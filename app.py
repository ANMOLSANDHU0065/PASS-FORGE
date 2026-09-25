from flask import Flask, render_template, request, jsonify, session
import secrets
import string
import os

app = Flask(__name__)

# Session security key
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "pass-forge-demo-secret-key"
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

    try:

        length = int(
            data.get("length", 16)
        )

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

        # ---------------------------------------
        # PER-USER SESSION COUNTER
        # ---------------------------------------

        current_count = session.get(
            "total_generated",
            0
        )

        session["total_generated"] = (
            current_count + 1
        )

        session["last_length"] = len(password)

        session["last_strength"] = strength["level"]

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

    total_generated = session.get(
        "total_generated",
        0
    )

    last_length = session.get(
        "last_length",
        0
    )

    last_strength = session.get(
        "last_strength",
        "None"
    )

    return jsonify({

        "total_generated":
            total_generated,

        "last_length":
            last_length,

        "last_strength":
            last_strength

    })


# ---------------------------------------
# RUN SERVER
# ---------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )