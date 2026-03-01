import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Enterprise Ontology Manager",
    page_layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main container styling */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    
    /* Card styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: #f8f9fa;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: transform 0.2s;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Dataframe styling */
    .dataframe-container {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        background: white;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Info boxes */
    .info-box {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #e8f5e9;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3e0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff9800;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'ontology_graph' not in st.session_state:
    st.session_state.ontology_graph = None
if 'entities' not in st.session_state:
    st.session_state.entities = {}
if 'relationships' not in st.session_state:
    st.session_state.relationships = []

class EnterpriseOntology:
    def __init__(self):
        self.graph = Graph()
        self.ens = Namespace("http://enterprise.org/")
        self.graph.bind("ent", self.ens)
        
    def create_enterprise_schema(self):
        """Create enterprise ontology schema based on your fields"""
        
        # Define classes
        classes = {
            "Customer": "Customer entity",
            "Product": "Product package",
            "Market": "Market region",
            "Facility": "Healthcare facility",
            "CorporateGroup": "Corporate parent group",
            "Subsidiary": "Owner subsidiary",
            "Geography": "Geographical location",
            "FactTable": "Fact table entry",
            "CustomerTable": "Customer table entry",
            "ProductTable": "Product table entry"
        }
        
        for class_name, description in classes.items():
            class_uri = self.ens[class_name]
            self.graph.add((class_uri, RDF.type, OWL.Class))
            self.graph.add((class_uri, RDFS.label, Literal(class_name)))
            self.graph.add((class_uri, RDFS.comment, Literal(description)))
        
        # Define properties based on your fields
        properties = {
            # Customer properties
            "ae_name": (self.ens.Customer, XSD.string, "AE name"),
            "ae_geography_name": (self.ens.Geography, XSD.string, "AE geography name"),
            "ae_isid": (self.ens.Customer, XSD.string, "AE ISID"),
            "ae_row_number": (self.ens.CustomerTable, XSD.integer, "AE row number"),
            "customer_party_id": (self.ens.Customer, XSD.string, "Customer party ID"),
            "cust_table_row_number": (self.ens.CustomerTable, XSD.integer, "Customer table row number"),
            
            # Corporate properties
            "corporate_parent_id": (self.ens.CorporateGroup, XSD.string, "Corporate parent ID"),
            "owner_subsidiary_id": (self.ens.Subsidiary, XSD.string, "Owner subsidiary ID"),
            
            # Address and metrics
            "customer_address": (self.ens.Customer, XSD.string, "Customer address"),
            "Dds_gross": (self.ens.FactTable, XSD.decimal, "DDS gross amount"),
            "month": (self.ens.FactTable, XSD.date, "Month"),
            "fact_table_row_number": (self.ens.FactTable, XSD.integer, "Fact table row number"),
            
            # Product properties
            "product_package_id": (self.ens.Product, XSD.string, "Product package ID"),
            "product_table_row_number": (self.ens.ProductTable, XSD.integer, "Product table row number"),
            
            # Market properties
            "Market_id": (self.ens.Market, XSD.string, "Market ID"),
            "Market_name": (self.ens.Market, XSD.string, "Market name"),
            
            # Facility properties
            "hcos_facility_id": (self.ens.Facility, XSD.string, "HCOS facility ID")
        }
        
        for prop_name, (domain, range_type, comment) in properties.items():
            prop_uri = self.ens[prop_name]
            self.graph.add((prop_uri, RDF.type, OWL.DatatypeProperty))
            self.graph.add((prop_uri, RDFS.domain, domain))
            self.graph.add((prop_uri, RDFS.range, range_type))
            self.graph.add((prop_uri, RDFS.label, Literal(prop_name)))
            self.graph.add((prop_uri, RDFS.comment, Literal(comment)))
        
        # Define relationships
        relationships = [
            ("hasCustomer", self.ens.FactTable, self.ens.Customer, "Fact table has customer"),
            ("hasProduct", self.ens.FactTable, self.ens.Product, "Fact table has product"),
            ("hasMarket", self.ens.Customer, self.ens.Market, "Customer belongs to market"),
            ("hasFacility", self.ens.Customer, self.ens.Facility, "Customer associated with facility"),
            ("belongsToCorporate", self.ens.Customer, self.ens.CorporateGroup, "Customer belongs to corporate group"),
            ("hasSubsidiary", self.ens.CorporateGroup, self.ens.Subsidiary, "Corporate group has subsidiary"),
            ("locatedIn", self.ens.Customer, self.ens.Geography, "Customer located in geography")
        ]
        
        for rel_name, domain, range_type, comment in relationships:
            rel_uri = self.ens[rel_name]
            self.graph.add((rel_uri, RDF.type, OWL.ObjectProperty))
            self.graph.add((rel_uri, RDFS.domain, domain))
            self.graph.add((rel_uri, RDFS.range, range_type))
            self.graph.add((rel_uri, RDFS.label, Literal(rel_name)))
            self.graph.add((rel_uri, RDFS.comment, Literal(comment)))
        
        return True
    
    def add_sample_data(self):
        """Add sample data to the ontology"""
        
        # Create sample customers
        customers = [
            ("CUST001", "ABC Pharma", "North Region", "ISID001", "123 Pharma St"),
            ("CUST002", "XYZ Medical", "South Region", "ISID002", "456 Medical Ave"),
            ("CUST003", "Global Health", "East Region", "ISID003", "789 Health Blvd")
        ]
        
        for cust_id, name, geo, isid, address in customers:
            customer_uri = self.ens[f"Customer_{cust_id}"]
            self.graph.add((customer_uri, RDF.type, self.ens.Customer))
            self.graph.add((customer_uri, self.ens.ae_name, Literal(name)))
            self.graph.add((customer_uri, self.ens.ae_geography_name, Literal(geo)))
            self.graph.add((customer_uri, self.ens.ae_isid, Literal(isid)))
            self.graph.add((customer_uri, self.ens.customer_address, Literal(address)))
            self.graph.add((customer_uri, self.ens.customer_party_id, Literal(cust_id)))
        
        # Create sample products
        products = [
            ("PROD001", "Pharma Product A"),
            ("PROD002", "Medical Device B"),
            ("PROD003", "Diagnostic Kit C")
        ]
        
        for prod_id, prod_name in products:
            product_uri = self.ens[f"Product_{prod_id}"]
            self.graph.add((product_uri, RDF.type, self.ens.Product))
            self.graph.add((product_uri, self.ens.product_package_id, Literal(prod_id)))
        
        # Create sample markets
        markets = [
            ("MKT001", "US Market"),
            ("MKT002", "EU Market"),
            ("MKT003", "Asia Market")
        ]
        
        for market_id, market_name in markets:
            market_uri = self.ens[f"Market_{market_id}"]
            self.graph.add((market_uri, RDF.type, self.ens.Market))
            self.graph.add((market_uri, self.ens.Market_id, Literal(market_id)))
            self.graph.add((market_uri, self.ens.Market_name, Literal(market_name)))
        
        # Create relationships
        self.graph.add((self.ens.Customer_CUST001, self.ens.hasMarket, self.ens.Market_MKT001))
        self.graph.add((self.ens.Customer_CUST002, self.ens.hasMarket, self.ens.Market_MKT002))
        self.graph.add((self.ens.Customer_CUST003, self.ens.hasMarket, self.ens.Market_MKT003))
        
        return True

def create_ontology_visualization(graph):
    """Create interactive ontology visualization"""
    G = nx.MultiDiGraph()
    
    # Add nodes and edges
    node_colors = {}
    node_sizes = {}
    
    for subj, pred, obj in graph:
        subj_str = str(subj).split('/')[-1]
        obj_str = str(obj).split('/')[-1]
        pred_str = str(pred).split('/')[-1]
        
        G.add_node(subj_str)
        G.add_node(obj_str)
        G.add_edge(subj_str, obj_str, label=pred_str)
        
        # Color by type
        if (subj, RDF.type, OWL.Class) in graph:
            node_colors[subj_str] = '#FF6B6B'  # Classes in red
            node_sizes[subj_str] = 30
        elif (subj, RDF.type, OWL.NamedIndividual) in graph:
            node_colors[subj_str] = '#4ECDC4'  # Individuals in teal
            node_sizes[subj_str] = 20
    
    # Create layout
    pos = nx.spring_layout(G, k=3, iterations=50)
    
    # Create edge traces
    edge_traces = []
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        
        edge_trace = go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            line=dict(width=1, color='#888'),
            hoverinfo='none',
            mode='lines',
            showlegend=False
        )
        edge_traces.append(edge_trace)
    
    # Create node trace
    node_x = []
    node_y = []
    node_text = []
    node_color_list = []
    node_size_list = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        node_color_list.append(node_colors.get(node, '#95A5A6'))
        node_size_list.append(node_sizes.get(node, 15))
    
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            color=node_color_list,
            size=node_size_list,
            line=dict(color='white', width=2)
        ),
        showlegend=False
    )
    
    # Create figure
    fig = go.Figure(
        data=edge_traces + [node_trace],
        layout=go.Layout(
            title=dict(
                text="Ontology Graph Visualization",
                font=dict(size=16, color='#2C3E50')
            ),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=20, r=20, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=600
        )
    )
    
    return fig

