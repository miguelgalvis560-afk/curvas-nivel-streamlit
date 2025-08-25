import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configuración
st.set_page_config(page_title="Graficador 3D y Curvas de Nivel", layout="wide")
st.title("Graficador de Superficies 3D y Curvas de Nivel con Animación")

# Caja de texto para la función
funcion = st.text_input("Ingresa una función en términos de x e y (ejemplo: sqrt(9 - x**2 - y**2))", "sqrt(9 - x**2 - y**2)")

# Slider para rango
rango = st.slider("Selecciona el rango para x e y", 5, 20, 10)

# Opción de vista
vista = st.radio("Elige la vista", ["3D", "Curvas de Nivel"])

# Definir malla
x = np.linspace(-rango, rango, 200)
y = np.linspace(-rango, rango, 200)
X, Y = np.meshgrid(x, y)

# Intentar calcular Z
try:
    Z = eval(funcion, {"x": X, "y": Y, "np": np, "sqrt": np.sqrt, "sin": np.sin, "cos": np.cos, "exp": np.exp})

    # Caso especial: funciones que generan ±Z (esfera, cono, elipsoide, etc.)
    if np.any(Z < 0):  
        Z_pos = np.where(Z >= 0, Z, np.nan)
        Z_neg = np.where(Z <= 0, Z, np.nan)
    else:
        Z_pos, Z_neg = Z, None

    fig = go.Figure()

    if vista == "3D":
        # Superficie positiva
        fig.add_trace(go.Surface(x=X, y=Y, z=Z_pos, colorscale="Viridis", opacity=0.9))
        # Superficie negativa (si aplica)
        if Z_neg is not None:
            fig.add_trace(go.Surface(x=X, y=Y, z=Z_neg, colorscale="Viridis", opacity=0.9))

        fig.update_layout(scene=dict(
            xaxis=dict(range=[-rango, rango]),
            yaxis=dict(range=[-rango, rango]),
            zaxis=dict(range=[-rango, rango])
        ))

    elif vista == "Curvas de Nivel":
        # Animación: Z baja hacia 0
        frames = []
        steps = 20
        for i in range(steps + 1):
            factor = 1 - i / steps
            Z_anim = Z * factor
            frames.append(go.Frame(data=[go.Surface(x=X, y=Y, z=Z_anim, colorscale="Viridis", showscale=False)]))

        fig = go.Figure(
            data=[go.Surface(x=X, y=Y, z=Z, colorscale="Viridis", showscale=False)],
            frames=frames
        )

        fig.update_layout(
            updatemenus=[{
                "buttons": [
                    {"args": [None, {"frame": {"duration": 100, "redraw": True},
                                     "fromcurrent": True}], 
                     "label": "▶", "method": "animate"},
                    {"args": [[None], {"frame": {"duration": 0, "redraw": True},
                                       "mode": "immediate"}],
                     "label": "⏹", "method": "animate"}
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }]
        )

        fig.update_traces(contours_z=dict(show=True, usecolormap=True, highlightcolor="limegreen", project_z=True))

    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error en la función: {e}")
