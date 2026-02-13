from flask import Flask, request, jsonify
from flask_cors import CORS

from services.mindmap_service import generate_mindmap_service
from services.flowchart_service import generate_flowchart_service

app = Flask(__name__)
CORS(app)

@app.route("/")
def health():
    return "Text2Visuals API running"

@app.route("/mindmap", methods=["POST"])
def mindmap():
    text = (request.json or {}).get("text", "").strip()
    if not text:
        return jsonify({"error": "Text required"}), 400

    nodes, edges = generate_mindmap_service(text)
    return jsonify({"nodes": nodes, "edges": edges})

@app.route("/flowchart", methods=["POST"])
def flowchart():
    data = request.json or {}
    problem = data.get("problem", "").strip()
    skill = data.get("skillLevel", "intermediate")

    if not problem:
        return jsonify({"error": "Problem required"}), 400

    nodes, edges = generate_flowchart_service(problem, skill)
    return jsonify({"nodes": nodes, "edges": edges})

if __name__ == "__main__": 
    app.run()