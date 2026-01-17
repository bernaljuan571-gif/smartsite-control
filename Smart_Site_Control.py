import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

# --- CONFIGURACIÓN TÉCNICA ---
st.set_page_config(page_title="SmartSite Control", page_icon="🏗️", layout="wide")

# --- LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🏗️ SmartSite Control")
    st.subheader("Plataforma de monitoreo inteligente")
    u, c = st.text_input("Usuario"), st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if u == "admin" and c == "1234":
            st.session_state.autenticado = True
            st.rerun()
    st.stop()

# --- SIDEBAR: GESTIÓN DE ARCHIVOS ---
with st.sidebar:
    st.header("📁 Smart Site Control")
    st.caption("Fase 1: Prototipo Virtual")
    
    st.subheader("Carga de Datos")
    archivo_excel = st.file_uploader("Excel de Seguimiento", type=["xlsx"])
    
    st.subheader("Documentación Técnica")
    archivos_adjuntos = st.file_uploader(
        "Planos (DWG/RVT/PDF) e Imágenes", 
        type=["pdf", "dwg", "rvt", "jpg", "png"], 
        accept_multiple_files=True
    )
    
    if st.button("Cerrar Sesión"):
        st.session_state.autenticado = False
        st.rerun()

# --- ESTRUCTURA DEL DASHBOARD (SEGÚN ÍNDICE DEL MOCKUP) ---
st.title("🏗️ SmartSite Control")
st.markdown("### Plataforma de monitoreo inteligente y seguimiento de obra en tiempo real")

tabs = st.tabs([
    "01 Resumen Ejecutivo", 
    "02 Integración Tecnológica", 
    "03 Registro Automatizado", 
    "04 Eficiencia Operativa", 
    "05 Indicadores de Avance", 
    "06 Seguridad y Riesgos", 
    "07 Análisis Estratégico"
])

# --- TAB 1: RESUMEN EJECUTIVO ---
with tabs[0]:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.metric("Avance Físico Actual", "88%", "+2.1%")
        st.metric("Meta de la fase", "95%")
        st.metric("Puntos de Inspección", "265", "+21")
    
    with col2:
        # Progreso de obra (Last 6 months)
        meses = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        valores = [5, 7, 8, 10, 9, 14]
        fig_prog = px.line(x=meses, y=valores, title="Progreso de obra (Last 6 months)", markers=True)
        st.plotly_chart(fig_prog, use_container_width=True)
        
    with col3:
        st.metric("Índice de Calidad", "92%", "+32%")
        st.metric("Eficiencia de Tiempos", "88%", "+14%")
        st.info("La IA ha validado un 50% de precisión geométrica respecto al modelo BIM")

# --- TAB 2: INTEGRACIÓN TECNOLÓGICA ---
with tabs[1]:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Estado de Maquinaria")
        maquinaria = {"Tipo": ["Grúas", "Excavadoras", "Volquetas", "Elevadores"], "Estado %": [12, 26, 28, 16]}
        st.table(pd.DataFrame(maquinaria))
        
        # Alertas por categoría
        fig_alert = px.bar(x=["Estructural", "Eléctrico", "Sanitarios", "Seguridad"], 
                          y=[90, 50, 30, 70], title="Alertas por Categoría", color_discrete_sequence=['orange'])
    with c2:
        st.plotly_chart(fig_alert, use_container_width=True)
        st.subheader("Geolocalización de Unidades IOT")
        st.map() # Mapa interactivo

# --- TAB 3: REGISTRO AUTOMATIZADO ---
with tabs[2]:
    m1, m2 = st.columns(2)
    with m1:
        st.subheader("Origen de los Registros")
        fig_pie = px.pie(values=[42, 58], names=["Dron", "360°"], hole=0.5, title="Distribución de Captura")
        st.plotly_chart(fig_pie)
    with m2:
        st.subheader("Categorización por IA")
        fig_ia = px.bar(x=["Estructural", "Instalaciones", "Acabados", "Seguridad"], 
                       y=[45, 28, 18, 10], title="Datos en cola para análisis")
        st.plotly_chart(fig_ia)

# --- TAB 4: EFICIENCIA OPERATIVA ---
with tabs[3]:
    st.subheader("Curva de Productividad")
    fig_prod = px.area(x=meses, y=[10, 30, 40, 50, 55, 60], title="Rendimiento del Proyecto")
    st.plotly_chart(fig_prod, use_container_width=True)
    
    st.subheader("Tiempo de Respuesta a Incidentes")
    fig_resp = px.bar(x=meses, y=[4, 6, 5, 7, 4, 6], title="Horas promedio de resolución")
    st.plotly_chart(fig_resp, use_container_width=True)

# --- TAB 5: INDICADORES DE AVANCE (DATOS REALES) ---
with tabs[4]:
    if archivo_excel:
        df = pd.read_excel(archivo_excel)
        df["Avance %"] = (df["Cantidad_Ejecutada"] / df["Cantidad_Total"] * 100).round(2)
        
        st.subheader("Análisis de Partidas de Obra")
        st.dataframe(df.style.format({"Avance %": "{:.2f}%"}), use_container_width=True)
        
        fig_cat = px.sunburst(df, path=['Área', 'Actividad'], values='Cantidad_Ejecutada', title="Distribución de Avance Real")
        st.plotly_chart(fig_cat)
    else:
        st.warning("Cargue el archivo 'Seguimiento_Obra_Ejemplo.xlsx' para visualizar el análisis dinámico.")

# --- TAB 6: SEGURIDAD Y RIESGOS ---
with tabs[5]:
    s1, s2 = st.columns(2)
    with s1:
        st.subheader("Incidentes de Seguridad")
        fig_sec = px.line(x=meses, y=[210, 160, 150, 145, 140, 80], title="Tendencia de Incidentes")
        st.plotly_chart(fig_sec)
    with s2:
        st.metric("Índice de Seguridad", "88%")
        st.metric("Tiempo respuesta médica", "5 min")
        st.progress(0.7, text="Eficiencia de Capacitación (70%)")

# --- TAB 7: ANÁLISIS ESTRATÉGICO ---
with tabs[6]:
    st.header("Hallazgos Estratégicos")
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.success("**Eficiencia en Tiempo:** Reducción del 15% en retrasos de estructura mediante IA")
        st.success("**Rentabilidad:** Ahorro proyectado del 10% al evitar demoliciones")
    with col_e2:
        st.info("**Calidad:** 92% de hitos cumplen estrictamente con el modelo BIM")
        st.info("**Recursos:** Optimización de flujo basada en Big Data")








