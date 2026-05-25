from flask import Flask, request, jsonify

app = Flask(__name__)

blocked_terms = [
    "social security",
    "ssn",
    "password",
    "private information",
    "another user's account",
    "credit card"
]

@app.route("/")
def home():
    return """
    <h1>Black-Box AI Monitoring Lab</h1>
    <p>Send a POST request to /analyze with a prompt.</p>
    """

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json() or {}
    prompt = data.get("prompt", "")

    blocked = any(term in prompt.lower() for term in blocked_terms)

    if blocked:
        return jsonify({
            "status": "blocked",
            "reason": "Prompt triggered AI monitoring boundary.",
            "prompt_reviewed": prompt
        }), 403

    return jsonify({
        "status": "allowed",
        "response": f"Simulated AI response for: {prompt}"
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
