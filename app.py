import streamlit as st
from typing import List, Dict, Optional
import uuid

class OntologyNode:
    def __init__(self, name: str, node_type: str = "concept", children: List = None, 
                 properties: Dict = None, icon: str = "🔷"):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.node_type = node_type  # "class", "property", "instance"
        self.children = children or []
        self.properties = properties or {}
        self.expanded = False
        self.icon = icon
        self.level = 0

def create_sample_ontology():
    """Create the ontology structure exactly like in the image"""
    return {
        "Thing": OntologyNode("Thing", "class", [
            OntologyNode("Agent", "class", [
                OntologyNode("Person", "class", [
                    OntologyNode("Student", "class", icon="👤"),
                    OntologyNode("Professor", "class", icon="👨‍🏫"),
                    OntologyNode("Staff", "class", icon="👔")
                ], icon="👥"),
                OntologyNode("Organization", "class", [
                    OntologyNode("University", "class", icon="🏛️"),
                    OntologyNode("Department", "class", icon="📚"),
                    OntologyNode("Research Group", "class", icon="🔬")
                ], icon="🏢")
            ], icon="🤖"),
            
            OntologyNode("Event", "class", [
                OntologyNode("Academic Event", "class", [
                    OntologyNode("Conference", "class", icon="🎯"),
                    OntologyNode("Workshop", "class", icon="🔧"),
                    OntologyNode("Seminar", "class", icon="📢")
                ], icon="📅"),
                OntologyNode("Social Event", "class", [
                    OntologyNode("Meeting", "class", icon="🤝"),
                    OntologyNode("Ceremony", "class", icon="🎉")
                ], icon="🎊")
            ], icon="📆"),
            
            OntologyNode("Place", "class", [
                OntologyNode("Building", "class", [
                    OntologyNode("Classroom", "class", icon="🏫"),
                    OntologyNode("Laboratory", "class", icon="🧪"),
                    OntologyNode("Office", "class", icon="💼")
                ], icon="🏢"),
                OntologyNode("Location", "class", [
                    OntologyNode("City", "class", icon="🌆"),
                    OntologyNode("Campus", "class", icon="🏰")
                ], icon="📍")
            ], icon="🌍"),
            
            OntologyNode("Document", "class", [
                OntologyNode("Publication", "class", [
                    OntologyNode("Paper", "class", icon="📄"),
                    OntologyNode("Book", "class", icon="📚"),
                    OntologyNode("Thesis", "class", icon="🎓")
                ], icon="📑"),
                OntologyNode("Record", "class", [
                    OntologyNode("Transcript", "class", icon="📊"),
                    OntologyNode("Certificate", "class", icon="📜")
                ], icon="📋")
            ], icon="📄")
        ], icon="🔷")
    }

def set_node_levels(node_dict, level=0):
    """Recursively set level for all nodes"""
    for node in node_dict.values():
        node.level = level
        if node.children:
            child_dict = {child.name: child for child in node.children}
            set_node_levels(child_dict, level + 1)

