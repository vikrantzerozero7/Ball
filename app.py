import streamlit as st
from typing import Dict, List, Optional
import time

class TreeNode:
    def __init__(self, id: str, label: str, children: List['TreeNode'] = None, 
                 node_type: str = "default", data: Dict = None):
        self.id = id
        self.label = label
        self.children = children or []
        self.node_type = node_type
        self.data = data or {}
        self.expanded = False
        self.selected = False

def create_file_system_style_ontology():
    """Create ontology with file system style"""
    return [
        TreeNode("root1", "📁 Knowledge Base", [
            TreeNode("node1", "📁 Sciences", [
                TreeNode("node11", "📁 Physics", [
                    TreeNode("node111", "📄 Classical Mechanics", 
                            node_type="file", 
                            data={"author": "Newton", "year": 1687}),
                    TreeNode("node112", "📄 Quantum Physics",
                            node_type="file",
                            data={"author": "Various", "year": "1900s"})
                ]),
                TreeNode("node12", "📁 Chemistry", [
                    TreeNode("node121", "📄 Organic Chemistry",
                            node_type="file"),
                    TreeNode("node122", "📄 Inorganic Chemistry",
                            node_type="file")
                ])
            ]),
            TreeNode("node2", "📁 Mathematics", [
                TreeNode("node21", "📁 Algebra", [
                    TreeNode("node211", "📄 Linear Algebra",
                            node_type="file"),
                    TreeNode("node212", "📄 Abstract Algebra",
                            node_type="file")
                ]),
                TreeNode("node22", "📁 Calculus", [
                    TreeNode("node221", "📄 Differential Calculus",
                            node_type="file"),
                    TreeNode("node222", "📄 Integral Calculus",
                            node_type="file")
                ])
            ])
        ], node_type="folder", data={"description": "Main knowledge base"}),
        
        TreeNode("root2", "📁 Projects", [
            TreeNode("node3", "📁 Active Projects", [
                TreeNode("node31", "📄 Project Alpha",
                        node_type="file",
                        data={"status": "active", "priority": "high"}),
                TreeNode("node32", "📄 Project Beta",
                        node_type="file",
                        data={"status": "active", "priority": "medium"})
            ]),
            TreeNode("node4", "📁 Archived Projects", [
                TreeNode("node41", "📄 Old Project",
                        node_type="file",
                        data={"status": "archived", "year": 2023})
            ])
        ], node_type="folder")
    ]

def render_node_js_style(nodes: List[TreeNode], level: int = 0):
    """Render tree in Node.js file explorer style"""
    
    for node in nodes:
        # Create unique key
        node_key = f"tree_{node.id}_{level}"
        
        # Create columns for layout
        cols = st.columns([0.05, 0.05, 0.9])
        
        with cols[0]:
            # Expand/collapse button for folders
            if node.children:
                icon = "▼" if node.expanded else "▶"
                if st.button(icon, key=f"btn_{node_key}", help="Click to expand/collapse"):
                    node.expanded = not node.expanded
                    st.rerun()
            else:
                st.write("  ")
        
        with cols[1]:
            # Hierarchy lines
            st.markdown("│  " * level + "├─" if level > 0 else "")
        
        with cols[2]:
            # Node content with hover effect
            col_content, col_actions = st.columns([0.8, 0.2])
            
            with col_content:
                # Node label with styling
                if node.children:
                    st.markdown(f"**{node.label}**")
                else:
                    st.markdown(node.label)
            
            with col_actions:
                # Action buttons on hover (simulated with columns)
                if st.button("ℹ️", key=f"info_{node_key}", help="Show details"):
                    show_node_details(node)
        
        # Render children if expanded
        if node.expanded and node.children:
            render_node_js_style(node.children, level + 1)

def show_node_details(node: TreeNode):
    """Show node details in a modal/popup"""
    with st.popover(f"Details: {node.label}"):
        st.write(f"**ID:** {node.id}")
        st.write(f"**Type:** {node.node_type}")
        
        if node.data:
            st.write("**Data:**")
            for key, value in node.data.items():
                st.write(f"- {key}: {value}")
        
        if node.children:
            st.write(f"**Children:** {len(node.children)}")

def main():
    st.set_page_config(layout="wide", page_title="Node.js Style Ontology")
    
    st.title("🌳 Node.js Style Ontology Explorer")
    st.caption("Click ▶ to expand, ▼ to collapse, ℹ️ for details")
    
    # Initialize
    if 'tree_nodes' not in st.session_state:
        st.session_state.tree_nodes = create_file_system_style_ontology()
    
    # Toolbar
    toolbar = st.container()
    with toolbar:
        cols = st.columns([1, 1, 1, 3])
        
        with cols[0]:
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()
        
        with cols[1]:
            if st.button("📂 Expand All", use_container_width=True):
                def expand_all(nodes):
                    for node in nodes:
                        node.expanded = True
                        if node.children:
                            expand_all(node.children)
                expand_all(st.session_state.tree_nodes)
                st.rerun()
        
        with cols[2]:
            if st.button("📁 Collapse All", use_container_width=True):
                def collapse_all(nodes):
                    for node in nodes:
                        node.expanded = False
                        if node.children:
                            collapse_all(node.children)
                collapse_all(st.session_state.tree_nodes)
                st.rerun()
        
        with cols[3]:
            st.text_input("🔍 Filter nodes...", key="filter", placeholder="Type to filter...")
    
    st.divider()
    
    # Main tree view
    with st.container():
        render_node_js_style(st.session_state.tree_nodes)
    
    # Status bar
    st.divider()
    st.caption(f"📍 Total root nodes: {len(st.session_state.tree_nodes)} | Click ▶ to explore")

if __name__ == "__main__":
    main()
