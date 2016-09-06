import json
from nodes import *

def parse(text):
	data = json.loads(text)
	idmap = {}
	if "node" in data:
		node = convert_node(data["node"], idmap)
	else:
		node = None
	
	edges = []
	if "edges" in data:
		for edge in data["edges"]:
			new_edge = convert_edge(edge, idmap)
			edges.append(new_edge)
	return {"node": node, "edges": edges}
	
def convert_node(node, idmap):
	if node["type"] == "box":
		assert "id" in node and "label" in node
		node = BoxNode(node["id"], node["label"])
		assert node.id not in idmap
		idmap[node.id] = node
	elif node["type"] == "cluster":
		assert "id" in node and "children" in node
		children = [convert_node(n, idmap) for n in node["children"]]
		node = ClusterNode(node["id"], children)
		idmap[node.id] = node
	elif node["type"] == "repeat":
		assert "id" in node and "child" in node and "count" in node
		child = convert_node(node["child"], idmap)
		node = RepeatedClusterNode(node["id"], child, node["count"])
		idmap[node.id] = node
	elif node["type"] == "layer":
		children = [convert_node(n, idmap) for n in node["children"]]
		node = LayerNode(node["id"], children)
		idmap[node.id] = node
	elif node["type"] == "container":
		assert "id" in node and "child" in node
	 	child = convert_node(node["child"], idmap)
		label = node["label"] if "label" in node else None
		node = ContainerNode(node["id"], child, label)
		idmap[node.id] = node
	return node

def convert_edge(edge, idmap):
	assert "src" in edge and "dst" in edge
	edge_node = EdgeNode(idmap[edge["src"]], idmap[edge["dst"]])
	return edge_node

	
