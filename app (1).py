import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Necesario para gráficos 3D

st.title("📊 Visualización de funciones f(x,y)")

# Entrada de la función
funcion = st.text_input("Escribe la función f(x,y):", "x**2 - y**2")

# Rango de valores
xmin = st.slider("x mínimo", -10, 0, -5)
xmax = st.slider("x máximo", 0, 10, 5)
ymin = st.slider("y mínimo", -10, 0, -5)
ymax = st.slider("y máximo", 0, 10, 5)

# Tipo de gráfico
modo = st.radio("Elige el tipo de gráfico:", ("Curvas de nivel (2D)", "Superficie 3D"))

# Niveles de contorno
niveles = st.slider("Cantidad de curvas/superficie", 5, 50, 20)

# Crear malla de puntos
x = np.linspace(xmin, xmax, 200)
y = np.linspace(ymin, ymax, 200)
X, Y = np.meshgrid(x, y)

try:
    # Evaluar función con seguridad
    Z = eval(funcion, {"x": X, "y": Y, "np": np})

    if modo == "Curvas de nivel (2D)":
        fig, ax = plt.subplots(figsize=(6,6))
        contornos = ax.contour(X, Y, Z, levels=niveles, cmap="plasma")
        ax.clabel(contornos, inline=True, fontsize=8)
        ax.set_title(f"Curvas de nivel de f(x,y) = {funcion}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True)
        st.pyplot(fig)

    else:  # Superficie 3D
        fig = plt.figure(figsize=(7,6))
        ax = fig.add_subplot(111, projection="3d")
        superficie = ax.plot_surface(X, Y, Z, cmap="plasma", edgecolor="k", alpha=0.8)
        ax.set_title(f"Superficie 3D de f(x,y) = {funcion}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("f(x,y)")
        fig.colorbar(superficie, shrink=0.5, aspect=10)
        st.pyplot(fig)

except Exception as e:
    st.error(f"Error al evaluar la función: {e}")
