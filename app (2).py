import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Visualizador de Superficies", layout="wide")

# --- Funciones disponibles ---
def paraboloide(x, y):
    return x**2 + y**2

def hiperboloide(x, y):
    return x**2 - y**2

def cono(x, y):
    return np.sqrt(x**2 + y**2)

def cilindro(x, y):
    return np.where(x**2 + y**2 <= 25, 10, np.nan)

def cilindro_eliptico(x, y):
    return np.where((x/3)**2 + (y/2)**2 <= 1, 10, np.nan)

# Diccionario de funciones
funciones = {
    "Paraboloide": paraboloide,
    "Hiperboloide": hiperboloide,
    "Cono": cono,
    "Cilindro": cilindro,
    "Cilindro Elíptico": cilindro_eliptico
}

# --- Interfaz ---
st.title("📊 Visualizador Interactivo de Superficies y Curvas de Nivel")

opcion = st.selectbox("Elige una función:", list(funciones.keys()))
view = st.radio("Vista:", ["3D", "Curvas de Nivel"])

# --- Generación de datos ---
x = np.linspace(-10, 10, 100)
y = np.linspace(-10, 10, 100)
X, Y = np.meshgrid(x, y)
Z = funciones[opcion](X, Y)

# --- Graficar ---
if view == "3D":
    fig = go.Figure(data=[go.Surface(z=Z, x=x, y=y, colorscale="Viridis")])
    fig.update_layout(
        scene=dict(
            xaxis=dict(title="X", visible=True),
            yaxis=dict(title="Y", visible=True),
            zaxis=dict(title="Z", visible=True),
        ),
        width=800, height=700,
        title=f"Superficie 3D: {opcion}"
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

    # Ajuste de ejes en R²
    fig.update_layout(
        width=700, height=600,
        xaxis=dict(
            title="Eje X",
            showgrid=True,
            zeroline=True,
            scaleanchor="y"  # proporción 1:1
        ),
        yaxis=dict(
            title="Eje Y",
            showgrid=True,
            zeroline=True,
            scaleratio=1
        ),
        title=f"Curvas de Nivel en R²: {opcion}"
    )

    st.plotly_chart(fig, use_container_width=True)