# Header
st.markdown("""
<div class="main-header">
    <h1>🏢 Enterprise Ontology Manager</h1>
    <p>Comprehensive ontology management system for enterprise data integration</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🎯 Quick Actions")
    
    if st.button("🚀 Initialize Enterprise Ontology", use_container_width=True):
        with st.spinner("Creating enterprise ontology..."):
            ontology = EnterpriseOntology()
            ontology.create_enterprise_schema()
            ontology.add_sample_data()
            st.session_state.ontology_graph = ontology.graph
            st.session_state.entities = {
                'classes': [str(s) for s in ontology.graph.subjects(RDF.type, OWL.Class)],
                'individuals': [str(s) for s in ontology.graph.subjects(RDF.type, OWL.NamedIndividual)],
                'properties': [str(s) for s in ontology.graph.subjects(RDF.type, OWL.DatatypeProperty)]
            }
            st.success("✅ Ontology initialized successfully!")
    
    st.markdown("---")
    st.markdown("## 📁 Import Data")
    
    data_file = st.file_uploader(
        "Upload CSV/Excel",
        type=['csv', 'xlsx', 'xls'],
        help="Upload your enterprise data to populate the ontology"
    )
    
    if data_file:
        try:
            if data_file.name.endswith('.csv'):
                df = pd.read_csv(data_file)
            else:
                df = pd.read_excel(data_file)
            
            st.success(f"Loaded {len(df)} rows")
            st.dataframe(df.head(3), use_container_width=True)
        except Exception as e:
            st.error(f"Error loading file: {e}")

# Main content
if st.session_state.ontology_graph:
    # Quick metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Classes</h3>
            <h2>{}</h2>
            <small>Total ontology classes</small>
        </div>
        """.format(len(st.session_state.entities.get('classes', []))), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>👥 Individuals</h3>
            <h2>{}</h2>
            <small>Total instances</small>
        </div>
        """.format(len(st.session_state.entities.get('individuals', []))), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🔗 Properties</h3>
            <h2>{}</h2>
            <small>Data properties</small>
        </div>
        """.format(len(st.session_state.entities.get('properties', []))), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>🔄 Triples</h3>
            <h2>{}</h2>
            <small>Total relationships</small>
        </div>
        """.format(len(st.session_state.ontology_graph)), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🌐 Ontology Graph", 
        "📋 Classes", 
        "👤 Individuals", 
        "🔧 Properties",
        "📊 Data Explorer"
    ])
    
    with tab1:
        st.markdown("### Interactive Ontology Visualization")
        fig = create_ontology_visualization(st.session_state.ontology_graph)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📖 Graph Controls"):
            st.markdown("""
            - **Zoom**: Use scroll wheel or pinch gesture
            - **Pan**: Click and drag empty space
            - **Hover**: See node details
            - **Nodes**: Colored by type (Red: Classes, Teal: Individuals)
            """)
    
    with tab2:
        st.markdown("### Class Hierarchy")
        
        # Search classes
        class_search = st.text_input("🔍 Search classes", placeholder="Enter class name...")
        
        classes = st.session_state.entities.get('classes', [])
        filtered_classes = [c for c in classes if class_search.lower() in c.lower()] if class_search else classes
        
        for cls in filtered_classes:
            with st.container():
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                    <h4 style="color: #667eea; margin:0;">📌 {cls.split('/')[-1]}</h4>
                    <p style="color: #666; margin:0; font-size: 0.9rem;">{cls}</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### Individuals/Instances")
        
        individuals = st.session_state.entities.get('individuals', [])
        
        # Group by type
        individual_types = {}
        for ind in individuals:
            ind_uri = URIRef(ind)
            for obj in st.session_state.ontology_graph.objects(ind_uri, RDF.type):
                type_name = str(obj).split('/')[-1]
                if type_name not in individual_types:
                    individual_types[type_name] = []
                individual_types[type_name].append(ind)
        
        # Display individuals by type
        for type_name, inds in individual_types.items():
            with st.expander(f"{type_name} ({len(inds)})"):
                for ind in inds:
                    st.markdown(f"- {ind.split('/')[-1]}")
    
    with tab4:
        st.markdown("### Properties")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Datatype Properties**")
            for prop in st.session_state.ontology_graph.subjects(RDF.type, OWL.DatatypeProperty):
                prop_name = str(prop).split('/')[-1]
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 0.5rem; border-radius: 5px; margin: 0.3rem 0;">
                    <strong>{prop_name}</strong>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("**🔄 Object Properties**")
            for prop in st.session_state.ontology_graph.subjects(RDF.type, OWL.ObjectProperty):
                prop_name = str(prop).split('/')[-1]
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 0.5rem; border-radius: 5px; margin: 0.3rem 0;">
                    <strong>{prop_name}</strong>
                </div>
                """, unsafe_allow_html=True)
    
    with tab5:
        st.markdown("### Data Explorer")
        
        # Convert to DataFrame for exploration
        data_rows = []
        for subj, pred, obj in st.session_state.ontology_graph:
            data_rows.append({
                'Subject': str(subj).split('/')[-1],
                'Predicate': str(pred).split('/')[-1],
                'Object': str(obj).split('/')[-1]
            })
        
        df_triples = pd.DataFrame(data_rows)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            subject_filter = st.selectbox("Filter by Subject", ['All'] + list(df_triples['Subject'].unique()))
        with col2:
            predicate_filter = st.selectbox("Filter by Predicate", ['All'] + list(df_triples['Predicate'].unique()))
        with col3:
            object_filter = st.selectbox("Filter by Object", 
