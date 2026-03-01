import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL
import json

# Page configuration
st.set_page_config(
    page_title="Ontology Viewer",
    page_layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("🔍 Ontology Explorer")
st.markdown("---")

class OntologyManager:
    def __init__(self):
        self.graph = Graph()
        self.ns = Namespace("http://example.org/")
        
    def load_ontology(self, file):
        """Load ontology from file"""
        try:
            self.graph.parse(file, format="xml")
            return True
        except Exception as e:
            st.error(f"Error loading ontology: {e}")
            return False
    
    def get_classes(self):
        """Get all classes in the ontology"""
        classes = []
        for s in self.graph.subjects(RDF.type, OWL.Class):
            classes.append(str(s))
        return classes
    
    def get_individuals(self):
        """Get all individuals"""
        individuals = []
        for s in self.graph.subjects(RDF.type, OWL.NamedIndividual):
            individuals.append(str(s))
        return individuals
    
    def get_properties(self):
        """Get all properties"""
        properties = []
        for s in self.graph.subjects(RDF.type, OWL.ObjectProperty):
            properties.append(str(s))
        for s in self.graph.subjects(RDF.type, OWL.DatatypeProperty):
            properties.append(str(s))
        return properties

def create_network_graph(ontology_graph):
    """Create a network graph visualization"""
    G = nx.Graph()
    
    # Add nodes and edges from ontology
    for subj, pred, obj in ontology_graph:
        G.add_node(str(subj))
        G.add_node(str(obj))
        G.add_edge(str(subj), str(obj), label=str(pred))
    
    # Create plotly figure
    pos = nx.spring_layout(G)
    
    edge_trace = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace.append(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines'
        ))
    
    node_trace = go.Scatter(
        x=[], y=[], text=[],
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left'
            )
        )
    )
    
    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += (x,)
        node_trace['y'] += (y,)
        node_trace['text'] += (node,)
    
    fig = go.Figure(data=edge_trace + [node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    ))
    
    return fig

# Sidebar
with st.sidebar:
    st.header("📁 Ontology Management")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload Ontology File",
        type=['owl', 'rdf', 'ttl', 'xml']
    )
    
    # Initialize ontology manager
    if 'manager' not in st.session_state:
        st.session_state.manager = OntologyManager()
    
    # Load ontology
    if uploaded_file is not None:
        if st.button("Load Ontology"):
            with st.spinner("Loading ontology..."):
                if st.session_state.manager.load_ontology(uploaded_file):
                    st.success("Ontology loaded successfully!")
                    st.session_state.ontology_loaded = True
    
    st.markdown("---")
    
    # Display options
    st.header("⚙️ Display Options")
    show_classes = st.checkbox("Show Classes", value=True)
    show_individuals = st.checkbox("Show Individuals", value=True)
    show_properties = st.checkbox("Show Properties", value=True)

# Main content
if 'ontology_loaded' in st.session_state and st.session_state.ontology_loaded:
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview", 
        "🔷 Classes", 
        "👤 Individuals", 
        "🔗 Properties"
    ])
    
    with tab1:
        st.header("Ontology Overview")
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Classes", len(st.session_state.manager.get_classes()))
        with col2:
            st.metric("Total Individuals", len(st.session_state.manager.get_individuals()))
        with col3:
            st.metric("Total Properties", len(st.session_state.manager.get_properties()))
        
        # Graph visualization
        st.subheader("Ontology Graph")
        fig = create_network_graph(st.session_state.manager.graph)
        st.plotly_chart(fig, use_container_width=True)
        
        # Triple count
        st.info(f"Total triples: {len(st.session_state.manager.graph)}")
    
    with tab2:
        st.header("Classes")
        if show_classes:
            classes = st.session_state.manager.get_classes()
            if classes:
                df_classes = pd.DataFrame(classes, columns=["Class URI"])
                st.dataframe(df_classes, use_container_width=True)
                
                # Class details
                selected_class = st.selectbox("Select class to view details", classes)
                if selected_class:
                    st.subheader(f"Details for {selected_class}")
                    
                    # Get subclass relationships
                    subclasses = []
                    for s in st.session_state.manager.graph.subjects(RDFS.subClassOf, URIRef(selected_class)):
                        subclasses.append(str(s))
                    
                    if subclasses:
                        st.write("**Subclasses:**")
                        for sub in subclasses:
                            st.write(f"- {sub}")
            else:
                st.info("No classes found in ontology")
    
    with tab3:
        st.header("Individuals")
        if show_individuals:
            individuals = st.session_state.manager.get_individuals()
            if individuals:
                df_ind = pd.DataFrame(individuals, columns=["Individual URI"])
                st.dataframe(df_ind, use_container_width=True)
                
                # Individual details
                selected_ind = st.selectbox("Select individual to view details", individuals)
                if selected_ind:
                    st.subheader(f"Properties for {selected_ind}")
                    
                    # Get all properties of the individual
                    props = []
                    for pred, obj in st.session_state.manager.graph.predicate_objects(URIRef(selected_ind)):
                        props.append({
                            "Property": str(pred),
                            "Value": str(obj)
                        })
                    
                    if props:
                        df_props = pd.DataFrame(props)
                        st.dataframe(df_props, use_container_width=True)
            else:
                st.info("No individuals found in ontology")
    
    with tab4:
        st.header("Properties")
        if show_properties:
            properties = st.session_state.manager.get_properties()
            if properties:
                df_props = pd.DataFrame(properties, columns=["Property URI"])
                st.dataframe(df_props, use_container_width=True)
            else:
                st.info("No properties found in ontology")

else:
    # Welcome screen
    st.info("👈 Please upload an ontology file to get started!")
    
    # Example instructions
    with st.expander("📖 How to use this app"):
        st.markdown("""
        1. **Upload** an ontology file (OWL, RDF, Turtle, or XML format)
        2. Click **Load Ontology** to process the file
        3. Explore the ontology using the tabs:
           - **Overview**: See statistics and graph visualization
           - **Classes**: Browse all classes and their hierarchies
           - **Individuals**: View instances and their properties
           - **Properties**: List all object and datatype properties
        """)
    
    with st.expander("🎯 Features"):
        st.markdown("""
        - **Graph Visualization**: Interactive network graph of ontology relationships
        - **Class Hierarchy**: Explore subclass relationships
        - **Individual Details**: View all properties of specific individuals
        - **Statistics**: Quick overview of ontology size and composition
        - **Search**: Find specific entities in the ontology
        """)

# Footer
st.markdown("---")
st.markdown("Built with Streamlit and RDFlib")
