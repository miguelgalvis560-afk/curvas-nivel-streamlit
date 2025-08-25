import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("📊 Graficador de Curvas de Nivel")

# Entrada de la función
funcion = st.text_input("Escribe la función f(x,y):", "x**2 - y**2")

# Rango de valores
xmin = st.slider("x mínimo", -10, 0, -5)
xmax = st.slider("x máximo", 0, 10, 5)
ymin = st.slider("y mínimo", -10, 0, -5)
ymax = st.slider("y máximo", 0, 10, 5)

# Niveles de contorno
niveles = st.slider("Cantidad de curvas de nivel", 5, 50, 20)

# Crear malla de puntos
x = np.linspace(xmin, xmax, 200)
y = np.linspace(ymin, ymax, 200)
X, Y = np.meshgrid(x, y)

# Evaluar la función con seguridad
try:
    Z = eval(funcion, {"x": X, "y": Y, "np": np})
    
    fig, ax = plt.subplots(figsize=(6,6))
    contornos = ax.contour(X, Y, Z, levels=niveles, cmap='plasma')
    ax.clabel(contornos, inline=True, fontsize=8)
    ax.set_title(f"Curvas de nivel de f(x,y) = {funcion}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True)
    
    st.pyplot(fig)

except Exception as e:
    st.error(f"Error al evaluar la función: {e}")
