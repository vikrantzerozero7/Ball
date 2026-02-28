import streamlit as st
import plotly.graph_objects as go
import numpy as np
from streamlit.components.v1 import html

st.set_page_config(layout="wide")
st.title("🎮 3D Object Rotation with Touch/Mouse")

# Create a 3D object (cube with colors)
def create_3d_object():
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
    
    # Add each face
    for i, face in enumerate(faces):
        x = [vertices[vertex][0] for vertex in face] + [vertices[face[0]][0]]
        y = [vertices[vertex][1] for vertex in face] + [vertices[face[0]][1]]
        z = [vertices[vertex][2] for vertex in face] + [vertices[face[0]][2]]
        
        fig.add_trace(go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines',
            line=dict(color=colors[i], width=3),
            showlegend=False,
            name=f'Face {i+1}'
        ))
    
    # Add semi-transparent surfaces
    for i, face in enumerate(faces):
        x = [vertices[vertex][0] for vertex in face]
        y = [vertices[vertex][1] for vertex in face]
        z = [vertices[vertex][2] for vertex in face]
        
        fig.add_trace(go.Mesh3d(
            x=x, y=y, z=z,
            color=colors[i],
            opacity=0.3,
            showlegend=False,
            name=f'Surface {i+1}'
        ))
    
    # Add vertices
    fig.add_trace(go.Scatter3d(
        x=vertices[:, 0], y=vertices[:, 1], z=vertices[:, 2],
        mode='markers',
        marker=dict(size=5, color='white'),
        showlegend=False
    ))
    
    # Update layout for interactive rotation
    fig.update_layout(
        scene=dict(
            xaxis=dict(showbackground=False, showticklabels=False, title=''),
            yaxis=dict(showbackground=False, showticklabels=False, title=''),
            zaxis=dict(showbackground=False, showticklabels=False, title=''),
            camera=dict(
                eye=dict(x=2, y=2, z=2)
            )
        ),
        width=800,
        height=600,
        margin=dict(l=0, r=0, b=0, t=0),
        hovermode=False,
        dragmode='turntable'  # Important for rotation
    )
    
    return fig

# Alternative: 3D Torus (donut shape)
def create_torus():
    n = 50
    m = 50
    R = 2  # Major radius
    r = 1  # Minor radius
    
    theta = np.linspace(0, 2*np.pi, n)
    phi = np.linspace(0, 2*np.pi, m)
    theta, phi = np.meshgrid(theta, phi)
    
    x = (R + r * np.cos(phi)) * np.cos(theta)
    y = (R + r * np.cos(phi)) * np.sin(theta)
    z = r * np.sin(phi)
    
    fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, colorscale='viridis', opacity=0.8)])
    
    fig.update_layout(
        scene=dict(
            xaxis=dict(showbackground=False, showticklabels=False, title=''),
            yaxis=dict(showbackground=False, showticklabels=False, title=''),
            zaxis=dict(showbackground=False, showticklabels=False, title=''),
            camera=dict(
                eye=dict(x=3, y=3, z=3)
            )
        ),
        width=800,
        height=600,
        margin=dict(l=0, r=0, b=0, t=0),
        dragmode='turntable'
    )
    
    return fig

# Sidebar controls
st.sidebar.header("Settings")

object_type = st.sidebar.selectbox(
    "Choose Object",
    ["Cube", "Torus", "Sphere", "Cylinder"]
)

if object_type == "Cube":
    fig = create_3d_object()
elif object_type == "Torus":
    fig = create_torus()
elif object_type == "Sphere":
    # Simple sphere
    u = np.linspace(0, 2*np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    
    fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, colorscale='hot')])
    fig.update_layout(scene_camera=dict(eye=dict(x=2.5, y=2.5, z=2.5)), dragmode='turntable')
else:  # Cylinder
    z = np.linspace(-1, 1, 50)
    theta = np.linspace(0, 2*np.pi, 50)
    theta, z = np.meshgrid(theta, z)
    x = np.cos(theta)
    y = np.sin(theta)
    
    fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, colorscale='portland')])
    fig.update_layout(scene_camera=dict(eye=dict(x=2.5, y=2.5, z=2.5)), dragmode='turntable')

# Display rotation instructions
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 🖱️ How to Rotate:
- **Drag with mouse** - Free rotation
- **Touch and drag** - On touch devices
- **Scroll** - Zoom in/out
- **Double click** - Reset view
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Tip:")
st.sidebar.markdown("Click and drag anywhere on the 3D object to rotate it in any direction!")

# Main area - display the 3D plot
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': True,
        'scrollZoom': True,
        'doubleClick': 'reset',
        'showTips': True
    })

# Add some information
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>✨ <strong>Touch/mouse drag</strong> to rotate the 3D object in any direction!</p>
    <p>📱 Works on both desktop and mobile devices with touch support</p>
</div>
""", unsafe_allow_html=True)
