import streamlit as st
import pyvista as pv

st.title("Fully Free-Rotate 3D Cube with PyVista")

# Create cube
cube = pv.Cube()

# Plotter
plotter = pv.Plotter(off_screen=True)
plotter.add_mesh(cube, color="lightblue", opacity=0.6)
plotter.enable_trackball_style()  # free rotation

# Export interactive HTML
html_file = "cube.html"
plotter.show(jupyter_backend="static", auto_close=False, window_size=[400, 400])
plotter.export_html(html_file)

# Render in Streamlit via iframe
st.components.v1.iframe(src=html_file, width=500, height=500)
