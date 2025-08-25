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
       "Personalizada": lambda x, y: None,
    "Paraboloide circular: z = x² + y²": lambda x, y: x**2 + y**2,
    "Paraboloide hiperbólico (silla de montar): z = x² - y²": lambda x, y: x**2 - y**2,
    "Esfera: z = sqrt(25 - x² - y²)": lambda x, y: np.sqrt(np.maximum(25 - x**2 - y**2, 0)),
    "Cilindro circular: z = sqrt(25 - x²)": lambda x, y: np.sqrt(np.maximum(25 - x**2, 0)),
    "Cilindro elíptico: z = sqrt(25 - (x²/9) - (y²/4))": lambda x, y: np.sqrt(np.maximum(25 - (x**2/9) - (y**2/4), 0)),
    "Hiperboloide de una hoja: z = sqrt(x² + y² - 1)": lambda x, y: np.sqrt(np.maximum(x**2 + y**2 - 1, 0)),
    "Hiperboloide de dos hojas: z = sqrt(x² + y² + 1)": lambda x, y: np.sqrt(x**2 + y**2 + 1),
    "Toro: z = sqrt(1 - (sqrt(x² + y²) - 2)²)": lambda x, y: np.sqrt(np.maximum(1 - (np.sqrt(x**2 + y**2) - 2)**2, 0)),
    "Cono circular: z = sqrt(x² + y²)": lambda x, y: np.sqrt(x**2 + y**2),
    "Onda senoidal: z = sin(sqrt(x² + y²))": lambda x, y: np.sin(np.sqrt(x**2 + y**2)),
    "Catenoide: z = cosh(sqrt(x² + y²))": lambda x, y: np.cosh(np.sqrt(x**2 + y**2)),
    "Elipsoide: z = sqrt(25 - (x²/4) - (y²/9))": lambda x, y: np.sqrt(np.maximum(25 - (x**2/4) - (y**2/9), 0)),
    "Silla de montar con seno: z = sin(x) - cos(y)": lambda x, y: np.sin(x) - np.cos(y)
    ]
)

# Asignar expresión según la figura
if figura == "Personalizada":
    # 🔹 Usar st.text_area para poder escribir multilinea y detectar cambios dinámicamente
    expr = st.text_area("Escribe tu función en términos de x y y:", st.session_state.expr, height=50)
    if expr != st.session_state.expr:
        st.session_state.expr = expr
        st.experimental_rerun()  # 🔹 Fuerza recarga de la app con la nueva expresión
else:
    if figura == "Paraboloide circular: z = x² + y²":
        expr = "x**2 + y**2"
    elif figura == "Paraboloide hiperbólico (silla de montar): z = x² - y²":
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
    fig.add_trace(go.Contour(
        z=Z, x=x, y=y,
        colorscale="Viridis",
        contours=dict(
            coloring="lines"  # 🔹 Solo dibuja las curvas, sin colorear
        ),
        line=dict(width=1)   # 🔹 Grosor de las curvas
    ))
    fig.update_layout(
        xaxis_title="Eje X",
        yaxis_title="Eje Y",
        width=800, height=600
    )

st.plotly_chart(fig, use_container_width=True)


