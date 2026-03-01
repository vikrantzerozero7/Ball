import streamlit as st
from streamlit_option_menu import option_menu
import json

class OntologyNode:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children if children else []
        self.expanded = False

def create_ontology_structure():
    """Create a sample ontology structure"""
    return {
        "Thing": OntologyNode("Thing", [
            OntologyNode("Physical Object", [
                OntologyNode("Living Thing", [
                    OntologyNode("Animal"),
                    OntologyNode("Plant")
                ]),
                OntologyNode("Non-living Thing", [
                    OntologyNode("Mineral"),
                    OntologyNode("Artifact")
                ])
            ]),
            OntologyNode("Abstract Entity", [
                OntologyNode("Idea"),
                OntologyNode("Concept", [
                    OntologyNode("Mathematical Concept"),
                    OntologyNode("Philosophical Concept")
                ])
            ])
        ])
    }

def render_interactive_ontology(node_dict, level=0):
    """Render interactive ontology with toggle buttons"""
    for key, node in node_dict.items():
        # Create unique key for each node
        node_key = f"node_{key}_{level}_{id(node)}"
        
        # Create columns for layout
        cols = st.columns([1, 1, 4])
        
        with cols[0]:
            # Toggle button for expand/collapse
            if node.children:
                if st.button("▼" if node.expanded else "▶", key=f"toggle_{node_key}"):
                    node.expanded = not node.expanded
                    st.rerun()
        
        with cols[1]:
            st.write("  " * level + "•")
        
        with cols[2]:
            # Node name with styling
            st.markdown(f"**{node.name}**" if node.children else f"  {node.name}")
        
        # Render children if expanded
        if node.expanded and node.children:
            for child in node.children:
                render_interactive_ontology({child.name: child}, level + 1)

def main():
    st.set_page_config(layout="wide")
    st.title("Interactive Ontology Viewer")
    
    # Initialize ontology in session state
    if 'ontology' not in st.session_state:
        st.session_state.ontology = create_ontology_structure()
    
    # Sidebar controls
    with st.sidebar:
        st.header("Controls")
        
        if st.button("Expand All"):
            def expand_all(node_dict):
                for node in node_dict.values():
                    node.expanded = True
                    if node.children:
                        expand_all({child.name: child for child in node.children})
            expand_all(st.session_state.ontology)
            st.rerun()
        
        if st.button("Collapse All"):
            def collapse_all(node_dict):
                for node in node_dict.values():
                    node.expanded = False
                    if node.children:
                        collapse_all({child.name: child for child in node.children})
            collapse_all(st.session_state.ontology)
            st.rerun()
        
        st.divider()
        
        # Search functionality
        st.subheader("Search")
        search_term = st.text_input("Search concepts")
        
        if search_term:
            st.info(f"Searching for: {search_term}")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Ontology Tree")
        render_interactive_ontology(st.session_state.ontology)
    
    with col2:
        st.subheader("Node Details")
        st.info("Click on nodes to see details")
        
        # Add some metadata display
        st.markdown("""
        **Legend:**
        - ▶ : Collapsed node (click to expand)
        - ▼ : Expanded node (click to collapse)
        - **Bold**: Parent node with children
        - Normal: Leaf node
        """)

if __name__ == "__main__":
    main()
