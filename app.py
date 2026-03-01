# app_expandable_ai.py
import streamlit as st
import networkx as nx
from pyvis.network import Network
import tempfile
import os
import random
import math
from collections import defaultdict
import numpy as np

st.set_page_config(page_title="AI Concepts Explorer", layout="wide")
st.title("AI Concepts: Search, Logic & Reasoning Under Uncertainty")

# ------------------------
# Enhanced AI Topics Ontology
# ------------------------
ai_ontology = {
    "Search Algorithms": {
        "instances": ["Uninformed Search", "Informed Search", "Adversarial Search"],
        "properties": {
            "timeComplexity": ["O(b^d)", "O(b^d)", "O(b^m)"],
            "spaceComplexity": ["O(b^d)", "O(b^d)", "O(bm)"],
            "completeness": ["Yes (if finite)", "Yes", "Yes (if finite)"],
            "optimality": ["No (for BFS/DFS)", "Yes (A*)", "No (Minimax)"]
        },
        "formulas": {
            "Uninformed Search": "BFS: O(b^d) time, O(b^d) space\nDFS: O(b^m) time, O(bm) space",
            "Informed Search": "A*: f(n) = g(n) + h(n)\nwhere h(n) ≤ h*(n) for admissibility",
            "Adversarial Search": "Minimax: V(s) = max_{a∈actions} min_{opponent} V(s')\nAlpha-Beta: O(b^(m/2))"
        }
    },
    
    "Logic": {
        "instances": ["Propositional Logic", "Predicate Logic"],
        "properties": {
            "syntax": ["Atoms + Connectives", "Terms + Predicates + Quantifiers"],
            "semantics": ["Truth Tables", "Interpretations + Models"],
            "inferenceRules": ["Modus Ponens, Resolution", "Universal Instantiation, Resolution"],
            "decidability": ["Decidable", "Semi-decidable"]
        },
        "formulas": {
            "Propositional Logic": "Modus Ponens: (P → Q) ∧ P ⇒ Q\nResolution: (P ∨ Q) ∧ (¬P ∨ R) ⇒ (Q ∨ R)",
            "Predicate Logic": "∀x P(x) ⇒ P(c) [Universal Instantiation]\n∃x P(x) ⇒ P(sk) [Skolemization]"
        }
    },
    
    "Reasoning Under Uncertainty": {
        "instances": ["Conditional Independence", "Exact Inference", "Approximate Inference"],
        "properties": {
            "representation": ["Bayesian Networks", "Variable Elimination", "Sampling Methods"],
            "complexity": ["O(2^n)", "O(n * d^k)", "O(n * samples)"],
            "accuracy": ["Exact", "Exact", "Approximate"],
            "useCase": ["Knowledge representation", "Probabilistic queries", "Large-scale inference"]
        },
        "formulas": {
            "Conditional Independence": "P(X,Y|Z) = P(X|Z) * P(Y|Z)\nX ⊥ Y | Z ⇔ P(X,Y,Z) ∝ φ₁(X,Z)φ₂(Y,Z)",
            "Exact Inference": "P(Q|E=e) = α ∑_{H} ∏_{i} P(X_i|Parents(X_i))\nVariable Elimination: τ(z) = ∑_x ∏_i φ_i(x,z)",
            "Approximate Inference": "Rejection Sampling: P(Q|E=e) ≈ count(Q ∧ e) / count(e)\nLikelihood Weighting: w = ∏ P(e_i|Parents(E_i))"
        }
    }
}

# ------------------------
# Sidebar for Topic Selection
# ------------------------
st.sidebar.header("Select AI Topic")
main_topics = list(ai_ontology.keys())
selected_topic = st.sidebar.selectbox("Main Topic", main_topics)

topic_data = ai_ontology[selected_topic]
instances = topic_data["instances"]
selected_instance = st.sidebar.selectbox("Subtopic", instances)

# Find index of selected instance
instance_index = instances.index(selected_instance)

