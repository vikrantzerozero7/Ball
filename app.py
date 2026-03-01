import streamlit as st
import streamlit.components.v1 as components

# For older Streamlit versions or custom tree
def create_custom_ontology_tree():
    """Create ontology with custom HTML/CSS tree"""
    
    ontology_html = """
    <style>
    .tree {
        font-family: Arial, sans-serif;
        margin-left: 20px;
    }
    .tree-node {
        margin: 5px 0;
        cursor: pointer;
    }
    .tree-node:hover {
        background-color: #f0f0f0;
    }
    .tree-children {
        margin-left: 20px;
        display: none;
    }
    .tree-children.expanded {
        display: block;
    }
    .toggle-btn {
        display: inline-block;
        width: 20px;
        text-align: center;
        cursor: pointer;
        user-select: none;
    }
    .node-name {
        display: inline-block;
        padding: 2px 5px;
    }
    .node-name.parent {
        font-weight: bold;
    }
    </style>
    
    <div class="tree" id="ontologyTree">
        <div class="tree-node" onclick="toggleNode(this)">
            <span class="toggle-btn">▶</span>
            <span class="node-name parent">Thing</span>
            <div class="tree-children">
                <div class="tree-node" onclick="toggleNode(this)">
                    <span class="toggle-btn">▶</span>
                    <span class="node-name parent">Physical Object</span>
                    <div class="tree-children">
                        <div class="tree-node" onclick="toggleNode(this)">
                            <span class="toggle-btn">▶</span>
                            <span class="node-name parent">Living Thing</span>
                            <div class="tree-children">
                                <div class="tree-node">Animal</div>
                                <div class="tree-node">Plant</div>
                            </div>
                        </div>
                        <div class="tree-node" onclick="toggleNode(this)">
                            <span class="toggle-btn">▶</span>
                            <span class="node-name parent">Non-living Thing</span>
                            <div class="tree-children">
                                <div class="tree-node">Mineral</div>
                                <div class="tree-node">Artifact</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="tree-node" onclick="toggleNode(this)">
                    <span class="toggle-btn">▶</span>
                    <span class="node-name parent">Abstract Entity</span>
                    <div class="tree-children">
                        <div class="tree-node">Idea</div>
                        <div class="tree-node" onclick="toggleNode(this)">
                            <span class="toggle-btn">▶</span>
                            <span class="node-name parent">Concept</span>
                            <div class="tree-children">
                                <div class="tree-node">Mathematical Concept</div>
                                <div class="tree-node">Philosophical Concept</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
    function toggleNode(element) {
        var children = element.querySelector('.tree-children');
        var toggleBtn = element.querySelector('.toggle-btn');
        
        if (children) {
            if (children.classList.contains('expanded')) {
                children.classList.remove('expanded');
                toggleBtn.textContent = '▶';
            } else {
                children.classList.add('expanded');
                toggleBtn.textContent = '▼';
            }
        }
    }
    
    // Initialize all nodes
    document.querySelectorAll('.tree-node').forEach(node => {
        if (node.querySelector('.tree-children')) {
            node.style.cursor = 'pointer';
        }
    });
    </script>
    """
    
    return ontology_html

def main():
    st.title("Ontology Tree with Custom HTML/JS")
    
    # Option to use custom HTML
    use_custom = st.checkbox("Use Custom HTML Tree", value=True)
    
    if use_custom:
        # Embed custom HTML
        components.html(create_custom_ontology_tree(), height=500)
    else:
        # Fallback to simple expander method
        st.subheader("Simple Ontology")
        with st.expander("Thing", expanded=False):
            with st.expander("Physical Object", expanded=False):
                with st.expander("Living Thing", expanded=False):
                    st.write("• Animal")
                    st.write("• Plant")
                with st.expander("Non-living Thing", expanded=False):
                    st.write("• Mineral")
                    st.write("• Artifact")
            with st.expander("Abstract Entity", expanded=False):
                st.write("• Idea")
                with st.expander("Concept", expanded=False):
                    st.write("• Mathematical Concept")
                    st.write("• Philosophical Concept")

if __name__ == "__main__":
    main()
