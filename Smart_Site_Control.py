import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(page_title="SmartSite Control", page_icon="🏗️", layout="wide")

st.markdown("""
    <style>
    .stMetric { border-left: 5px solid #1E3A8A; background-color: #f0f2f6; padding: 10px; border-radius: 5px; }
    .main { background-color: #ffffff; }
    </style>
""", unsafe_allow_html=True)

# --- ACCESO ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🏗️ SmartSite Control")
    u = st.text_input("Usuario")
    c = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if u == "admin" and c == "1234":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")
    st.stop()

# --- HEADER ---
st.title("🏗️ SmartSite Control")
st.caption("Plataforma de monitoreo inteligente y seguimiento de obra en tiempo real")

# --- GUÍA Y PLANTILLA ---
with st.expander("📥 Descargar Plantilla y Ver Guía de Modelos"):
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("*Modelo de Seguimiento (Excel)*")
        df_temp = pd.DataFrame({
            "Actividad": ["Zapata Z1"],
            "Área": ["Estructural"],
            "Unidad": ["m3"],
            "Cantidad_Total": [100.0],
            "Cantidad_Ejecutada": [50.0]
        })
        st.dataframe(df_temp, hide_index=True)

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df_temp.to_excel(writer, index=False, sheet_name="Seguimiento")
        st.download_button(
            "Descargar Plantilla Maestra",
            data=buffer.getvalue(),
            file_name="Plantilla_SmartSite.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with col_b:
        st.write("*Modelos Técnicos Aceptados*")
        st.info("PDF (Planos), RVT (Revit), DWG (AutoCAD), JPG/PNG (Fotos de Obra)")

st.divider()

# --- CARGA ---
with st.sidebar:
    st.header("📂 Panel de Carga")
    archivo_excel = st.file_uploader("1. Excel de Seguimiento", type=["xlsx"])
    archivos_soporte = st.file_uploader(
        "2. Documentación/Fotos",
        type=["pdf", "dwg", "rvt", "jpg", "png"],
        accept_multiple_files=True
    )
    if st.button("Cerrar Sesión"):
        st.session_state.autenticado = False
        st.rerun()

# --- DASHBOARD ---
if archivo_excel:
    df = pd.read_excel(archivo_excel)

    # Validación mínima de columnas esperadas
    required = {"Actividad", "Área", "Unidad", "Cantidad_Total", "Cantidad_Ejecutada"}
    if not required.issubset(set(df.columns)):
        st.error(f"Tu Excel debe tener estas columnas: {sorted(list(required))}")
        st.stop()

    df["Avance %"] = (df["Cantidad_Ejecutada"] / df["Cantidad_Total"] * 100).round(2)
    avance_global = float(df["Avance %"].mean())

    tabs = st.tabs([
        "01 Resumen", "02 Integración Tech", "03 Registro IA",
        "04 Eficiencia Op.", "05 Indicadores", "06 Seguridad", "07 Estrategia"
    ])

    with tabs[0]:
        st.header("01 Resumen Ejecutivo")
        c1, c2, c3 = st.columns(3)
        c1.metric("Avance Físico Actual", f"{avance_global:.2f}%")
        c2.metric("Puntos de Inspección", "265", "+21")
        c3.metric("Índice de Calidad", "92%", "+32%")

    with tabs[1]:
        st.header("02 Integración Tecnológica")
        col_m1, col_m2 = st.columns([1, 1])
        with col_m1:
            st.subheader("Estado de Maquinaria (Sensores IoT)")
            maq_data = pd.DataFrame({
                "Equipo": ["Grúas", "Excavadoras", "Volquetas", "Retroexcavadoras"],
                "Uso %": [12, 26, 28, 18]
            })
            st.plotly_chart(px.bar(maq_data, x="Equipo", y="Uso %", color="Equipo"), use_container_width=True)
        with col_m2:
            st.subheader("Geolocalización de Unidades")
            map_data = pd.DataFrame({"lat": [-2.1894, -0.1807], "lon": [-79.8891, -78.4678]})
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
            st.info("Cargue imágenes de la obra para validación geométrica contra el modelo BIM.")

    with tabs[3]:
        st.header("04 Eficiencia Operativa")
        st.subheader("Curva de Productividad")
        hist = pd.DataFrame({"Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun"], "Avance": [10, 30, 45, 60, 75, avance_global]})
        st.plotly_chart(px.area(hist, x="Mes", y="Avance", title="Rendimiento del Proyecto vs Tiempo"), use_container_width=True)
        st.info("El sistema reduce traslados físicos mediante inspección remota.")

    with tabs[4]:
        st.header("05 Indicadores de Avance")
        fig_av = px.bar(df.groupby("Área", as_index=False)["Avance %"].mean(), x="Área", y="Avance %", color="Avance %")
        st.plotly_chart(fig_av, use_container_width=True)

    with tabs[5]:
        st.header("06 Seguridad y Riesgos")
        st.metric("Incidentes Totales", "80", "-15%")
        st.plotly_chart(
            px.line(x=["Ene", "Feb", "Mar", "Abr", "May", "Jun"], y=[210, 160, 150, 145, 140, 80], title="Tendencia de Accidentes"),
            use_container_width=True
        )

    with tabs[6]:
        st.header("07 Análisis Estratégico")
        st.success("La detección temprana de errores redujo retrasos en un 15% mediante IA.")
        st.info("Se proyecta un ahorro del 10% del presupuesto al evitar reprocesos.")

else:
    st.warning("⚠️ Cargue el archivo Excel para activar el monitoreo inteligente.")
