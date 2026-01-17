# =====================================================
# =====================================================
# SMARTSITE CONTROL – HACKATHON MVP
# Prototipo Inteligente de Monitoreo de Obras
# Enfoque: Innovación | Impacto | IA + IoT
# Autor: Juan Bernal – Ingeniería Civil
# =====================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="SmartSite Control", layout="wide")

# -----------------------------------------------------
# LOGIN SIMPLE (USUARIO / CONTRASEÑA)
# -----------------------------------------------------

USUARIO_CORRECTO = "admin"
CLAVE_CORRECTA = "1234"

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 Acceso a SmartSite Control")
    st.subheader("Dashboard de Monitoreo Inteligente de Obras")

    usuario = st.text_input("Usuario")
    clave = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if usuario == USUARIO_CORRECTO and clave == CLAVE_CORRECTA:
            st.session_state.autenticado = True
            st.success("Acceso concedido")
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

    st.stop()

# -----------------------------------------------------
# ENCABEZADO
# -----------------------------------------------------
st.title("🚧 SMARTSITE CONTROL")
st.subheader("Monitoreo Inteligente de Obras con IA + IoT")
st.markdown("**Hackathon MVP | Innovación en Construcción**")

st.divider()

# -----------------------------------------------------
# KPIs CLAVE (IMPACTO INMEDIATO)
# -----------------------------------------------------
st.header("📊 Indicadores Clave en Tiempo Real")

col1, col2, col3, col4 = st.columns(4)

avance = random.randint(60, 95)
calidad = random.randint(85, 98)
seguridad = random.randint(90, 100)
ahorro = random.randint(5, 15)

col1.metric("Avance Global", f"{avance} %")
col2.metric("Índice de Calidad", f"{calidad} %")
col3.metric("Seguridad Operativa", f"{seguridad} %")
col4.metric("Ahorro Proyectado", f"{ahorro} %")

st.divider()

# -----------------------------------------------------
# PROGRESO PREDICTIVO (IA SIMULADA)
# -----------------------------------------------------
st.header("🤖 Predicción de Avance por IA")

meses = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
real = np.cumsum(np.random.randint(5, 15, 6))
pred = real + np.random.randint(2, 6, 6)

fig1, ax1 = plt.subplots()
ax1.plot(meses, real, label="Avance Real", marker='o')
ax1.plot(meses, pred, linestyle='--', label="Predicción IA")
ax1.set_ylim(0, 100)
ax1.legend()

st.pyplot(fig1)

st.info("La IA proyecta el avance futuro y detecta retrasos antes de que ocurran.")

st.divider()

# -----------------------------------------------------
# MONITOREO IoT – MAQUINARIA
# -----------------------------------------------------
st.header("📡 Estado de Maquinaria (IoT)")

maquinaria = ["Grúas", "Excavadoras", "Volquetas", "Elevadores", "Retroexcavadoras"]
uso = np.random.randint(10, 40, len(maquinaria))

fig2, ax2 = plt.subplots()
ax2.bar(maquinaria, uso)
ax2.set_ylabel("Uso (%)")

st.pyplot(fig2)

st.success("Sensores IoT permiten redistribuir equipos en tiempo real.")

st.divider()

# -----------------------------------------------------
# -----------------------------------------------------
# REGISTRO AUTOMATIZADO – DRONES
# -----------------------------------------------------
st.header("🚁 Registro Automatizado con Drones y Visión Artificial")

col5, col6 = st.columns(2)

with col5:
    registros = pd.DataFrame({
        "Fuente": ["Drones", "Cámaras 360°"],
        "Cobertura (%)": [58, 42]
    })
    st.bar_chart(registros.set_index("Fuente"))

with col6:
    st.write("✔ Registro 360° sin puntos ciegos")
    st.write("✔ Eliminación total del registro manual")
    st.write("✔ Evidencia automática para fiscalización")

st.divider()

# -----------------------------------------------------
# CARGA DE ARCHIVOS (DOCUMENTACIÓN DE OBRA)
# -----------------------------------------------------
st.header("📂 Carga de Archivos de Obra")

st.write("Suba evidencias como planos, informes, fotos o reportes técnicos.")

archivos = st.file_uploader(
    "Seleccione uno o varios archivos",
    type=["pdf", "jpg", "png", "xlsx", "docx"],
    accept_multiple_files=True
)

if archivos:
    for archivo in archivos:
        st.success(f"Archivo cargado: {archivo.name}")
        st.write(f"Tipo: {archivo.type}")
        st.write(f"Tamaño: {round(archivo.size / 1024, 2)} KB")

st.info("Los archivos quedan asociados al proyecto para trazabilidad y control de calidad.")

st.divider()

# -----------------------------------------------------
# SEGURIDAD INTELIGENTE
# -----------------------------------------------------
st.header("🦺 Seguridad Predictiva")

riesgos = {
    "Trabajo en Altura": random.randint(0, 5),
    "Maquinaria Pesada": random.randint(0, 5),
    "Riesgo Eléctrico": random.randint(0, 5)
}

st.bar_chart(pd.DataFrame.from_dict(riesgos, orient='index'))

st.warning("El sistema genera alertas antes de que ocurra un incidente.")

st.divider()
# -----------------------------------------------------
st.header("🌍 Impacto del Sistema")

st.write("• Reduce accidentes laborales a cero")
st.write("• Optimiza costos y plazos de obra")
st.write("• Digitaliza completamente la supervisión")
st.write("• Aplica IA y Big Data a la Ingeniería Civil")

st.divider()

# -----------------------------------------------------
# PROPUESTA DE VALOR
# -----------------------------------------------------
st.header("🚀 Propuesta de Valor")

st.success("SmartSite Control transforma la obra tradicional en una obra inteligente,
permitiendo decisiones basadas en datos, no en suposiciones.")

st.caption("Smart Construction | Ecuador")


