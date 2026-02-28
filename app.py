import streamlit as st
import numpy as np
from trafo import Variable,Vector, Rotation, Trafo
import plotly.graph_objects as go

st.title("⚡ trafo - Quaternion Math Demo")

# Create rotation using quaternions (no gimbal lock!)
rot_x = Rotation.from_axis_angle(Vector.ex(), np.pi/4)  # 45° around X
rot_y = Rotation.from_axis_angle(Vector.ey(), np.pi/3)  # 60° around Y
rot_z = Rotation.from_axis_angle(Variable.ez(), np.pi/6)  # 30° around Z

# Combine rotations
combined_rot = rot_x * rot_y * rot_z

# Apply to a point
point = Vector(1, 0, 0)
rotated_point = combined_rot.apply(point)

st.write(f"Original point: (1, 0, 0)")
st.write(f"Rotated point: ({rotated_point.x:.2f}, {rotated_point.y:.2f}, {rotated_point.z:.2f})")