# ------------------------
# Main Content Area
# ------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(f"📚 {selected_instance}")
    
    # Display properties
    st.markdown("### Properties")
    props_df = {}
    for prop, values in topic_data["properties"].items():
        props_df[prop] = values[instance_index]
    
    for prop, value in props_df.items():
        st.markdown(f"**{prop}:** {value}")
    
    # Display formula if available
    if "formulas" in topic_data and selected_instance in topic_data["formulas"]:
        st.markdown("### 📐 Key Formula(s)")
        st.code(topic_data["formulas"][selected_instance], language="text")
    
    # Interactive example based on topic
    st.markdown("### 🧪 Interactive Example")
    
    if selected_topic == "Search Algorithms":
        if selected_instance == "Informed Search (A*)":
            start = st.number_input("Start Node", value=0)
            goal = st.number_input("Goal Node", value=5)
            heuristic = st.slider("Heuristic value h(n)", 0, 10, 5)
            st.markdown(f"**f(n) = g(n) + h(n) = ? + {heuristic}**")
            
        elif selected_instance == "Adversarial Search":
            depth = st.slider("Search depth", 1, 5, 3)
            st.markdown(f"Minimax value at depth {depth}: O(b^{depth}) complexity")
    
    elif selected_topic == "Reasoning Under Uncertainty":
        if selected_instance == "Conditional Independence":
            st.latex(r"P(A,B|C) = P(A|C) \times P(B|C)")
            st.markdown("Given C, A and B are independent")
            
        elif selected_instance == "Exact Inference":
            st.latex(r"P(Q|E=e) = \alpha \sum_{H} \prod_i P(X_i|Parents(X_i))")
            st.markdown("Variable Elimination eliminates hidden variables H")
            
        elif selected_instance == "Approximate Inference":
            n_samples = st.slider("Number of samples", 100, 10000, 1000)
            st.markdown(f"Sampling with {n_samples} samples")
            st.markdown("**Rejection Sampling:** Keep samples matching evidence")
            st.markdown("**Likelihood Weighting:** Weight samples by evidence probability")

with col2:
    st.subheader("📊 Concept Graph Visualization")
    
    # Create enhanced graph
    G = nx.DiGraph()
    
    # Main topic node
    G.add_node(selected_topic, 
               color='lightblue', 
               size=40,
               title=f"Topic: {selected_topic}",
               level=1)
    
    # Add subtopic nodes
    for i, instance in enumerate(instances):
        color = 'lightgreen' if instance == selected_instance else 'lightgray'
        size = 30 if instance == selected_instance else 20
        
        G.add_node(instance, 
                  color=color, 
                  size=size,
                  title=f"Subtopic: {instance}",
                  level=2)
        G.add_edge(selected_topic, instance, 
                  label="hasSubtopic",
                  color='gray',
                  width=2)
        
        # Add property nodes for selected instance only (to keep graph readable)
        if instance == selected_instance:
            for prop, values in topic_data["properties"].items():
                prop_value = values[i]
                prop_node = f"{prop}: {prop_value}"
                
                G.add_node(prop_node, 
                          color='orange', 
                          size=15,
                          title=f"Property: {prop}",
                          level=3)
                G.add_edge(instance, prop_node, 
                          label=prop,
                          color='blue',
                          width=1.5)
                
                # Add formula nodes if available
                if "formulas" in topic_data and instance in topic_data["formulas"]:
                    formula_short = topic_data["formulas"][instance][:30] + "..."
                    formula_node = f"Formula: {instance}"
                    
                    G.add_node(formula_node,
                              color='pink',
                              size=12,
                              title=topic_data["formulas"][instance],
                              level=4)
                    G.add_edge(prop_node, formula_node,
                              label="hasFormula",
                              color='red',
                              width=1,
                              dashes=True)
    
    # Pyvis network with improved settings
    net = Network(height="500px", width="100%", directed=True, bgcolor="#ffffff", font_color="black")
    
    # Physics options for better layout
    net.set_options("""
    {
        "physics": {
            "enabled": true,
            "hierarchicalRepulsion": {
                "centralGravity": 0.0,
                "springLength": 200,
                "springConstant": 0.01,
                "nodeDistance": 150,
                "damping": 0.09
            },
            "solver": "hierarchicalRepulsion"
        },
        "layout": {
            "hierarchical": {
                "enabled": true,
                "direction": "LR",
                "sortMethod": "directed"
            }
        }
    }
    """)
    
    net.from_nx(G)
    
    # Save to temporary HTML file
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    net.save_graph(tmp_file.name)
    
    # Display in Streamlit
    with open(tmp_file.name, 'r', encoding='utf-8') as f:
        components_html = f.read()
    st.components.v1.html(components_html, height=550)
    os.unlink(tmp_file.name)

