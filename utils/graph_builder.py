from nlp.preprocessing import clean_phrase

def build_nodes_edges(flow_json, root_time_estimate=None):
    nodes, edges = [], []
    node_id = 0

    def add_node(node, parent_id=None, depth=0):
        nonlocal node_id
        current_id = str(node_id)

        label = node if isinstance(node, str) else node.get("label", node.get("root", "Step"))
        time_estimate = node.get("timeEstimate") if isinstance(node, dict) else None

        node_obj = {
            "id": current_id,
            "label": clean_phrase(label),
            "depth": depth
        }

        if time_estimate is not None:
            node_obj["timeEstimate"] = time_estimate

        nodes.append(node_obj)

        if parent_id:
            edges.append({"from": parent_id, "to": current_id})

        node_id += 1

        children = []
        if isinstance(node, dict):
            children = node.get("children") or node.get("subchildren") or []

        for child in children:
            add_node(child, current_id, depth + 1)

    add_node(flow_json)
    return nodes, edges
