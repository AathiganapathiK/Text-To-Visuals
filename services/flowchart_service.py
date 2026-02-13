import json
from nlp.nlp_loader import nlp
from utils.graph_builder import build_nodes_edges
from services.time_estimator import estimate_step_duration
from config.settings import co

def generate_flowchart_service(problem, skill_level):
    prompt = f"""
Convert problem to flowchart JSON:
{problem}
"""

    try:
        response = co.chat(model="command-xlarge-nightly", message=prompt)
        ai_json = json.loads(response.text)
    except Exception:
        ai_json = {"root": "Start", "children": []}

    def add_time(node):
        if isinstance(node, dict):
            node["timeEstimate"] = estimate_step_duration(node.get("label", ""), skill_level)
            for k in ("children", "subchildren"):
                for c in node.get(k, []):
                    add_time(c)
        return node

    ai_json = add_time(ai_json)
    return build_nodes_edges(ai_json)
