import streamlit as st
import numpy as np
import plotly.graph_objects as go

if "expr" not in st.session_state:
    st.session_state.expr = "x**2 + y**2"
if "last_view" not in st.session_state:
    st.session_state.last_view = "3D"

def get_function(expr):
    def func(x, y):
        try:
            return eval(expr, {"x": x, "y": y, "np": np})
        except Exception:
            return np.nan
    return func

st.title("Visualizador 3D Y Curvas de Nivel 📊")

figuras_dict = {
    "Personalizada": None,
    "Paraboloide circular: z = x² + y²": "x**2 + y**2",
    "Paraboloide hiperbólico (silla de montar): z = x**2 - y**2": "x**2 - y**2",
    "Esfera: z = np.sqrt(np.maximum(25 - x**2 - y**2, 0))": "np.sqrt(np.maximum(25 - x**2 - y**2, 0))",
    "Cilindro circular: z = np.sqrt(np.maximum(25 - x**2, 0))": "np.sqrt(np.maximum(25 - x**2, 0))",
    "Cilindro elíptico: z = np.sqrt(np.maximum(25 - (x**2/9) - (y**2/4), 0))": "np.sqrt(np.maximum(25 - (x**2/9) - (y**2/4), 0))",
    "Hiperboloide de una hoja: z = np.sqrt(np.maximum(x**2 + y**2 - 1, 0))": "np.sqrt(np.maximum(x**2 + y**2 - 1, 0))",
    "Hiperboloide de dos hojas: z = np.sqrt(x**2 + y**2 + 1)": "np.sqrt(x**2 + y**2 + 1)",
    "Toro: z = np.sqrt(np.maximum(1 - (np.sqrt(x**2 + y**2) - 2)**2, 0))": "np.sqrt(np.maximum(1 - (np.sqrt(x**2 + y**2) - 2)**2, 0))",
    "Cono circular: z = np.sqrt(x**2 + y**2)": "np.sqrt(x**2 + y**2)",
    "Onda senoidal: z = np.sin(np.sqrt(x**2 + y**2))": "np.sin(np.sqrt(x**2 + y**2))",
    "Catenoide: z = np.cosh(np.sqrt(x**2 + y**2))": "np.cosh(np.sqrt(x**2 + y**2))",
    "Elipsoide: z = np.sqrt(np.maximum(25 - (x**2/4) - (y**2/9), 0))": "np.sqrt(np.maximum(25 - (x**2/4) - (y**2/9), 0))",
    "Silla de montar con seno: z = np.sin(x) - np.cos(y)": "np.sin(x) - np.cos(y)"
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

animate = (
    (st.session_state.last_view == "3D" and view == "Curvas de Nivel (2D)") or
    (st.session_state.last_view == "Curvas de Nivel (2D)" and view == "3D")
)
last_view = st.session_state.last_view
st.session_state.last_view = view

if animate:
    frames = []
    n_frames = 15
    # Transición de 3D a 2D (aplanar) o de 2D a 3D (levantar)
    if last_view == "3D" and view == "Curvas de Nivel (2D)":
        # Aplana la superficie
        for i in range(n_frames + 1):
            alpha = i / n_frames
            Z_frame = Z * (1 - alpha)
            # La última frame es el contour
            frame = go.Frame(
                data=[
                    go.Surface(z=Z_frame, x=X, y=Y, colorscale="Viridis", showscale=False)
                    if alpha < 1 else
                    go.Contour(z=Z, x=x, y=y, colorscale="Viridis", contours=dict(coloring="lines"), line=dict(width=1))
                ],
                name=str(i)
            )
            frames.append(frame)
        fig = go.Figure(
            data=[go.Surface(z=Z, x=X, y=Y, colorscale="Viridis", showscale=False)],
            frames=frames
        )
    elif last_view == "Curvas de Nivel (2D)" and view == "3D":
        # Levanta la superficie desde plano
        for i in range(n_frames + 1):
            alpha = i / n_frames
            Z_frame = Z * alpha
            # La primer frame es el contour
            frame = go.Frame(
                data=[
                    go.Contour(z=Z, x=x, y=y, colorscale="Viridis", contours=dict(coloring="lines"), line=dict(width=1))
                    if alpha < 1e-6 else
                    go.Surface(z=Z_frame, x=X, y=Y, colorscale="Viridis", showscale=False)
                ],
                name=str(i)
            )
            frames.append(frame)
        fig = go.Figure(
            data=[go.Contour(z=Z, x=x, y=y, colorscale="Viridis", contours=dict(coloring="lines"), line=dict(width=1))],
            frames=frames
        )
    fig.update_layout(
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            buttons=[dict(label="▶", method="animate", args=[None, {"frame": {"duration":50, "redraw": True}, "fromcurrent": True, "transition": {"duration": 0}}])]
        )],
        width=800, height=600
    )
else:
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
            contours=dict(coloring="lines"),
            line=dict(width=1)
        ))
        fig.update_layout(
            xaxis_title="Eje X",
            yaxis_title="Eje Y",
            width=800, height=600
        )

st.plotly_chart(fig, use_container_width=True)


