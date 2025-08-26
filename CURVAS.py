import streamlit as st
import numpy as np
import plotly.graph_objects as go

# -------------------------
# Inicializar session_state
# -------------------------
if "expr" not in st.session_state:
    st.session_state.expr = "x**2 + y**2"

# -------------------------
# Función para evaluar la expresión
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
st.title("Visualizador de Curvas de Nivel 📊")

# -------------------------
# Diccionario de figuras y sus expresiones
# -------------------------
figuras_dict = {
    "Personalizada": None,
    "Paraboloide circular: z = x² + y²": "x**2 + y**2",
    "Paraboloide hiperbólico (silla de montar): z = x² - y²": "x**2 - y**2",
    "Esfera: z = sqrt(25 - x² - y²)": "np.sqrt(np.maximum(25 - x**2 - y**2, 0))",
    "Cilindro circular: z = sqrt(25 - x²)": "np.sqrt(np.maximum(25 - x**2, 0))",
    "Cilindro elíptico: z = sqrt(25 - (x²/9) - (y²/4))": "np.sqrt(np.maximum(25 - (x**2/9) - (y**2/4), 0))",
    "Hiperboloide de una hoja: z = sqrt(x² + y² - 1)": "np.sqrt(np.maximum(x**2 + y**2 - 1, 0))",
    "Hiperboloide de dos hojas: z = sqrt(x² + y² + 1)": "np.sqrt(x**2 + y**2 + 1)",
    "Toro: z = sqrt(1 - (sqrt(x² + y²) - 2)²)": "np.sqrt(np.maximum(1 - (np.sqrt(x**2 + y**2) - 2)**2, 0))",
    "Cono circular: z = sqrt(x² + y²)": "np.sqrt(x**2 + y**2)",
    "Onda senoidal: z = sin(sqrt(x² + y²))": "np.sin(np.sqrt(x**2 + y**2))",
    "Catenoide: z = cosh(sqrt(x² + y²))": "np.cosh(np.sqrt(x**2 + y**2))",
    "Elipsoide: z = sqrt(25 - (x²/4) - (y²/9))": "np.sqrt(np.maximum(25 - (x**2/4) - (y**2/9), 0))",
    "Silla de montar con seno: z = sin(x) - cos(y)": "np.sin(x) - np.cos(y)"
}

# -------------------------
# Sidebar: selección de figura
# -------------------------
st.sidebar.title("Figuras comunes")
figura = st.sidebar.selectbox("Selecciona una figura:", list(figuras_dict.keys()))

# -------------------------
# Asignar expresión según selección
# -------------------------
if figura == "Personalizada":
    expr = st.text_area("Escribe tu función en términos de x y y:", st.session_state.expr, height=50)
    if expr != st.session_state.expr:
        st.session_state.expr = expr
        st.experimental_rerun()
else:
    expr = figuras_dict[figura]
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
    fig.add_trace(go.Surface(
        z=Z, x=X, y=Y,
        colorscale="Viridis",
        showscale=False,      # Ocultar barra de colores
        opacity=0.9
    ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(
                title="Eje X",
                range=[-10, 10],
                showgrid=True,
                zeroline=True,
                showline=True,
                mirror=True,
                backgroundcolor="white",
                gridcolor="lightgray",
                zerolinecolor="black"
            ),
            yaxis=dict(
                title="Eje Y",
                range=[-10, 10],
                showgrid=True,
                zeroline=True,
                showline=True,
                mirror=True,
                backgroundcolor="white",
                gridcolor="lightgray",
                zerolinecolor="black"
            ),
            zaxis=dict(
                title="Eje Z",
                showgrid=True,
                zeroline=True,
                showline=True,
                mirror=True,
                backgroundcolor="white",
                gridcolor="lightgray",
                zerolinecolor="black"
            ),
            # Cámara estilo GeoGebra
            camera=dict(
                eye=dict(x=1.8, y=1.8, z=1.2)  
            ),
            aspectmode="cube"  # Escala igual en X, Y, Z
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        width=800, height=600,
        paper_bgcolor="white"
    )

elif view == "Curvas de Nivel (2D)":
    fig.add_trace(go.Contour(
        z=Z, x=x, y=y,
        colorscale="Viridis",
        contours=dict(
            coloring="lines"  # Solo dibuja las curvas
        ),
        line=dict(width=1)
    ))
    fig.update_layout(
        xaxis_title="Eje X",
        yaxis_title="Eje Y",
        width=800, height=600,
        xaxis=dict(showgrid=True, zeroline=True),  # Cuadrícula en eje X
        yaxis=dict(showgrid=True, zeroline=True)   # Cuadrícula en eje Y
    )


# -------------------------
# Mostrar gráfico
# -------------------------
st.plotly_chart(fig, use_container_width=True)