# ------------------------
# Expandable Detailed View
# ------------------------
st.markdown("---")
st.subheader(f"🔍 Detailed Exploration: {selected_instance}")

# Create tabs for different aspects
tab1, tab2, tab3 = st.tabs(["📖 Theory", "🧮 Formulas & Examples", "🔄 Related Concepts"])

with tab1:
    st.markdown(f"### {selected_instance} - Theoretical Foundation")
    
    if selected_topic == "Search Algorithms":
        if selected_instance == "Uninformed Search":
            st.markdown("""
            **Uninformed (Blind) Search** strategies have no additional information about states beyond that provided in the problem definition.
            
            - **BFS:** Explores all nodes at current depth before moving deeper
            - **DFS:** Explores as deep as possible along each branch before backtracking
            - **Uniform Cost:** Expands node with lowest path cost
            """)
        elif selected_instance == "Informed Search":
            st.markdown("""
            **Informed (Heuristic) Search** uses problem-specific knowledge to find solutions more efficiently.
            
            - **Greedy Best-First:** Expands node closest to goal
            - **A* Search:** Combines actual cost + heuristic estimate
            - **IDA*:** Iterative deepening A* for memory efficiency
            """)
        else:
            st.markdown("""
            **Adversarial Search** deals with competitive environments where agents have conflicting goals.
            
            - **Minimax:** Optimal decision in zero-sum games
            - **Alpha-Beta Pruning:** Prunes branches that cannot influence final decision
            - **Expectimax:** For games with chance nodes
            """)
    
    elif selected_topic == "Logic":
        if selected_instance == "Propositional Logic":
            st.markdown("""
            **Propositional Logic** deals with propositions and their logical relationships.
            
            - **Syntax:** Atoms (P, Q) and connectives (∧, ∨, ¬, →, ↔)
            - **Semantics:** Truth tables assign truth values
            - **Inference:** Modus ponens, resolution, forward/backward chaining
            """)
        else:
            st.markdown("""
            **First-Order Predicate Logic** extends propositional logic with quantifiers and predicates.
            
            - **Syntax:** Constants, variables, functions, predicates, quantifiers (∀, ∃)
            - **Semantics:** Interpretation over a domain
            - **Inference:** Unification, generalized modus ponens, resolution
            """)
    
    else:  # Reasoning Under Uncertainty
        if selected_instance == "Conditional Independence":
            st.markdown("""
            **Conditional Independence** is a fundamental concept in probabilistic graphical models.
            
            - **Definition:** X ⊥ Y | Z ⇔ P(X,Y|Z) = P(X|Z)P(Y|Z)
            - **Graphical test:** d-separation in Bayesian networks
            - **Factorization:** P(X₁,...,Xₙ) = ∏ P(Xᵢ|Parents(Xᵢ))
            """)
        elif selected_instance == "Exact Inference":
            st.markdown("""
            **Exact Inference** computes precise probabilities in Bayesian networks.
            
            - **Variable Elimination:** Dynamic programming approach
            - **Complexity:** Exponential in treewidth
            - **Junction Tree:** Clustering algorithm for exact inference
            """)
        else:
            st.markdown("""
            **Approximate Inference** uses sampling when exact inference is intractable.
            
            - **Rejection Sampling:** Generate samples, reject those not matching evidence
            - **Likelihood Weighting:** Fix evidence variables, weight samples
            - **MCMC:** Gibbs sampling, Metropolis-Hastings
            """)

