import numpy as np
from pytransform3d import rotations as pr
import streamlit as st

st.title("🔬 pytransform3d - Gimbal Lock Analysis")

# Check if angles are near gimbal lock
angles = np.array([np.pi/2, 0.1, 0.2])  # Euler angles

# Check for gimbal lock
is_near_lock = pr.euler_near_gimbal_lock(
    angles, 
    i=0, j=1, k=2,  # Axis order
    tolerance=1e-6
)

st.write(f"Angles: {angles}")
st.write(f"Near Gimbal Lock: {is_near_lock}")

# Convert to quaternion (safe representation)
q = pr.quaternion_from_euler(angles, 0, 1, 2)
st.write(f"Quaternion: {q}")
