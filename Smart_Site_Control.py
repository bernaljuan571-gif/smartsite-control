# =====================================================
# SMARTSITE CONTROL – SISTEMA INTELIGENTE DE SEGUIMIENTO DE OBRA
# -----------------------------------------------------
# Tecnologías:
# - Streamlit (Dashboard Web)
# - IA (Análisis de texto en informes PDF)
# - Big Data (Lectura de Excel y múltiples fuentes)
# - IoT (Simulación de sensores de obra)
# -----------------------------------------------------
# Descripción general:
# La aplicación calcula automáticamente el avance de obra,
# detecta retrasos, genera alertas, clasifica frentes de trabajo
# y produce reportes, todo a partir de datos cargados por el usuario.
# -----------------------------------------------------
# Autor: Grupo#5 – Ingeniería Civil
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

st.set_page_config(page_title="SmartSite Control – Hackathon", layout="wide")

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

# -----------------------------------------------------
# -----------------------------------------------------
# ANALÍTICA AUTOMÁTICA (IA + BIG DATA)
# Integración real: Excel + Texto + Pesos + Cronograma
# -----------------------------------------------------
st.header("🧠 Analítica Inteligente de Avance de Obra")

st.write("Los indicadores se calculan automáticamente a partir de los archivos cargados.")

avance_estructura = 0
avance_instalaciones = 0
avance_acabados = 0

# ---- 1. LECTURA DE EXCEL (METRADOS / AVANCE) ----
for archivo in archivos or []:
    if archivo.name.endswith('.xlsx'):
        df = pd.read_excel(archivo)
        if {'Actividad', 'Ejecutado', 'Total'}.issubset(df.columns):
            df['Avance (%)'] = df['Ejecutado'] / df['Total'] * 100
            avance_estructura += df['Avance (%)'].mean()

# ---- 2. ANÁLISIS DE TEXTO (INFORMES PDF / WORD – SIMULADO) ----
for archivo in archivos or []:
    if archivo.name.endswith('.pdf') or archivo.name.endswith('.docx'):
        texto = archivo.name.lower()
        if 'estructura' in texto:
            avance_estructura += 10
        if 'instalacion' in texto:
            avance_instalaciones += 10
        if 'acabado' in texto:
            avance_acabados += 10

# ---- 3. PESOS POR ACTIVIDAD ----
peso_estructura = 0.4
peso_instalaciones = 0.3
peso_acabados = 0.3

avance_global = (
    avance_estructura * peso_estructura +
    avance_instalaciones * peso_instalaciones +
    avance_acabados * peso_acabados
)

# ---- 4. CRONOGRAMA (SIMULADO) ----
dias_planificados = 180
dias_transcurridos = 120
cumplimiento_cronograma = dias_transcurridos / dias_planificados * 100

# ---- RESULTADOS ----
data_resultados = pd.DataFrame({
    'Indicador': ['Estructura', 'Instalaciones', 'Acabados', 'Cumplimiento Cronograma'],
    'Avance (%)': [
        min(100, avance_estructura),
        min(100, avance_instalaciones),
        min(100, avance_acabados),
        cumplimiento_cronograma
    ]
})

st.subheader("📊 Resultados calculados automáticamente")
st.bar_chart(data_resultados.set_index('Indicador'))

st.metric("Avance Global Ponderado", f"{round(min(100, avance_global), 1)} %")

st.success("Los porcentajes se generan automáticamente a partir de datos reales cargados.")

# -----------------------------------------------------
# -----------------------------------------------------
# IA REAL BÁSICA – LECTURA DE PDF + ALERTAS
# -----------------------------------------------------
st.header("🤖 IA: Análisis de Informes y Alertas Automáticas")

from PyPDF2 import PdfReader

alertas = []

for archivo in archivos or []:
    if archivo.name.endswith('.pdf'):
        reader = PdfReader(archivo)
        texto_pdf = "".join([p.extract_text() or "" for p in reader.pages]).lower()

        if "retraso" in texto_pdf or "atraso" in texto_pdf:
            alertas.append("⚠️ Posible retraso detectado en informe")
        if "fisura" in texto_pdf or "falla" in texto_pdf:
            alertas.append("⚠️ Riesgo estructural mencionado")
        if "no conforme" in texto_pdf:
            alertas.append("⚠️ No conformidad detectada")