with tab2:
    st.markdown(f"### Formulas and Examples for {selected_instance}")
    
    if "formulas" in topic_data and selected_instance in topic_data["formulas"]:
        st.code(topic_data["formulas"][selected_instance], language="text")
    
    # Interactive formula demonstration
    st.markdown("#### Interactive Demonstration")
    
    if selected_topic == "Reasoning Under Uncertainty":
        if selected_instance == "Conditional Independence":
            st.latex(r"P(COVID|Fever) = \frac{P(Fever|COVID)P(COVID)}{P(Fever)}")
            
            # Simple Bayesian network demo
            st.markdown("**Bayesian Network Example:**")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                p_covid = st.slider("P(COVID)", 0.0, 1.0, 0.1)
            with col_b:
                p_fever_given_covid = st.slider("P(Fever|COVID)", 0.0, 1.0, 0.8)
            with col_c:
                p_fever_given_no_covid = st.slider("P(Fever|¬COVID)", 0.0, 1.0, 0.1)
            
            # Calculate posterior
            p_no_covid = 1 - p_covid
            p_fever = p_fever_given_covid * p_covid + p_fever_given_no_covid * p_no_covid
            p_covid_given_fever = (p_fever_given_covid * p_covid) / p_fever if p_fever > 0 else 0
            
            st.metric("P(COVID|Fever)", f"{p_covid_given_fever:.3f}")
            
        elif selected_instance == "Exact Inference":
            st.markdown("**Variable Elimination Example:**")
            st.markdown("""
            Query: P(COVID | Fever=True)
            
            Factors:
            - φ₁(COVID) = P(COVID)
            - φ₂(Fever|COVID) = P(Fever|COVID)
            
            Elimination:
            P(COVID|Fever) ∝ φ₁(COVID) × φ₂(Fever|COVID)
            """)
            
        elif selected_instance == "Approximate Inference":
            st.markdown("**Sampling Demonstration:**")
            
            if st.button("Generate Samples"):
                n_samples = 1000
                covid_samples = np.random.binomial(1, 0.1, n_samples)
                fever_samples = []
                
                for covid in covid_samples:
                    if covid == 1:
                        fever_samples.append(np.random.binomial(1, 0.8))
                    else:
                        fever_samples.append(np.random.binomial(1, 0.1))
                
                samples_with_fever = sum(fever_samples)
                covid_given_fever = sum((covid_samples == 1) & (np.array(fever_samples) == 1))
                
                if samples_with_fever > 0:
                    prob = covid_given_fever / samples_with_fever
                    st.metric("Approximate P(COVID|Fever)", f"{prob:.3f}")
                    st.markdown(f"Generated {n_samples} samples, {samples_with_fever} had fever")

with tab3:
    st.markdown("### Related Concepts and Connections")
    
    # Show connections to other topics
    related = {
        "Search Algorithms": ["Logic for state representation", "Uncertainty in heuristic estimates"],
        "Logic": ["Search in theorem proving", "Uncertainty in fuzzy logic"],
        "Reasoning Under Uncertainty": ["Search in probabilistic inference", "Logic in knowledge representation"]
    }
    
    for topic, connections in related.items():
        if topic != selected_topic:
            st.markdown(f"**{topic}:**")
            for conn in connections:
                st.markdown(f"- {conn}")

# ------------------------
# Summary Statistics
# ------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Topic Statistics")
st.sidebar.metric("Main Topics", len(ai_ontology))
st.sidebar.metric("Subtopics", sum(len(v["instances"]) for v in ai_ontology.values()))
st.sidebar.metric("Properties", sum(len(v["properties"]) for v in ai_ontology.values()))

# Footer
st.markdown("---")
st.markdown("*Interactive AI Concepts Explorer - Integrating Search, Logic, and Reasoning Under Uncertainty*")
