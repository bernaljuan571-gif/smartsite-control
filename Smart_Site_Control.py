import streamlit as st
import pandas as pd
import io
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

# -----------------------------------------------------
# CONFIGURACIÓN INICIAL
# -----------------------------------------------------
st.set_page_config(
    page_title="SmartSite Control",
    page_icon="🏗️",
    layout="wide"
)

# -----------------------------------------------------
# LOGIN
# -----------------------------------------------------
USUARIO_VALIDO = "admin"
CLAVE_VALIDA = "1234"

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 Acceso al Sistema")
    usuario = st.text_input("Usuario")
    clave = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if usuario == USUARIO_VALIDO and clave == CLAVE_VALIDA:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")
    st.stop()

# -----------------------------------------------------
# APP PRINCIPAL
# -----------------------------------------------------
st.title("🏗️ SmartSite Control")
st.subheader("Sistema de seguimiento real de obra")

# --- BARRA LATERAL: ADJUNTAR PDFS ---
with st.sidebar:
    st.header("📁 Documentación")
    archivos_pdf = st.file_uploader(
        "Adjuntar PDFs (Planos/Informes)", 
        type=["pdf"], 
        accept_multiple_files=True
    )

st.divider()

# -----------------------------------------------------
# NUEVA SECCIÓN: DESCARGA DE PLANTILLA EXCEL
# -----------------------------------------------------
st.header("📥 Preparación de Datos")
col_plantilla, col_info = st.columns([1, 2])

with col_plantilla:
    st.write("¿No tiene el formato?")
    
    # Crear un DataFrame de ejemplo para la plantilla
    df_plantilla = pd.DataFrame({
        "Actividad": ["Excavación", "Hormigón de Cimentación", "Acero de Refuerzo"],
        "Área": ["Estructura", "Estructura", "Estructura"],
        "Unidad": ["m3", "m3", "kg"],
        "Cantidad_Total": [100, 50, 1000],
        "Cantidad_Ejecutada": [0, 0, 0]
    })

    # Función para convertir DF a Excel en memoria
    def to_excel(df):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Seguimiento')
        return output.getvalue()

    excel_data = to_excel(df_plantilla)

    st.download_button(
        label="🟢 Descargar Plantilla Excel",
        data=excel_data,
        file_name="Plantilla_SmartSite_Control.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

with col_info:
    st.info("""
    **Instrucciones:**
    1. Descargue la plantilla.
    2. Complete las columnas 'Cantidad_Total' y 'Cantidad_Ejecutada'.
    3. Suba el archivo en la sección de abajo para ver el progreso.
    """)

st.divider()

# -----------------------------------------------------
# CARGA Y PROCESAMIENTO
# -----------------------------------------------------
st.header("📂 Carga de Seguimiento")
archivo = st.file_uploader("Suba su Excel completado", type=["xlsx"])

if archivo:
    try:
        df = pd.read_excel(archivo)
        
        columnas_obligatorias = ["Actividad", "Área", "Unidad", "Cantidad_Total", "Cantidad_Ejecutada"]
        if all(col in df.columns for col in columnas_obligatorias):
            
            # Cálculos
            df["Porcentaje_Avance"] = (df["Cantidad_Ejecutada"] / df["Cantidad_Total"] * 100).round(2)
            avance_global = df["Porcentaje_Avance"].mean()

            # Métricas con 2 decimales
            st.header("📊 Indicadores Generales")
            c1, c2 = st.columns(2)
            c1.metric("Avance Físico Global", f"{avance_global:.2f}%")
            c2.metric("Partidas en Seguimiento", len(df))

            st.divider()

            # Ranking Formateado
            st.header("🏆 Ranking de Frentes de Trabajo")
            ranking = df.groupby("Área")["Porcentaje_Avance"].mean().sort_values(ascending=False).reset_index()
            ranking["Porcentaje_Avance"] = ranking["Porcentaje_Avance"].map("{:.2f}%".format)
            st.table(ranking)

            # Detalle de Partidas
            st.header("📋 Detalle de Obra")
            df_mostrar = df.copy()
            df_mostrar["Porcentaje_Avance"] = df_mostrar["Porcentaje_Avance"].map("{:.2f}%".format)
            st.dataframe(df_mostrar, use_container_width=True)

            # Mostrar PDFs si existen
            if archivos_pdf:
                st.divider()
                st.header("📑 Documentación Adjunta")
                for pdf in archivos_pdf:
                    st.download_button(f"📥 Descargar: {pdf.name}", data=pdf.read(), file_name=pdf.name)

        else:
            st.error("El archivo no coincide con la plantilla. Por favor, use la plantilla descargable.")
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
else:
    st.warning("Esperando carga de datos...")