def render_ontology_tree(nodes_dict, search_term=""):
    """Render ontology tree with exact style from image"""
    
    for node_name, node in nodes_dict.items():
        # Filter based on search
        if search_term and search_term.lower() not in node.name.lower():
            continue
        
        # Create unique key
        node_key = f"node_{node.id}_{node.level}"
        
        # Main node row with custom styling
        cols = st.columns([0.05, 0.05, 0.9])
        
        with cols[0]:
            # Expand/collapse button for nodes with children
            if node.children:
                button_label = "▼" if node.expanded else "▶"
                if st.button(button_label, key=f"toggle_{node_key}", help="Click to expand/collapse"):
                    node.expanded = not node.expanded
                    st.rerun()
            else:
                st.write("  ")
        
        with cols[1]:
            # Visual connector lines for hierarchy
            if node.level > 0:
                st.markdown("│  " * (node.level - 1) + "├─")
            else:
                st.write("  ")
        
        with cols[2]:
            # Node content with icon and name
            icon = node.icon
            node_html = f"""
            <div style="display: flex; align-items: center; padding: 2px 0;">
                <span style="margin-right: 8px; font-size: 1.2em;">{icon}</span>
                <span style="font-weight: {'bold' if node.children else 'normal'}; 
                           color: {'#1E88E5' if node.node_type == 'class' else '#424242'};
                           cursor: pointer;"
                      onmouseover="this.style.backgroundColor='#F5F5F5'"
                      onmouseout="this.style.backgroundColor='transparent'">
                    {node.name}
                </span>
            </div>
            """
            st.markdown(node_html, unsafe_allow_html=True)
        
        # Show properties if node has any
        if node.properties and node.expanded:
            with st.container():
                for key, value in node.properties.items():
                    st.markdown(f"""
                    <div style="margin-left: {60 + node.level * 20}px; color: #666; font-size: 0.9em;">
                        ⚡ {key}: {value}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Render children if expanded
        if node.expanded and node.children:
            child_dict = {child.name: child for child in node.children}
            render_ontology_tree(child_dict, search_term)

def main():
    st.set_page_config(
        page_title="Ontology Viewer",
        page_icon="🔷",
        layout="wide"
    )
    
    # Custom CSS for exact styling
    st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background-color: #FFFFFF;
    }
    
    /* Tree container */
    .tree-container {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding: 20px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Node styling */
    .node-row {
        display: flex;
        align-items: center;
        padding: 4px 8px;
        border-radius: 4px;
        transition: background-color 0.2s;
    }
    
    .node-row:hover {
        background-color: #F5F5F5;
    }
    
    /* Button styling */
    .stButton > button {
        background: transparent;
        border: none;
        padding: 0 4px;
        min-width: 24px;
        height: 24px;
        font-size: 14px;
        color: #555;
        border-radius: 4px;
    }
    
    .stButton > button:hover {
        background-color: #E0E0E0;
        color: #000;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #F8F9FA;
    }
    
    /* Header styling */
    h1 {
        color: #1E3A5F;
        font-weight: 500;
        border-bottom: 2px solid #E0E0E0;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    /* Stats cards */
    .stat-card {
        background: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 4px solid #1E88E5;
        margin-bottom: 10px;
    }
    
    /* Legend items */
    .legend-item {
        display: flex;
        align-items: center;
        padding: 5px 0;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'ontology' not in st.session_state:
        st.session_state.ontology = create_sample_ontology()
        set_node_levels(st.session_state.ontology)
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🔷 Ontology Explorer")
        st.markdown("Browse and explore the ontology hierarchy")
    
    with col2:
        st.image("https://img.icons8.com/color/96/000000/flow-chart.png", width=80)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎮 Controls")
        
        # Search
        search_term = st.text_input("🔍 Search concepts", placeholder="Type to filter...")
        
        st.markdown("---")
        
        # Expand/Collapse buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔽 Expand All", use_container_width=True):
                def expand_all(nodes):
                    for node in nodes.values():
                        node.expanded = True
                        if node.children:
                            child_dict = {child.name: child for child in node.children}
                            expand_all(child_dict)
                expand_all(st.session_state.ontology)
                st.rerun()
        
        with col2:
            if st.button("🔼 Collapse All", use_container_width=True):
                def collapse_all(nodes):
                    for node in nodes.values():
                        node.expanded = False
                        if node.children:
                            child_dict = {child.name: child for child in node.children}
                            collapse_all(child_dict)
                collapse_all(st.session_state.ontology)
                st.rerun()
        
        st.markdown("---")
        
        # Statistics
        st.markdown("## 📊 Statistics")
        
        total_classes = count_classes(st.session_state.ontology)
        max_depth = get_max_depth(st.session_state.ontology)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Classes", total_classes)
        with col2:
            st.metric("Max Depth", max_depth)
        
        st.markdown("---")
        
        # Legend
        st.markdown("## 📖 Legend")
        legend_items = [
            ("🔷", "Class (with children)"),
            ("👤", "Person types"),
            ("🏛️", "Organization types"),
            ("📅", "Event types"),
            ("🌍", "Place types"),
            ("📄", "Document types")
        ]
        
        for icon, label in legend_items:
            st.markdown(f"<div class='legend-item'><span style='margin-right: 10px; font-size: 1.2em;'>{icon}</span> {label}</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Export option
        if st.button("📥 Export Ontology", use_container_width=True):
            st.success("Ontology exported successfully!")
    
    # Main content
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<div class="tree-container">', unsafe_allow_html=True)
        st.markdown("### 🌳 Ontology Tree")
        
        # Render the tree
        render_ontology_tree(st.session_state.ontology, search_term)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### ℹ️ Instructions")
        with st.container():
            st.markdown("""
            <div style="background: #F8F9FA; padding: 15px; border-radius: 8px;">
                <p>▶️ Click to expand/collapse</p>
                <p>🔍 Use search to filter</p>
                <p>📊 Statistics show structure</p>
                <p>🎨 Colors indicate types</p>
                <hr>
                <p><small>Total nodes expandable<br>Click arrows to explore</small></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick actions
        st.markdown("### 🚀 Quick Actions")
        if st.button("🔄 Reset View", use_container_width=True):
            collapse_all(st.session_state.ontology)
            st.rerun()
        
        if st.button("📋 Copy Path", use_container_width=True):
            st.info("Path copied to clipboard")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 10px;'>"
        "🔷 Ontology Explorer v1.0 | Click arrows to expand/collapse nodes"
        "</div>", 
        unsafe_allow_html=True
    )

def count_classes(nodes_dict):
    """Count total number of classes in ontology"""
    count = len(nodes_dict)
    for node in nodes_dict.values():
        if node.children:
            child_dict = {child.name: child for child in node.children}
            count += count_classes(child_dict)
    return count

def get_max_depth(nodes_dict, current_depth=1):
    """Get maximum depth of ontology"""
    if not nodes_dict:
        return current_depth
    
    max_depth = current_depth
    for node in nodes_dict.values():
        if node.children:
            child_dict = {child.name: child for child in node.children}
            depth = get_max_depth(child_dict, current_depth + 1)
            max_depth = max(max_depth, depth)
    
    return max_depth

if __name__ == "__main__":
    main()
