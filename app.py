import streamlit as st
from vedo import *
import numpy as np

st.title("🎨 Vedo - Scientific Visualization")

# Create a complex object
sphere = Sphere(pos=(0,0,0), r=1, c='blue', alpha=0.5)
cube = Cube(pos=(0,0,0), side=1.5, c='red', alpha=0.3)

# Combine objects
objects = sphere + cube

# Add axes
axes = Axes(xrange=(-2,2), yrange=(-2,2), zrange=(-2,2))

# Create plotter
plt = Plotter(axes=1, offscreen=True)
plt.show(objects, axes, viewup='z')

# Convert to numpy array for Streamlit
img = plt.screenshot(asarray=True)
st.image(img, caption="3D Object (Static)")

# Note: For interactive, you'd need vedo's browser backend
