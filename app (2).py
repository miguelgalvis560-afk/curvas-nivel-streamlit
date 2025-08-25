import streamlit as st
import numpy as np
import plotly.graph_objects as go

# -------------------------
# Inicializar session_state
# -------------------------
if "expr" not in st.session_state:
    st.session_state.expr = "x**2 + y**2"

# -------------------------
# Funciones matemáticas
# -------------------------
def get_function(expr):
    def func(x, y):
        try:
            return eval(expr, {"x": x, "y": y, "np": np})
        except Exception:
            return np.nan
    return func

# -------------------------
# Interfaz
# -------------------------
st.title("Visualizador 3D y Curvas de Nivel 📊")

# -------------------------
# Lista de funciones comunes
# -------------------------
st.sidebar.title("Figuras comunes")
figura = st.sidebar.selectbox(
    "Selecciona una figura:",
    [
        "Personalizada",
        "Paraboloide circular: z = x² + y²",
        "Paraboloide hiperbólico (silla de montar): z = x² - y²",
        "Esfera: z = sqrt(25 - x² - y²)",
        "Cilindro circular: z = sqrt(25 - x²)",
        "Cilindro elíptico: z = sqrt(25 - (x²/9) - (y²/4))",
        "Hiperboloide de una hoja: z = sqrt(x² + y² - 1)",
        "Hiperboloide de dos hojas: z = sqrt(x² + y² + 1)"
    ]
)

# Asignar expresión según la figura
if figura == "Personalizada":
    expr = st.text_input("Escribe tu función en términos de x y y:", st.session_state.expr)
else:
    if figura == "Paraboloide circular: z = x² + y²":
        expr = "x**2 + y**2"
    elif figura == "Paraboloide hiperbólico (silla de montar): z = x**2 - y**2"
:
        expr = "x**2 - y**2"
    elif figura == "Esfera: z = sqrt(25 - x² - y²)":
        expr = "np.sqrt(25 - x**2 - y**2)"
    elif figura == "Cilindro circular: z = sqrt(25 - x²)":
        expr = "np.sqrt(25 - x**2)"
    elif figura == "Cilindro elíptico: z = sqrt(25 - (x²/9) - (y²/4))":
        expr = "np.sqrt(25 - (x**2/9) - (y**2/4))"
    elif figura == "Hiperboloide de una hoja: z = sqrt(x² + y² - 1)":
        expr = "np.sqrt(x**2 + y**2 - 1)"
    elif figura == "Hiperboloide de dos hojas: z = sqrt(x² + y² + 1)":
        expr = "np.sqrt(x**2 + y**2 + 1)"

st.session_state.expr = expr

# -------------------------
# Generar malla
# -------------------------
x = np.linspace(-10, 10, 200)
y = np.linspace(-10, 10, 200)
X, Y = np.meshgrid(x, y)

f = get_function(st.session_state.expr)
Z = f(X, Y)

# -------------------------
# Selector de vista
# -------------------------
view = st.radio("Selecciona vista:", ["3D", "Curvas de Nivel (2D)"])

fig = go.Figure()

if view == "3D":
    fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale="Viridis"))
    fig.update_layout(
        scene=dict(
            xaxis_title="Eje X",
            yaxis_title="Eje Y",
            zaxis_title="Eje Z",
            xaxis=dict(range=[-10, 10]),
            yaxis=dict(range=[-10, 10]),
        ),
        width=800, height=600
    )

elif view == "Curvas de Nivel (2D)":
    fig.add_trace(go.Contour(z=Z, x=x, y=y, colorscale="Viridis"))
    fig.update_layout(
        xaxis_title="Eje X",
        yaxis_title="Eje Y",
        width=800, height=600
    )

st.plotly_chart(fig, use_container_width=True)




