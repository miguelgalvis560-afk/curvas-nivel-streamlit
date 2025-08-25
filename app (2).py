import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math

st.set_page_config(page_title="Visualizador de Superficies", layout="wide")

# --- Funciones corregidas ---
def paraboloide(x, y):
    return x**2 + y**2

def hiperboloide(x, y):
    return x**2 - y**2

def cono(x, y):
    return np.sqrt(x**2 + y**2)

def cilindro(x, y):
    r = 5
    z2 = r**2 - x**2
    z2[z2 < 0] = np.nan
    return np.sqrt(z2)

def cilindro_eliptico(x, y):
    a, b, h = 3, 2, 5
    inside = 1 - (x/a)**2 - (y/b)**2
    inside[inside < 0] = np.nan
    return np.sqrt(inside) * h

# Diccionario de funciones
funciones = {
    "Paraboloide": paraboloide,
    "Hiperboloide": hiperboloide,
    "Cono": cono,
    "Cilindro": cilindro,
    "Cilindro Elíptico": cilindro_eliptico,
}

# --- Interfaz ---
st.title("📊 Visualizador Interactivo de Superficies y Curvas de Nivel")

opcion = st.selectbox("Elige una función:", list(funciones.keys()) + ["Personalizada"])
view = st.radio("Vista:", ["3D", "Curvas de Nivel"])

# Caja de texto para fórmulas
formula = ""
if opcion == "Personalizada":
    formula = st.text_input("Escribe tu fórmula en función de x, y (ej: x**2 + y**2)", "x**2 + y**2")

    # Teclado estilo GeoGebra
    botones = ["x", "y", "+", "-", "*", "/", "**", "sqrt(", "sin(", "cos(", "tan(", "exp(", "log("]
    cols = st.columns(len(botones))
    for i, b in enumerate(botones):
        if cols[i].button(b):
            formula += b
            st.session_state["formula"] = formula

# --- Generación de datos ---
x = np.linspace(-10, 10, 200)
y = np.linspace(-10, 10, 200)
X, Y = np.meshgrid(x, y)

if opcion == "Personalizada" and formula:
    try:
        Z = eval(formula, {"x": X, "y": Y, "np": np, "sqrt": np.sqrt, 
                           "sin": np.sin, "cos": np.cos, "tan": np.tan, 
                           "exp": np.exp, "log": np.log})
    except Exception as e:
        st.error(f"Error en la fórmula: {e}")
        Z = np.zeros_like(X)
else:
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
            scaleanchor="y"
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


