# =====================================================
# SMARTSITE CONTROL – SEGUIMIENTO REAL DE OBRA
# Autor: Grupo5 – Ingeniería Civil
# =====================================================

import streamlit as st
import pandas as pd

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
st.subheader("Sistema real de seguimiento de obra")

st.divider()

# -----------------------------------------------------
# CARGA DE ARCHIVO EXCEL
# -----------------------------------------------------
st.header("📂 Carga de información de obra")

archivo = st.file_uploader(
    "Suba el archivo Excel de seguimiento",
    type=["xlsx"]
)

if archivo is None:
    st.info("📌 Para continuar, cargue el archivo Excel con los datos reales de la obra.")
    st.stop()

# -----------------------------------------------------
# LECTURA Y VALIDACIÓN DEL EXCEL
# -----------------------------------------------------
try:
    df = pd.read_excel(archivo)
except Exception as e:
    st.error("Error al leer el archivo Excel")
    st.stop()

columnas_obligatorias = [
    "Actividad",
    "Área",
    "Unidad",
    "Cantidad_Total",
    "Cantidad_Ejecutada"
]

for col in columnas_obligatorias:
    if col not in df.columns:
        st.error(f"Falta la columna obligatoria: {col}")
        st.stop()

# -----------------------------------------------------
# CÁLCULO DE PORCENTAJES
# -----------------------------------------------------
df["Porcentaje_Avance"] = (
    df["Cantidad_Ejecutada"] / df["Cantidad_Total"] * 100
).round(2)

# -----------------------------------------------------
# MÉTRICAS GENERALES
# -----------------------------------------------------
st.header("📊 Indicadores Generales")

avance_global = df["Porcentaje_Avance"].mean()

col1, col2 = st.columns(2)
col1.metric("Avance Global (%)", f"{avance_global:.2f}")

total_partidas = len(df)
col2.metric("Partidas Registradas", total_partidas)

st.divider()

# -----------------------------------------------------
# AVANCE POR ÁREA
# -----------------------------------------------------
st.header("🏗️ Avance por Área")

avance_area = (
    df.groupby("Área")["Porcentaje_Avance"]
    .mean()
    .reset_index()
)

st.dataframe(avance_area, use_container_width=True)

st.divider()

# -----------------------------------------------------
# ALERTAS REALES
# -----------------------------------------------------
st.header("🚨 Alertas Técnicas")

UMBRAL = 50

hay_alertas = False

for _, fila in avance_area.iterrows():
    if fila["Porcentaje_Avance"] < UMBRAL:
        st.warning(
            f"⚠️ Bajo avance en {fila['Área']} "
            f"({fila['Porcentaje_Avance']:.1f}%)"
        )
        hay_alertas = True

if not hay_alertas:
    st.success("✅ Todas las áreas presentan un avance adecuado")

st.divider()

# -----------------------------------------------------
# RANKING DE FRENTES
# -----------------------------------------------------
st.header("🏆 Ranking de Frentes de Trabajo")

ranking = df.groupby("Área")["Porcentaje_Avance"].mean()
ranking = ranking.sort_values(ascending=False)

st.table(ranking.reset_index())

st.divider()

# -----------------------------------------------------
# TABLA DETALLADA
# -----------------------------------------------------
st.header("📋 Detalle de Partidas")

st.dataframe(df, use_container_width=True)

st.divider()

# -----------------------------------------------------
# EXPORTACIÓN DE REPORTE
# -----------------------------------------------------
st.header("📄 Exportar Reporte")

reporte = df.copy()

csv = reporte.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Descargar reporte CSV",
    data=csv,
    file_name="reporte_seguimiento_obra.csv",
    mime="text/csv"
)

st.success("Reporte generado a partir de datos reales")

# -----------------------------------------------------
# GENERACIÓN DE REPORTE PDF
# -----------------------------------------------------
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from datetime import datetime
import io

