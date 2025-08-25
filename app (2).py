import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("Visualización 3D y Curvas de Nivel")

# Caja de texto para la función
func_input = st.text_input("Escribe la función f(x,y):", "x**2 + y**2")

# Botón de selección
view = st.radio("Elige la vista:", ["3D", "Curvas de Nivel"])

# Definir el rango
x = np.linspace(-10, 10, 100)
y = np.linspace(-10, 10, 100)
X, Y = np.meshgrid(x, y)

# Evaluar la función
try:
    Z = eval(func_input, {"x": X, "y": Y, "np": np})
except Exception as e:
    st.error(f"Error en la función: {e}")
    Z = np.zeros_like(X)

# Mostrar el gráfico
if view == "3D":
    fig = go.Figure(data=[go.Surface(
        z=Z, x=X, y=Y,
        colorscale="Viridis",
        showscale=True,
        lighting=dict(ambient=0.6, diffuse=0.8, specular=0.5, roughness=0.3)
    )])

    # Ajustar tamaño y ejes visibles
    fig.update_layout(
        width=800, height=700,   # Tamaño más grande
        scene=dict(
            aspectmode="cube",   # Relación de aspecto igual
            xaxis=dict(title="X", visible=True, showgrid=True, zeroline=True),
            yaxis=dict(title="Y", visible=True, showgrid=True, zeroline=True),
            zaxis=dict(title="Z", visible=True, showgrid=True, zeroline=True)
        )
    )
    st.plotly_chart(fig, use_container_width=True)

elif view == "Curvas de Nivel":
    fig = go.Figure(data=[go.Contour(
        z=Z, x=x, y=y,
        colorscale="Turbo",
        contours=dict(
            coloring="lines",
            showlabels=True
        )
    )])
    fig.update_layout(
        width=700, height=600,
        xaxis=dict(scaleanchor="y"),
        yaxis=dict(scaleanchor="x", scaleratio=1),
        title="Curvas de Nivel"
    )
    st.plotly_chart(fig, use_container_width=True)

