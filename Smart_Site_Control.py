import streamlit as st
import pandas as pd
import io
import plotly.express as px

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="SmartSite Control", page_icon="🏗️", layout="wide")

# --- LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🏗️ SmartSite Control")
    st.caption("Fase 1: Prototipo Virtual")
    u, c = st.text_input("Usuario"), st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if u == "admin" and c == "1234":
            st.session_state.autenticado = True
            st.rerun()
    st.stop()

# --- SECCIÓN PREVIA: GUÍA DE FORMATOS Y PLANTILLA ---
if "archivo_listo" not in st.session_state:
    st.session_state.archivo_listo = False

st.title("🏗️ Configuración de Entrada de Datos")
st.markdown("### Antes de comenzar, asegúrese de usar los formatos compatibles con el sistema.")

col_ex, col_tec = st.columns(2)

with col_ex:
    st.subheader("📊 1. Seguimiento de Obra (Excel)")
    st.write("El archivo debe contener las siguientes columnas exactas:")
    
    # Mostrar el modelo visualmente
    modelo_df = pd.DataFrame({
        "Actividad": ["Ej: Excavación"],
        "Área": ["Ej: Estructura"],
        "Unidad": ["Ej: m3"],
        "Cantidad_Total": [100.0],
        "Cantidad_Ejecutada": [50.0]
    })
    st.dataframe(modelo_df, hide_index=True)
    
    # Generar botón de descarga de plantilla
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        modelo_df.to_excel(writer, index=False)
    
    st.download_button(
        label="📥 Descargar Plantilla Excel Maestra",
        data=buffer.getvalue(),
        file_name="Plantilla_SmartSite_Control.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

with col_tec:
    st.subheader("📁 2. Documentación Técnica")
    st.write("Formatos permitidos para el monitoreo inteligente:")
    st.markdown("""
    * **Modelos BIM:** `.rvt` (Revit) para validación de precisión geométrica[cite: 47, 265].
    * **Planos:** `.dwg` (AutoCAD) o `.pdf` para seguimiento de diseño[cite: 109].
    * **Registros:** `.jpg`, `.png` (Fotos de obra) para categorización por IA[cite: 112].
    """)

st.divider()

# --- CARGA DE ARCHIVOS ---
st.header("📂 Panel de Carga")
archivo_excel = st.file_uploader("Suba su archivo Excel completado", type=["xlsx"])
archivos_soporte = st.file_uploader("Suba planos, modelos o imágenes de respaldo", type=["pdf", "dwg", "rvt", "jpg", "png"], accept_multiple_files=True)

# --- VISUALIZACIÓN DE RESULTADOS (BASADO EN TUS DATOS SUBIDOS) ---
if archivo_excel:
    df = pd.read_excel(archivo_excel)
    
    # Validamos que las columnas existan
    columnas_req = ["Actividad", "Área", "Unidad", "Cantidad_Total", "Cantidad_Ejecutada"]
    if all(c in df.columns for c in columnas_req):
        
        # Procesamiento dinámico
        df["Avance %"] = (df["Cantidad_Ejecutada"] / df["Cantidad_Total"] * 100).round(2)
        avance_medio = df["Avance %"].mean()

        st.success("✅ Datos procesados con éxito.")
        
        # Dashboard dinámico imitando tu mockup [cite: 16, 177]
        t1, t2 = st.tabs(["Resumen Ejecutivo", "Indicadores de Avance"])
        
        with t1:
            st.header("01 Resumen Ejecutivo")
            c1, c2 = st.columns(2)
            c1.metric("Avance Físico Global", f"{avance_medio:.2f}%")
            c2.metric("Partidas en Seguimiento", len(df))
            st.dataframe(df, use_container_width=True)
            
        with t2:
            st.header("05 Indicadores de Avance")
            # Gráfico dinámico basado en las Áreas que tú definas en el Excel
            fig = px.bar(df.groupby("Área")["Avance %"].mean().reset_index(), 
                         x="Área", y="Avance %", title="Categorización de Avance Real",
                         color="Avance %", color_continuous_scale="Blues")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Error: El archivo no cumple con el modelo de columnas requerido.")