def generar_reporte_pdf(df, avance_global, avance_area):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    contenido = []

    # ------------------ TÍTULO ------------------
    contenido.append(
        Paragraph("<b>INFORME DE SEGUIMIENTO DE OBRA</b>", styles["Title"])
    )
    contenido.append(Spacer(1, 12))

    fecha = datetime.now().strftime("%d/%m/%Y")
    contenido.append(Paragraph(f"<b>Fecha del informe:</b> {fecha}", styles["Normal"]))
    contenido.append(Spacer(1, 12))

    # ------------------ RESULTADOS ------------------
    contenido.append(Paragraph("<b>1. RESULTADOS</b>", styles["Heading2"]))
    contenido.append(Spacer(1, 8))

    contenido.append(
        Paragraph(
            f"El proyecto presenta un avance físico global del "
            f"<b>{avance_global:.2f}%</b>, calculado a partir de las cantidades "
            f"ejecutadas en obra.",
            styles["Normal"]
        )
    )
    contenido.append(Spacer(1, 8))

    contenido.append(
        Paragraph(
            f"Se registran un total de <b>{len(df)}</b> partidas de obra evaluadas.",
            styles["Normal"]
        )
    )
    contenido.append(Spacer(1, 8))

    for _, fila in avance_area.iterrows():
        contenido.append(
            Paragraph(
                f"• Área <b>{fila['Área']}</b>: avance promedio "
                f"de <b>{fila['Porcentaje_Avance']:.2f}%</b>.",
                styles["Normal"]
            )
        )

    contenido.append(Spacer(1, 12))

    # ------------------ CONCLUSIONES ------------------
    contenido.append(Paragraph("<b>2. CONCLUSIONES</b>", styles["Heading2"]))
    contenido.append(Spacer(1, 8))

    if avance_global >= 75:
        estado = "un estado general favorable"
    elif avance_global >= 50:
        estado = "un avance moderado que requiere seguimiento"
    else:
        estado = "un avance bajo que evidencia retrasos importantes"

    contenido.append(
        Paragraph(
            f"El análisis de la información indica que la obra presenta "
            f"{estado}.",
            styles["Normal"]
        )
    )
    contenido.append(Spacer(1, 8))

    areas_criticas = avance_area[avance_area["Porcentaje_Avance"] < 50]

    if not areas_criticas.empty:
        contenido.append(
            Paragraph(
                "Se identifican áreas con avance inferior al 50%, lo cual "
                "representa un riesgo para el cumplimiento del cronograma.",
                styles["Normal"]
            )
        )
    else:
        contenido.append(
            Paragraph(
                "No se identifican áreas críticas con bajo rendimiento.",
                styles["Normal"]
            )
        )

    contenido.append(Spacer(1, 12))

    # ------------------ RECOMENDACIONES ------------------
    contenido.append(Paragraph("<b>3. RECOMENDACIONES</b>", styles["Heading2"]))
    contenido.append(Spacer(1, 8))

    contenido.append(
        Paragraph(
            "• Reforzar los frentes de trabajo con bajo rendimiento mediante "
            "la redistribución de personal y recursos.",
            styles["Normal"]
        )
    )
    contenido.append(Spacer(1, 6))

    contenido.append(
        Paragraph(
            "• Realizar un seguimiento semanal de las partidas críticas "
            "para evitar retrasos acumulativos.",
            styles["Normal"]
        )
    )
    contenido.append(Spacer(1, 6))

    contenido.append(
        Paragraph(
            "• Verificar el abastecimiento oportuno de materiales "
            "para no afectar la productividad.",
            styles["Normal"]
        )
    )

    # ------------------ GENERAR PDF ------------------
    doc.build(contenido)
    buffer.seek(0)
    return buffer

pdf_buffer = generar_reporte_pdf(df, avance_global, avance_area)

st.download_button(
    label="📄 Descargar Reporte Técnico (PDF)",
    data=pdf_buffer,
    file_name="Informe_Seguimiento_Obra.pdf",
    mime="application/pdf"
)