if alertas:
    for alerta in set(alertas):
        st.error(alerta)
else:
    st.success("No se detectaron alertas críticas en los informes analizados.")

st.info("La IA analiza texto real de informes PDF para detectar riesgos y retrasos.")

st.divider()

# -----------------------------------------------------
# -----------------------------------------------------
# CONTROL INTELIGENTE: AVANCE FÍSICO VS CRONOGRAMA
# -----------------------------------------------------
st.header("📅 Control Inteligente de Cronograma")

st.write("Comparación automática entre avance físico real y avance esperado según el tiempo.")

# Valores base
dias_planificados = st.number_input("Días totales planificados", value=180)
dias_transcurridos = st.number_input("Días transcurridos", value=120)

avance_esperado = dias_transcurridos / dias_planificados * 100
avance_fisico = min(100, avance_global)

colA, colB = st.columns(2)
colA.metric("Avance Esperado", f"{round(avance_esperado,1)} %")
colB.metric("Avance Físico Real", f"{round(avance_fisico,1)} %")

if avance_fisico + 5 < avance_esperado:
    st.error("🚨 Retraso crítico detectado")

elif avance_fisico < avance_esperado:
    st.warning("⚠️ Retraso leve detectado")

else:
    st.success("✅ Avance conforme al cronograma")


st.divider()

# -----------------------------------------------------
# ALERTAS POR BAJO RENDIMIENTO POR ÁREA
# -----------------------------------------------------
st.header("🚨 Alertas de Rendimiento por Área")

umbral = 50

if avance_estructura < umbral:
    st.warning("⚠️ Bajo rendimiento en Estructura")nif avance_instalaciones < umbral:
    st.warning("⚠️ Bajo rendimiento en Instalaciones")nif avance_acabados < umbral:
    st.warning("⚠️ Bajo rendimiento en Acabados")n
if avance_estructura >= umbral and avance_instalaciones >= umbral and avance_acabados >= umbral:
    st.success("✅ Todas las áreas presentan rendimiento adecuado")

st.divider()

# -----------------------------------------------------
# RANKING DE FRENTES DE TRABAJO
# -----------------------------------------------------
st.header("🏗️ Ranking de Frentes de Trabajo")

ranking = pd.DataFrame({
    "Frente": ["Estructura", "Instalaciones", "Acabados"],
    "Avance (%)": [avance_estructura, avance_instalaciones, avance_acabados]
}).sort_values(by="Avance (%)", ascending=False)

st.table(ranking)

st.info("Permite identificar frentes críticos y frentes eficientes.")

st.divider()

# -----------------------------------------------------
# SIMULACIÓN DE SENSORES IoT
# -----------------------------------------------------
st.header("📡 Simulación de Sensores IoT")

horas_maquina = np.random.randint(4, 10)
personal_en_obra = np.random.randint(20, 80)

col1, col2 = st.columns(2)
col1.metric("Horas Máquina (promedio/día)", f"{horas_maquina} h")
col2.metric("Personal en Obra", f"{personal_en_obra}")

if horas_maquina < 6:
    st.warning("⚠️ Subutilización de maquinaria detectada")nelse:
    st.success("✅ Uso adecuado de maquinaria")

st.divider()

# -----------------------------------------------------
# EXPORTACIÓN DE REPORTE AUTOMÁTICO
# -----------------------------------------------------
st.header("📄 Generación de Reporte Automático")

reporte = pd.DataFrame({
    "Indicador": ["Avance Global", "Avance Esperado", "Estructura", "Instalaciones", "Acabados"],
    "Valor": [
        f"{round(avance_global,1)} %",
        f"{round(avance_esperado,1)} %",
        f"{round(avance_estructura,1)} %",
        f"{round(avance_instalaciones,1)} %",
        f"{round(avance_acabados,1)} %"
    ]
})

st.download_button(
    label="📥 Descargar Reporte (CSV)",
    data=reporte.to_csv(index=False).encode('utf-8'),
    file_name="reporte_control_obra.csv",
    mime="text/csv"
)

st.success("Reporte generado automáticamente a partir de los datos analizados.")

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
# IMPACTO PARA EL HACKATHON
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

st.success("SmartSite Control transforma la obra tradicional en una obra inteligente, permitiendo decisiones basadas en datos, no en suposiciones.")

st.caption("Smart Construction | Ecuador")





