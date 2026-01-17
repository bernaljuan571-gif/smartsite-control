import streamlit as st
import pandas as pd
import io
import plotly.express as px # Usaremos Plotly para que los gráficos se parezcan a tu mockup
from datetime import datetime

# -----------------------------------------------------
# CONFIGURACIÓN ESTÉTICA (Basada en tu Mockup)
# -----------------------------------------------------
st.set_page_config(page_title="SmartSite Control", page_icon="🏗️", layout="wide")

# Estilo para imitar el modo oscuro de tu presentación
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------
# LOGIN Y CONTROL DE ACCESO
# -----------------------------------------------------
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🏗️ SmartSite Control")
    st.subheader("Plataforma de monitoreo inteligente")
    with st.container():
        usuario = st.text_input("Usuario")
        clave = st.text_input("Contraseña", type="password")
        if st.button("Ingresar al Sistema"):
            if usuario == "admin" and clave == "1234":
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
    st.stop()

# -----------------------------------------------------
# BARRA LATERAL Y PLANTILLA
# -----------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4342/4342728.png", width=100)
    st.header("SmartSite Control")
    st.write("**Fase 1: Prototipo Virtual**")
    
    # Generador de Plantilla
    df_plantilla = pd.DataFrame({
        "Actividad": ["Zapata Z1", "Columna C1", "Losa N1", "Pintura"],
        "Área": ["Estructural", "Estructural", "Estructural", "Acabados"],
        "Unidad": ["m3", "m3", "m2", "m2"],
        "Cantidad_Total": [10, 5, 100, 200],
        "Cantidad_Ejecutada": [8, 2, 10, 0]
    })
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_plantilla.to_excel(writer, index=False)
    
    st.download_button("📥 Descargar Formato Excel", data=output.getvalue(), file_name="formato_obra.xlsx")
    
    st.divider()
    archivos_pdf = st.file_uploader("Adjuntar Documentación (PDF)", type=["pdf"], accept_multiple_files=True)

# -----------------------------------------------------
# CUERPO PRINCIPAL - DASHBOARD ESTILO MOCKUP
# -----------------------------------------------------
st.title("📊 Dashboard de Monitoreo Real")
archivo = st.file_uploader("Suba el archivo de seguimiento actualizado", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)
    df["Porcentaje_Avance"] = (df["Cantidad_Ejecutada"] / df["Cantidad_Total"] * 100).round(2)
    avance_global = df["Porcentaje_Avance"].mean()

    # 1. RESUMEN EJECUTIVO (Fila de métricas)
    st.header("01 Resumen Ejecutivo") # Referencia a tu contenido [cite: 9]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avance Físico Actual", f"{avance_global:.1f}%", "+2.1%")
    col2.metric("Índice de Calidad", "92%", "+32%") # Datos fijos del mockup para demo [cite: 42]
    col3.metric("Eficiencia de Tiempos", "88%", "+14%") # [cite: 49]
    col4.metric("Partidas Activas", len(df))

    st.divider()

    # 2. INDICADORES DE AVANCE Y GRÁFICOS (Fila de gráficos)
    st.header("05 Indicadores de Avance") # Referencia [cite: 10]
    c_izq, c_der = st.columns(2)

    with c_izq:
        # Gráfico de barras por Área (como en tu mockup de Categorización)
        avance_area = df.groupby("Área")["Porcentaje_Avance"].mean().reset_index()
        fig_barra = px.bar(avance_area, x='Área', y='Porcentaje_Avance', 
                           title="Progreso por Categoría (IA)",
                           color='Porcentaje_Avance', color_continuous_scale='Blues')
        st.plotly_chart(fig_barra, use_container_width=True)

    with c_der:
        # Simulación de Curva de Productividad 
        # Aquí usamos datos ficticios para mostrar la tendencia que tienes en el PDF
        df_tendencia = pd.DataFrame({
            "Mes": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Avance": [10, 30, 45, 60, 75, avance_global]
        })
        fig_linea = px.line(df_tendencia, x="Mes", y="Avance", title="Curva de Productividad", markers=True)
        st.plotly_chart(fig_linea, use_container_width=True)

    # 3. ALERTAS Y RANKING
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.header("🚨 Alertas Técnicas") # [cite: 72]
        criticos = df[df["Porcentaje_Avance"] < 50]
        for _, fila in criticos.iterrows():
            st.warning(f"Bajo avance en {fila['Actividad']} ({fila['Área']}): {fila['Porcentaje_Avance']:.2f}%")
        if criticos.empty:
            st.success("✅ No se detectan anomalías estructurales.")

    with col_b:
        st.header("🏆 Ranking de Frentes") # [cite: 14]
        ranking = avance_area.sort_values(by="Porcentaje_Avance", ascending=False)
        ranking["Porcentaje_Avance"] = ranking["Porcentaje_Avance"].map("{:.2f}%".format)
        st.table(ranking)

    # 4. DOCUMENTACIÓN ADJUNTA
    if archivos_pdf:
        st.header("📑 Documentación Registrada")
        for pdf in archivos_pdf:
            st.info(f"Archivo: {pdf.name} - Sincronizado a la nube") # [cite: 97]

else:
    # Pantalla de bienvenida imitando el mockup vacío
    st.info("Bienvenido a SmartSite Control. Por favor, cargue los datos de obra para generar el análisis estratégico.")
    st.image("https://img.freepik.com/premium-vector/data-analysis-concept-illustration_639664-162.jpg", width=500)








