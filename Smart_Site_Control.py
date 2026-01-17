import streamlit as st
import pandas as pd
import plotly.express as px
import io
from PIL import Image

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="SmartSite Control", page_icon="🏗️", layout="wide")

st.markdown("""
    <style>
    .stMetric { border-left: 5px solid #1E3A8A; background-color: #f0f2f6; padding: 10px; border-radius: 5px; }
    .main { background-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ACCESO ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🏗️ SmartSite Control")
    u, c = st.text_input("Usuario"), st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if u == "admin" and c == "1234":
            st.session_state.autenticado = True
            st.rerun()
    st.stop()

# --- 3. GUÍA Y PLANTILLA ---
st.title("🏗️ SmartSite Control")
st.caption("Plataforma de monitoreo inteligente y seguimiento de obra en tiempo real")

with st.expander("📥 Descargar Plantilla y Ver Guía de Modelos"):
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Modelo de Seguimiento (Excel)**")
        df_temp = pd.DataFrame({
            "Actividad": ["Zapata Z1"], "Área": ["Estructural"], 
            "Unidad": ["m3"], "Cantidad_Total": [100.0], "Cantidad_Ejecutada": [50.0]
        })
        st.dataframe(df_temp, hide_index=True)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_temp.to_excel(writer, index=False)
        st.download_button("Descargar Plantilla Maestra", data=buffer.getvalue(), file_name="Plantilla_SmartSite.xlsx")
    with col_b:
        st.write("**Modelos Técnicos Aceptados**")
        st.info("PDF (Planos), RVT (Revit), DWG (AutoCAD), JPG/PNG (Fotos de Obra)")

st.divider()

# --- 4. CARGA DE ARCHIVOS ---
with st.sidebar:
    st.header("📂 Panel de Carga")
    archivo_excel = st.file_uploader("1. Excel de Seguimiento", type=["xlsx"])
    archivos_soporte = st.file_uploader("2. Documentación/Fotos", type=["pdf", "dwg", "rvt", "jpg", "png"], accept_multiple_files=True)
    if st.button("Cerrar Sesión"):
        st.session_state.autenticado = False
        st.rerun()

# --- 5. PROCESAMIENTO Y DASHBOARD ---
if archivo_excel:
    df = pd.read_excel(archivo_excel)
    df["Avance %"] = (df["Cantidad_Ejecutada"] / df["Cantidad_Total"] * 100).round(2)
    avance_global = df["Avance %"].mean()

    # TABS SEGÚN MOCKUP
    tabs = st.tabs(["01 Resumen", "02 Integración Tech", "03 Registro IA", "04 Eficiencia Op.", "05 Indicadores", "06 Seguridad", "07 Estrategia"])

    with tabs[0]:
        st.header("01 Resumen Ejecutivo")
        c1, c2, c3 = st.columns(3)
        c1.metric("Avance Físico Actual", f"{avance_global:.2f}%")
        c2.metric("Puntos de Inspección", "265", "+21") [cite: 39-40]
        c3.metric("Índice de Calidad", "92%", "+32%") [cite: 41-42]

    with tabs[1]:
        st.header("02 Integración Tecnológica")
        col_m1, col_m2 = st.columns([1, 1])
        with col_m1:
            st.subheader("Estado de Maquinaria (Sensores IoT)") [cite: 53, 87]
            maq_data = {"Equipo": ["Grúas", "Excavadoras", "Volquetas", "Retroexcavadoras"], "Uso %": [12, 26, 28, 18]} [cite: 57, 62, 70, 79]
            st.plotly_chart(px.bar(maq_data, x="Equipo", y="Uso %", color="Equipo", color_discrete_sequence=px.colors.qualitative.Prism))
        with col_m2:
            st.subheader("Geolocalización de Unidades") [cite: 87]
            # Mapa centrado en Ecuador (Guayaquil/Quito) [cite: 272]
            map_data = pd.DataFrame({'lat': [-2.1894, -0.1807], 'lon': [-79.8891, -78.4678]})
            st.map(map_data)

    with tabs[2]:
        st.header("03 Registro Automatizado")
        if archivos_soporte:
            for arc in archivos_soporte:
                if arc.type in ["image/jpeg", "image/png"]:
                    st.image(arc, caption=f"Categorización por IA: {arc.name}", use_container_width=True)
                else:
                    st.success(f"📄 Archivo sincronizado: {arc.name}")
        else:
            st.info("Cargue imágenes de la obra para validación geométrica contra el modelo BIM.") [cite: 47]

    with tabs[3]:
        st.header("04 Eficiencia Operativa")
        st.subheader("Curva de Productividad") [cite: 136]
        # Curva histórica que termina en el avance actual
        hist = {"Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun"], "Avance": [10, 30, 45, 60, 75, avance_global]}
        st.plotly_chart(px.area(hist, x="Mes", y="Avance", title="Rendimiento del Proyecto vs Tiempo"))
        st.info("El sistema reduce drásticamente la necesidad de traslados físicos mediante inspección remota.") [cite: 144, 168]

    with tabs[4]:
        st.header("05 Indicadores de Avance")
        fig_av = px.bar(df.groupby("Área")["Avance %"].mean().reset_index(), x="Área", y="Avance %", color="Avance %")
        st.plotly_chart(fig_av, use_container_width=True)

    with tabs[5]:
        st.header("06 Seguridad y Riesgos") [cite: 208]
        st.metric("Incidentes Totales", "80", "-15%") [cite: 222, 232, 240]
        st.plotly_chart(px.line(x=["Ene", "Feb", "Mar", "Abr", "May", "Jun"], y=[210, 160, 150, 145, 140, 80], title="Tendencia de Accidentes")) [cite: 222-234]

    with tabs[6]:
        st.header("07 Análisis Estratégico") [cite: 250]
        st.success(f"La detección temprana de errores redujo retrasos en un 15% mediante IA.") [cite: 255]
        st.info(f"Se proyecta un ahorro del 10% del presupuesto al evitar reprocesos.") [cite: 260]

else:
    st.warning("⚠️ Cargue el archivo Excel para activar el monitoreo inteligente.")



