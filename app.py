import streamlit as st
import plotly.graph_objects as go
import numpy as np
from streamlit.components.v1 import html

st.set_page_config(layout="wide")
st.title("🎮 3D Object Rotation with Touch/Mouse")

# Custom CSS for better touch experience
st.markdown("""
<style>
    .js-plotly-plot {
        touch-action: none;  /* Better touch handling */
    }
    .stApp {
        background-color: #0e1117;
    }
</style>
""", unsafe_allow_html=True)

def create_free_rotation_object():
    # Create a complex object with multiple features
    t = np.linspace(0, 4*np.pi, 200)
    
    # Helix (spring) for better rotation visualization
    x = np.sin(t) * 1.5
    y = np.cos(t) * 1.5
    z = t / 2 - 3
    
    # Additional points scattered in 3D space
    n_points = 150
    x_rand = np.random.randn(n_points) * 2
    y_rand = np.random.randn(n_points) * 2
    z_rand = np.random.randn(n_points) * 2
    
    fig = go.Figure()
    
    # Main helix with gradient color
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines+markers',
        line=dict(
            color=t,  # Color changes along the helix
            colorscale='Viridis',
            width=6
        ),
        marker=dict(
            size=2,
            color=t,
            colorscale='Plasma',
            showscale=False
        ),
        name='Helix',
        hoverinfo='none'
    ))
    
    # Scattered points with glow effect
    fig.add_trace(go.Scatter3d(
        x=x_rand, y=y_rand, z=z_rand,
        mode='markers',
        marker=dict(
            size=3,
            color=x_rand * y_rand,
            colorscale='Hot',
            opacity=0.8,
            showscale=False
        ),
        name='Particles',
        hoverinfo='none'
    ))
    
    # Add transparent sphere for reference
    u = np.linspace(0, 2*np.pi, 30)
    v = np.linspace(0, np.pi, 30)
    u, v = np.meshgrid(u, v)
    
    sphere_x = 1.5 * np.sin(v) * np.cos(u)
    sphere_y = 1.5 * np.sin(v) * np.sin(u)
    sphere_z = 1.5 * np.cos(v)
    
    fig.add_trace(go.Surface(
        x=sphere_x, y=sphere_y, z=sphere_z,
        opacity=0.1,
        colorscale='Greys',
        showscale=False,
        hoverinfo='none',
        name='Reference Sphere'
    ))
    
    # CRITICAL SETTINGS FOR FREE ROTATION - FIXED SYNTAX
    fig.update_layout(
        scene=dict(
            xaxis=dict(
                showbackground=True,
                backgroundcolor="rgba(20, 30, 50, 0.8)",
                gridcolor="rgba(255,255,255,0.2)",  # Only once!
                showline=True,
                linewidth=2,
                linecolor='white',
                showgrid=True,
                gridwidth=1,
                showticklabels=False,
                title='',
                range=[-3.5, 3.5]
            ),
            yaxis=dict(
                showbackground=True,
                backgroundcolor="rgba(20, 30, 50, 0.8)",
                gridcolor="rgba(255,255,255,0.2)",  # Only once!
                showline=True,
                linewidth=2,
                linecolor='white',
                showgrid=True,
                gridwidth=1,
                showticklabels=False,
                title='',
                range=[-3.5, 3.5]
            ),
            zaxis=dict(
                showbackground=True,
                backgroundcolor="rgba(20, 30, 50, 0.8)",
                gridcolor="rgba(255,255,255,0.2)",  # Only once!
                showline=True,
                linewidth=2,
                linecolor='white',
                showgrid=True,
                gridwidth=1,
                showticklabels=False,
                title='',
                range=[-3.5, 3.5]
            ),
            aspectmode='cube',
            camera=dict(
                eye=dict(x=2.5, y=2.5, z=2.5),
                center=dict(x=0, y=0, z=0),
                up=dict(x=0, y=0, z=1)
            ),
            dragmode='turntable',
        ),
        width=1000,
        height=700,
        margin=dict(l=0, r=0, b=0, t=30),
        hovermode=False,
        uirevision='constant',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# Create a cube with colored faces
def create_colored_cube():
    # Cube vertices
    vertices = np.array([
        [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
        [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
    ])
    
    # Cube faces
    faces = [
        [0, 1, 2, 3],  # back
        [4, 5, 6, 7],  # front
        [0, 1, 5, 4],  # bottom
        [2, 3, 7, 6],  # top
        [1, 2, 6, 5],  # right
        [0, 3, 7, 4]   # left
    ]
    
    # Colors for each face
    colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple']
    
    fig = go.Figure()
    
    # Add each face as a Mesh3d for solid colors
    for i, face in enumerate(faces):
        x = [vertices[vertex][0] for vertex in face]
        y = [vertices[vertex][1] for vertex in face]
        z = [vertices[vertex][2] for vertex in face]
        
        fig.add_trace(go.Mesh3d(
            x=x, y=y, z=z,
            color=colors[i],
            opacity=0.6,
            name=f'Face {i+1}',
            hoverinfo='none',
            flatshading=True
        ))
    
    # Add edges
    edges = [
        [0, 1], [1, 2], [2, 3], [3, 0],  # back face edges
        [4, 5], [5, 6], [6, 7], [7, 4],  # front face edges
        [0, 4], [1, 5], [2, 6], [3, 7]   # connecting edges
    ]
    
    for edge in edges:
        fig.add_trace(go.Scatter3d(
            x=[vertices[edge[0]][0], vertices[edge[1]][0]],
            y=[vertices[edge[0]][1], vertices[edge[1]][1]],
            z=[vertices[edge[0]][2], vertices[edge[1]][2]],
            mode='lines',
            line=dict(color='white', width=2),
            showlegend=False,
            hoverinfo='none'
        ))
    
    fig.update_layout(
        scene=dict(
            xaxis=dict(showticklabels=False, title='', range=[-1.5, 1.5]),
            yaxis=dict(showticklabels=False, title='', range=[-1.5, 1.5]),
            zaxis=dict(showticklabels=False, title='', range=[-1.5, 1.5]),
            aspectmode='cube',
            camera=dict(eye=dict(x=2, y=2, z=2)),
            dragmode='turntable'
        ),
        width=1000,
        height=700,
        uirevision='constant'
    )
    
    return fig

# Sidebar controls
with st.sidebar:
    st.header("🎛️ Settings")
    
    object_choice = st.selectbox(
        "Choose Object",
        ["Helix with Particles", "Colored Cube", "Abstract Shape"]
    )
    
    st.markdown("---")
    
    st.markdown("""
    ### 🖱️ How to Rotate:
    - **Drag with mouse** - Free rotation
    - **Touch and drag** - On touch devices
    - **Scroll** - Zoom in/out
    - **Double click** - Reset view
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 🎯 Tip:
    Click and drag anywhere on the 3D object to rotate it in any direction!
    """)
    
    st.markdown("---")
    
    # Rotation status
    st.success("✅ **Completely Free Rotation** - Kisi point pe nahi atakega!")

# Create appropriate figure
if object_choice == "Helix with Particles":
    fig = create_free_rotation_object()
elif object_choice == "Colored Cube":
    fig = create_colored_cube()
else:
    # Create abstract shape
    fig = create_free_rotation_object()  # Reuse helix for now

# Display the plot
st.plotly_chart(fig, use_container_width=True, config={
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToAdd': ['orbitRotation', 'resetCameraDefault'],
    'modeBarButtonsToRemove': ['select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 
                               'autoScale2d', 'resetScale2d', 'pan2d'],
    'scrollZoom': True,
    'doubleClick': 'reset',
    'showTips': True,
    'responsive': True
})

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <p style='font-size: 18px; color: #4CAF50;'>
        ✨ <strong>Ab object completely free ghumega!</strong>
    </p>
    <p style='font-size: 14px; color: #888;'>
        📱 Works on both desktop and mobile devices with touch support
    </p>
</div>
""", unsafe_allow_html=True)
