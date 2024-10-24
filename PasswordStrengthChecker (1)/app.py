
from flask import Flask, render_template, request
import re

app = Flask(__name__)

# Load common passwords list from a file
def load_common_passwords(file_path):
    with open(file_path, 'r') as file:
        return set(line.strip() for line in file)

common_passwords = load_common_passwords('common_passwords.txt')

# Check password strength
def check_password_strength(password):
    length_score = len(password) >= 8
    complexity_score = bool(re.search(r'[A-Z]', password)) and bool(re.search(r'[a-z]', password))                        and bool(re.search(r'[0-9]', password)) and bool(re.search(r'[^A-Za-z0-9]', password))
    uniqueness_score = password not in common_passwords

    if length_score and complexity_score and uniqueness_score:
        strength = "Strong"
    elif length_score and (complexity_score or uniqueness_score):
        strength = "Moderate"
    else:
        strength = "Weak"

    feedback = []
    if not length_score:
        feedback.append("Increase the length (at least 8 characters).")
    if not complexity_score:
        feedback.append("Include uppercase, lowercase letters, numbers, and special characters.")
    if not uniqueness_score:
        feedback.append("Avoid using common or easily guessable passwords.")

    return strength, feedback

@app.route("/", methods=["GET", "POST"])
def home():
    strength = None
    feedback = []
    if request.method == "POST":
        password = request.form["password"]
        strength, feedback = check_password_strength(password)
    return render_template("index.html", strength=strength, feedback=feedback)

if __name__ == "__main__":
    app.run(debug=True)
