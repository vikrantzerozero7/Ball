import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Interactive 3D Cube", layout="centered")
st.title("Touch / Drag to Rotate 3D Cube")

# Cube vertices
x = [0, 0, 1, 1, 0, 0, 1, 1]
y = [0, 1, 1, 0, 0, 1, 1, 0]
z = [0, 0, 0, 0, 1, 1, 1, 1]

# Hover text for vertices
hover_text = [f"Vertex {i}" for i in range(8)]

# Scatter for vertices
scatter = go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='markers+text',
    marker=dict(size=6, color='blue'),
    text=hover_text,
    textposition='top center',
    hoverinfo='text'
)

# Define cube faces
faces = [
    [0, 1, 2, 3],  # bottom
    [4, 5, 6, 7],  # top
    [0, 1, 5, 4],  # side 1
    [1, 2, 6, 5],  # side 2
    [2, 3, 7, 6],  # side 3
    [3, 0, 4, 7]   # side 4
]

# Mesh for cube faces
mesh = go.Mesh3d(
    x=x,
    y=y,
    z=z,
    color='lightblue',
    opacity=0.5,
    i=[face[0] for face in faces],
    j=[face[1] for face in faces],
    k=[face[2] for face in faces],
    hoverinfo='skip'
)

# Combine into figure
fig = go.Figure(data=[mesh, scatter])

fig.update_layout(
    scene=dict(
        xaxis=dict(title='X', range=[-0.5, 1.5]),
        yaxis=dict(title='Y', range=[-0.5, 1.5]),
        zaxis=dict(title='Z', range=[-0.5, 1.5])
    ),
    margin=dict(l=0, r=0, b=0, t=0)
)

# Render in Streamlit
st.plotly_chart(fig, use_container_width=True)
