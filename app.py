from flask import Flask, send_from_directory, request, jsonify
import xml.etree.ElementTree as ET
import os

# Initialize the Flask application
app = Flask(__name__)

# Determine the absolute path to the directory containing app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load common passwords from XML file into a set for fast lookup
xml_path = os.path.join(BASE_DIR, "common_passwords.xml")
tree = ET.parse(xml_path)
root = tree.getroot()
common_passwords = {p.text for p in root.findall("password")}

# Route to serve the main HTML page
@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")

# API route to evaluate password strength
@app.route("/check_password", methods=["POST"])
def check_password():
    data = request.get_json()
    password = data.get("password", "")

    # Return default response if no password is provided
    if not password:
        return jsonify({"score": 0, "status": "", "is_common": False})

    # Block passwords shorter than 6 characters
    if len(password) <= 5:
        return jsonify({
            "score": 0,
            "status": "Password too short, it must be longer than 5 characters",
            "is_common": False
        })

    # Check if the password is in the common password list
    is_common = password in common_passwords

    if is_common:
        return jsonify({
            "score": 0,
            "status": "This password is one of the 20 most commonly used in 2026 "
                      "and is not secure! Please choose a stronger, unique password",
            "is_common": True
        })

    # Calculate password strength score and textual status
    score = calculate_score(password)
    status = calculate_status(score)
    return jsonify({"score": score, "status": status, "is_common": False})

# Compute a numerical score for the password
# Factors: length, character variety, repeated characters, common patterns
def calculate_score(password):
    score = 0
    length = len(password)

    # Reward for length
    if length >= 8: score += 10
    if length >= 14: score += 25
    if length >= 20: score += 20

    # Reward for character variety
    if any(c.islower() for c in password): score += 10
    if any(c.isupper() for c in password): score += 10
    if any(c.isdigit() for c in password): score += 10
    if any(not c.isalnum() for c in password): score += 15

    # Penalize repeated consecutive characters
    if any(password[i] == password[i+1] == password[i+2] for i in range(len(password)-2)): score -= 20

    # Penalize common sequences and patterns
    if any(pat in password.lower() for pat in ["123", "abc", "qwerty", "password", "admin"]): score -= 25

    # Ensure score is between 0 and 100
    return max(0, min(100, score))

# Translate numerical score into a human-readable status
def calculate_status(score):
    if score < 20: return "Very weak"
    elif score < 40: return "Weak"
    elif score < 60: return "Moderate"
    elif score < 80: return "Strong"
    else: return "Very strong"

# Run the Flask development server
if __name__ == "__main__":
    app.run(debug=True)