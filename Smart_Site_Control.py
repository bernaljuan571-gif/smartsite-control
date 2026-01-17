import streamlit as st
import pandas as pd
import plotly.express as px
import io
from PIL import Image

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="SmartSite Control", page_icon="🏗️", layout="wide")

# --- LOGIN ---
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

# --- BARRA LATERAL: CARGA DE ARCHIVOS ---
with st.sidebar:
    st.header("📂 Carga de Datos Reales")
    archivo_excel = st.file_uploader("1. Subir Seguimiento de Obra (Excel)", type=["xlsx"])
    archivos_tecnicos = st.file_uploader("2. Subir Planos o Fotos (PDF, DWG, RVT, Imagen)", type=["pdf", "dwg", "rvt", "jpg", "png"], accept_multiple_files=True)
    
    if st.button("Cerrar Sesión"):
        st.session_state.autenticado = False
        st.rerun()

# --- LÓGICA DE PROCESAMIENTO ---
if archivo_excel:
    # Lectura del archivo real del usuario
    df = pd.read_excel(archivo_excel)
    
    # Verificación de columnas obligatorias
    columnas_req = ["Actividad", "Área", "Unidad", "Cantidad_Total", "Cantidad_Ejecutada"]
    if all(col in df.columns for col in columnas_req):
        
        # Cálculos dinámicos basados en tus datos
        df["Porcentaje_Avance"] = (df["Cantidad_Ejecutada"] / df["Cantidad_Total"] * 100).round(2)
        avance_global = df["Porcentaje_Avance"].mean()
        
        # Estructura de pestañas del mockup [cite: 8-15]
        tabs = st.tabs(["01 Resumen Ejecutivo", "03 Registro Automatizado", "05 Indicadores de Avance"])

        with tabs[0]:
            st.header("01 Resumen Ejecutivo")
            c1, c2, c3 = st.columns(3)
            # El avance físico ahora viene de tu Excel
            c1.metric("Avance Físico Actual", f"{avance_global:.2f}%")
            c2.metric("Partidas Registradas", len(df))
            c3.metric("Áreas en Control", df["Área"].nunique())
            
            st.divider()
            st.subheader("📋 Estado Actual de Actividades")
            st.dataframe(df, use_container_width=True)

        with tabs[1]:
            st.header("03 Registro Automatizado")
            # Si subes imágenes, se muestran aquí para validación técnica
            if archivos_tecnicos:
                for arc in archivos_tecnicos:
                    if arc.type in ["image/jpeg", "image/png"]:
                        st.image(arc, caption=f"Registro: {arc.name}", use_container_width=True)
                    else:
                        st.write(f"📄 Archivo técnico cargado: {arc.name}")
            else:
                st.info("Suba fotos de obra o planos en la barra lateral para visualizarlos aquí.")

        with tabs[2]:
            st.header("05 Indicadores de Avance")
            # Gráfico generado dinámicamente con tus áreas reales
            df_area = df.groupby("Área")["Porcentaje_Avance"].mean().reset_index()
            fig = px.bar(df_area, x="Área", y="Porcentaje_Avance", 
                         title="Análisis de Avance por Área (Datos Reales)",
                         color="Porcentaje_Avance", color_continuous_scale="Viridis")
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.error(f"El Excel debe contener las columnas: {', '.join(columnas_req)}")
else:
    st.warning("⚠️ Esperando carga de archivo Excel para procesar indicadores estratégicos.")
    st.info("La aplicación está lista. Por favor, cargue su archivo de seguimiento en la barra lateral izquierda.")








