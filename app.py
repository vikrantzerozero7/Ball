import streamlit as st
import pyvista as pv
from stpyvista import stpyvista

# Create a plotter
plotter = pv.Plotter(window_size=[800, 600])
plotter.background_color = 'white'

# Create a mesh (cube, sphere, etc.)
mesh = pv.Cube()
plotter.add_mesh(mesh, color='cyan', opacity=0.6)

# Add axes for reference
plotter.show_bounds(grid=True)

# Display in Streamlit
stpyvista(plotter, key="pv_cube")
