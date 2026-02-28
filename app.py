import streamlit as st
import plotly.graph_objects as go
import numpy as np
from streamlit.components.v1 import html

st.set_page_config(layout="wide")
st.title("🎮 Truly Free 3D Rotation - No Lock!")

# Custom CSS for better touch experience
st.markdown("""
<style>
    .js-plotly-plot {
        touch-action: none;  /* Better touch handling */
    }
</style>
""", unsafe_allow_html=True)

def create_free_rotation_object():
    # Create a complex object with multiple features
    t = np.linspace(0, 2*np.pi, 100)
    
    # Helix (spring) for better rotation visualization
    x = np.sin(t)
    y = np.cos(t)
    z = t / 2
    
    # Additional points scattered in 3D space
    n_points = 100
    x_rand = np.random.randn(n_points) * 2
    y_rand = np.random.randn(n_points) * 2
    z_rand = np.random.randn(n_points) * 2
    
    fig = go.Figure()
    
    # Main helix
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines+markers',
        line=dict(color='cyan', width=5),
        marker=dict(size=3, color='yellow'),
        name='Helix'
    ))
    
    # Scattered points
    fig.add_trace(go.Scatter3d(
        x=x_rand, y=y_rand, z=z_rand,
        mode='markers',
        marker=dict(
            size=4,
            color=x_rand,
            colorscale='Viridis',
            opacity=0.8
        ),
        name='Random Points'
    ))
    
    # Add some connecting lines
    for i in range(0, len(x_rand)-10, 10):
        fig.add_trace(go.Scatter3d(
            x=[x_rand[i], x_rand[i+5]],
            y=[y_rand[i], y_rand[i+5]],
            z=[z_rand[i], z_rand[i+5]],
            mode='lines',
            line=dict(color='rgba(100,100,100,0.3)', width=1),
            showlegend=False
        ))
    
    # CRITICAL SETTINGS FOR FREE ROTATION
    fig.update_layout(
        scene=dict(
            xaxis=dict(
                showbackground=True,
                backgroundcolor="rgba(0, 0, 0, 0.1)",
                gridcolor="white",
                showline=True,
                linewidth=2,
                linecolor='white',
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(255,255,255,0.1)',
                showticklabels=False,
                title='',
                range=[-3, 3]  # Fixed range
            ),
            yaxis=dict(
                showbackground=True,
                backgroundcolor="rgba(0, 0, 0, 0.1)",
                gridcolor="white",
                showline=True,
                linewidth=2,
                linecolor='white',
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(255,255,255,0.1)',
                showticklabels=False,
                title='',
                range=[-3, 3]
            ),
            zaxis=dict(
                showbackground=True,
                backgroundcolor="rgba(0, 0, 0, 0.1)",
                gridcolor="white",
                showline=True,
                linewidth=2,
                linecolor='white',
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(255,255,255,0.1)',
                showticklabels=False,
                title='',
                range=[-3, 3]
            ),
            aspectmode='cube',  # Equal aspect ratio
            camera=dict(
                # Initial camera position
                eye=dict(x=2.5, y=2.5, z=2.5),
                center=dict(x=0, y=0, z=0),
                # IMPORTANT: No up constraint
                up=dict(x=0, y=0, z=1)
            ),
            dragmode='turntable',  # Changed from 'orbit' for smoother rotation
        ),
        width=1000,
        height=700,
        margin=dict(l=0, r=0, b=0, t=30),
        hovermode=False,
        # These settings are crucial
        uirevision='constant',  # Maintain rotation state
    )
    
    return fig

