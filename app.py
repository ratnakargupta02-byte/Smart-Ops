import os
import requests
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GITHUB_REPO = "ratnakargupta02-byte/Smart-Ops"


@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "dashboard.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/api/deployments")
def deployments():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/commits"

    try:
        response = requests.get(
            url,
            headers={"Accept": "application/vnd.github+json"},
            timeout=10
        )
        response.raise_for_status()

        commits = response.json()[:10]

        history = []

        for commit in commits:
            history.append({
                "message": commit["commit"]["message"],
                "date": commit["commit"]["author"]["date"],
                "author": commit["commit"]["author"]["name"],
                "url": commit["html_url"]
            })

        return jsonify({
            "repository": GITHUB_REPO,
            "total": len(history),
            "deployments": history
        })

    except requests.RequestException:
        return jsonify({
            "error": "Unable to fetch GitHub history"
        }), 502


@app.route("/api/status")
def status():
    return jsonify({
        "application": "Smart Ops",
        "status": "running",
        "health": "healthy",
        "deployment_platform": "Render",
        "container_platform": "Docker"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )