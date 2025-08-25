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

# Caja de texto editable
expr = st.text_input("Escribe tu función en términos de x y y:", st.session_state.expr)
st.session_state.expr = expr  # sincronizar con lo que escriba el usuario

# -------------------------
# Teclado matemático
# -------------------------
st.write("### Teclado Matemático")

cols = st.columns(6)
buttons = [
    "x", "y", "+", "-", "*", "/",
    "(", ")", "^", "√", "sin", "cos",
    "tan", "exp", "log", "pi", "np", ","
]

for i, b in enumerate(buttons):
    if cols[i % 6].button(b):
        if b == "√":
            st.session_state.expr += "np.sqrt("
        elif b in ["sin", "cos", "tan", "exp", "log"]:
            st.session_state.expr += f"np.{b}("
        elif b == "^":
            st.session_state.expr += "**"
        elif b == "pi":
            st.session_state.expr += "np.pi"
        elif b == "np":
            st.session_state.expr += "np."
        else:
            st.session_state.expr += b
        # refrescar la página para actualizar la caja de texto
        st.experimental_rerun()

# -------------------------
# Generar malla
# -------------------------
x = np.linspace(-10, 10, 100)
y = np.linspace(-10, 10, 100)
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
            zaxis=dict(range=[np.nanmin(Z), np.nanmax(Z)])
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




