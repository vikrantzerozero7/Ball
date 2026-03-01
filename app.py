# app_expandable.py
import streamlit as st
import networkx as nx
from pyvis.network import Network
import tempfile
import os

st.set_page_config(page_title="Ontology Explorer", layout="wide")
st.title("Ontology Explorer with Expand/Collapse")

# ------------------------
# Sample Ontology Data
# ------------------------
ontology = {
    "Person": {
        "instances": ["V N", "Arya"],
        "properties": {"hasAge": [25, 30], "hasRole": ["Student", "Teacher"]}
    },
    "Car": {
        "instances": ["Tesla Model 3", "Toyota Corolla"],
        "properties": {"isElectric": [True, False], "owner": ["V N", "Arya"]}
    }
}

# ------------------------
# Sidebar for Class Selection
# ------------------------
st.sidebar.header("Select Ontology Class")
selected_class = st.sidebar.selectbox("Class", list(ontology.keys()))

# ------------------------
# Expandable Tree View
# ------------------------
st.subheader(f"Ontology Tree for '{selected_class}'")

class_info = ontology[selected_class]

for i, instance in enumerate(class_info["instances"]):
    with st.expander(f"Instance: {instance}"):
        st.write("Properties:")
        for prop, values in class_info["properties"].items():
            st.write(f"- {prop}: {values[i]}")

# ------------------------
# Visualize Ontology as Graph
# ------------------------
st.subheader("Ontology Graph Visualization")

# Create Graph
G = nx.DiGraph()
G.add_node(selected_class, color='lightblue', size=30)

for i, instance in enumerate(class_info["instances"]):
    G.add_node(instance, color='lightgreen', size=20)
    G.add_edge(selected_class, instance, label="instanceOf")
    for prop, values in class_info["properties"].items():
        prop_node = f"{prop}: {values[i]}"
        G.add_node(prop_node, color='orange', size=15)
        G.add_edge(instance, prop_node, label=prop)

# Pyvis network
net = Network(height="600px", width="100%", directed=True)
net.from_nx(G)
net.repulsion(node_distance=150, central_gravity=0.2)

# Save to temporary HTML file
tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
net.save_graph(tmp_file.name)

# Display in Streamlit
HtmlFile = open(tmp_file.name, 'r', encoding='utf-8')
components_html = HtmlFile.read()
st.components.v1.html(components_html, height=650)
HtmlFile.close()
os.unlink(tmp_file.name)
