import streamlit as st
import numpy as np
import plotly.graph_objects as go


if "expr" not in st.session_state:
    st.session_state.expr = "x**2 + y**2"


def get_function(expr):
    def func(x, y):
        try:
            return eval(expr, {"x": x, "y": y, "np": np})
        except Exception:
            return np.nan
    return func


st.title("Visualizador de Curvas de Nivel 📊")


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


st.sidebar.title("Figuras comunes")
figura = st.sidebar.selectbox("Selecciona una figura:", list(figuras_dict.keys()))


if figura == "Personalizada":
    expr = st.text_area("Escribe tu función en términos de x y y:", st.session_state.expr, height=50)
    if expr != st.session_state.expr:
        st.session_state.expr = expr
        st.experimental_rerun()
else:
    expr = figuras_dict[figura]
    st.session_state.expr = expr


x = np.linspace(-10, 10, 200)
y = np.linspace(-10, 10, 200)
X, Y = np.meshgrid(x, y)

f = get_function(st.session_state.expr)
Z = f(X, Y)


view = st.radio("Selecciona vista:", ["3D", "Curvas de Nivel (2D)"])

fig = go.Figure()

if view == "3D":
    fig.add_trace(go.Surface(
        z=Z, x=X, y=Y,
        colorscale="Viridis",
        showscale=False,
        opacity=0.9
    ))

    
    axis_length = 7  

   
    fig.update_layout(
    scene=dict(
        xaxis=dict(
            backgroundcolor="black",
            gridcolor="gray",
            zerolinecolor="white",
            tickfont=dict(color="red"),
            title="",
            range=[-axis_length, axis_length],
            tickmode="linear",
            dtick=1
        ),
        yaxis=dict(
            backgroundcolor="black",
            gridcolor="gray",
            zerolinecolor="white",
            tickfont=dict(color="green"),
            title="",
            range=[-axis_length, axis_length],
            tickmode="linear",
            dtick=1
        ),
        zaxis=dict(
            backgroundcolor="black",
            gridcolor="gray",
            zerolinecolor="white",
            tickfont=dict(color="blue"),
            title="",
            range=[-axis_length, axis_length],
            tickmode="linear",
            dtick=1
        ),
        aspectmode="manual", 
        aspectratio=dict(x=1, y=1, z=1) 
    ),
    paper_bgcolor="black",
    plot_bgcolor="black",
    width=1000,   # ancho de  gráfica
    height=800    # alto de gráfica
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


st.plotly_chart(fig, use_container_width=True)


