import streamlit as st
import numpy as np
import plotly.graph_objects as go
from sympy import sympify, symbols, lambdify

# Variables simbólicas
x, y, z = symbols('x y z')

st.title("Visualizador 3D y curvas de nivel")

# Lista de figuras comunes (incluyendo trigonométricas)
figura = st.selectbox("Elige una figura:", [
    "Esfera: x**2 + y**2 + z**2 - 25",
    "Elipsoide: (x**2)/9 + (y**2)/4 + (z**2)/16 - 1",
    "Cilindro circular: x**2 + y**2 - 9",
    "Cilindro elíptico: (x**2)/9 + (y**2)/4 - 1",
    "Cono: z**2 - x**2 - y**2",
    "Hiperboloide de una hoja: x**2/9 + y**2/9 - z**2/16 - 1",
    "Hiperboloide de dos hojas: z**2/16 - x**2/9 - y**2/9 - 1",
    "Paraboloide elíptico: z - (x**2/9 + y**2/4)",
    "Paraboloide hiperbólico (silla de montar): z - (x**2 - y**2)",
    "Seno: z - sin(x)",
    "Coseno: z - cos(x)",
    "Tangente: z - tan(x)",
    "Exponencial: z - exp(x)",
    "Raíz cuadrada: z - sqrt(x**2 + y**2)"
])

# Caja de texto editable con la ecuación seleccionada
formula = st.text_input("Escribe o edita la función f(x,y,z)=0:", figura.split(": ")[1])

# Crear grilla
X = np.linspace(-10, 10, 100)
Y = np.linspace(-10, 10, 100)
X, Y = np.meshgrid(X, Y)

try:
    expr = sympify(formula)
    f = lambdify((x, y, z), expr, 'numpy')

    # Evaluar para 3D (isocontorno)
    Z = np.linspace(-10, 10, 100)
    values = np.zeros((len(X), len(Y), len(Z)))

    for k, z_val in enumerate(Z):
        values[:, :, k] = f(X, Y, z_val)

    # Selección de vista
    vista = st.radio("Selecciona vista:", ["3D", "Curvas de nivel (2D)"])

    if vista == "3D":
        fig = go.Figure(data=go.Isosurface(
            x=X.flatten(),
            y=Y.flatten(),
            z=np.repeat(Z, X.shape[0]*X.shape[1]),
            value=values.flatten(),
            isomin=-0.01,
            isomax=0.01,
            surface_count=2,
            caps=dict(x_show=False, y_show=False, z_show=False)
        ))
        fig.update_layout(
            scene=dict(
                xaxis_title="X",
                yaxis_title="Y",
                zaxis_title="Z"
            ),
            width=900, height=700
        )
        st.plotly_chart(fig)

    else:  # Curvas de nivel
        Z_vals = f(X, Y, 0)
        fig = go.Figure(data=go.Contour(
            z=Z_vals,
            x=np.linspace(-10, 10, 100),
            y=np.linspace(-10, 10, 100),
            contours=dict(
                coloring='lines'  # 👈 Solo líneas, sin relleno
            ),
            line_smoothing=0.85
        ))
        fig.update_layout(
            xaxis_title="Eje X",
            yaxis_title="Eje Y",
            width=700, height=700
        )
        st.plotly_chart(fig)

except Exception as e:
    st.error(f"Error en la fórmula: {e}")