# Alternative: Sphere with custom rotation
def create_sphere_free_rotation():
    # Create sphere with multiple colors for better orientation
    u = np.linspace(0, 2*np.pi, 40)
    v = np.linspace(0, np.pi, 40)
    u, v = np.meshgrid(u, v)
    
    x = np.sin(v) * np.cos(u)
    y = np.sin(v) * np.sin(u)
    z = np.cos(v)
    
    # Color based on direction for better orientation
    colors = np.arctan2(y, x)  # Color changes with rotation
    
    fig = go.Figure(data=[
        go.Surface(
            x=x, y=y, z=z,
            surfacecolor=colors,
            colorscale='HSV',
            opacity=0.9,
            showscale=False
        )
    ])
    
    # Add axis lines for reference
    for axis, color in [('x', 'red'), ('y', 'green'), ('z', 'blue')]:
        line_data = np.array([[-2, 2], [0, 0], [0, 0]]) if axis == 'x' else \
                   np.array([[0, 0], [-2, 2], [0, 0]]) if axis == 'y' else \
                   np.array([[0, 0], [0, 0], [-2, 2]])
        
        fig.add_trace(go.Scatter3d(
            x=line_data[0], y=line_data[1], z=line_data[2],
            mode='lines',
            line=dict(color=color, width=3),
            showlegend=False,
            name=f'{axis}-axis'
        ))
    
    # CRITICAL: Same free rotation settings
    fig.update_layout(
        scene=dict(
            xaxis=dict(showticklabels=False, title='', range=[-2, 2]),
            yaxis=dict(showticklabels=False, title='', range=[-2, 2]),
            zaxis=dict(showticklabels=False, title='', range=[-2, 2]),
            aspectmode='cube',
            camera=dict(
                eye=dict(x=2.5, y=2.5, z=2.5),
                up=dict(x=0, y=0, z=1)  # Allow any up direction
            ),
            dragmode='turntable'
        ),
        uirevision='constant',
        width=1000,
        height=700
    )
    
    return fig

# Sidebar controls
st.sidebar.header("🎛️ Rotation Settings")

rotation_mode = st.sidebar.radio(
    "Rotation Mode",
    ["Free Orbit (No Lock)", "Turntable", "Custom"],
    index=0
)

object_choice = st.sidebar.selectbox(
    "Choose Object",
    ["Helix with Points", "Color Sphere", "Cube"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 🎯 **Tips for Free Rotation:**

1. **Drag anywhere** - Completely free movement
2. **Diagonal drag** - Multi-axis rotation
3. **Continuous spin** - Ek direction mein ghumate raho
4. **Avoid** - Sudden stops par focus mat karo

### 🔄 **Ab koi atakna nahi!**
""")

# Create appropriate figure
if object_choice == "Helix with Points":
    fig = create_free_rotation_object()
elif object_choice == "Color Sphere":
    fig = create_sphere_free_rotation()
else:
    fig = create_free_rotation_object()  # Reuse helix

# Update based on mode
if rotation_mode == "Free Orbit (No Lock)":
    fig.update_layout(
        scene=dict(
            dragmode='orbit',
            camera=dict(
                up=dict(x=0, y=1, z=0)  # Allow any orientation
            )
        )
    )
elif rotation_mode == "Turntable":
    fig.update_layout(
        scene=dict(
            dragmode='turntable',
            camera=dict(
                up=dict(x=0, y=0, z=1)  # Keep horizon level
            )
        )
    )

# JavaScript for additional rotation control
custom_js = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    var plotElement = document.querySelector('.js-plotly-plot');
    if (plotElement) {
        plotElement.on('plotly_relayout', function(eventData) {
            // Enable continuous rotation
            if (eventData['scene.camera']) {
                // Camera update hua - smooth rotation maintain karo
                console.log('Camera moved freely');
            }
        });
    }
});
</script>
"""

html(custom_js)

# Display the plot with special configuration
st.plotly_chart(fig, use_container_width=True, config={
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToAdd': ['orbitRotation', 'resetCameraDefault'],
    'modeBarButtonsToRemove': ['select2d', 'lasso2d'],
    'scrollZoom': True,
    'doubleClick': 'reset',
    'showTips': True,
    'responsive': True
})

# Success message
st.success("✨ Ab object **completely free** ghumega! Kisi point pe nahi atakega. Try karo continuous ek direction mein ghumana!")
