import streamlit as st
import pyvista as pv
from pyvista import examples
from streamlit_pyvista import st_pyvista

st.set_page_config(page_title="PyVista 3D Cube", layout="centered")
st.title("Fully Free-Rotate 3D Cube (Mouse / Touch)")

# Create cube
cube = pv.Cube()

# Add hover info by using labels
labels = [f"Vertex {i}" for i in range(cube.points.shape[0])]

# Create Plotter
plotter = pv.Plotter(notebook=False, off_screen=True)
plotter.add_mesh(cube, color="lightblue", opacity=0.6)
plotter.add_point_labels(cube.points, labels, point_size=10, font_size=10, text_color="blue")

# Enable interactive rotation, zoom, pan
plotter.enable_trackball_style()  # free rotation in all directions

# Render in Streamlit
st_pyvista(plotter, key="cube")
