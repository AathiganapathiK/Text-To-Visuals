import json
from rake_nltk import Rake
from nlp.nlp_loader import nlp, stop_words
from utils.graph_builder import build_nodes_edges
from config.settings import co

def generate_mindmap_service(text):
    rake = Rake(stopwords=stop_words)
    rake.extract_keywords_from_text(text)

    prompt = f"""
Convert text to mindmap JSON:
{text}
"""

    try:
        response = co.chat(model="command-xlarge-nightly", message=prompt)
        ai_json = json.loads(response.text)
    except Exception:
        ai_json = {
            "root": "Main Topic",
            "children": [{"label": k, "subchildren": []} for k in rake.get_ranked_phrases()[:3]]
        }

    return build_nodes_edges(ai_json)
