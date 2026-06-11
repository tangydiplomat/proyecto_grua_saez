import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
from src.calculos import calcular_analisis_grua

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Calculadora de Riesgo - Sáez TL-50-5T", layout="wide")

# Inicialización de variables de estado global (Session State)
if 'historial' not in st.session_state:
    st.session_state.historial = pd.DataFrame()

if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "home"

# =========================================================================
# VISTA 1: HOME / PORTADA INSTITUCIONAL (ESTILO CENTRADO ABSOLUTO)
# =========================================================================
if st.session_state.pagina_actual == "home":
    
    # Inyección de estilos CSS avanzados para centrado vertical, horizontal y fuentes
    st.markdown("""
    <style>
        /* Fondo corporativo */
        .stApp {
            background-color: #111E38 !important;
        }
        
        /* Contenedor principal que fuerza el centro absoluto de la pantalla */
        .contenedor-centro {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            min-height: 65vh;
            width: 100%;
        }
        
        /* Tipografía estilizada para títulos */
        .titulo-portada {
            font-family: 'Georgia', 'Times New Roman', serif !important;
            color: #FFFFFF;
            font-size: 32px;
            font-weight: bold;
            line-height: 1.4;
            margin-top: 25px;
            margin-bottom: 35px;
        }
        
        /* Ajuste fino para el texto secundario en la otra línea */
        .sub-linea {
            display: block;
            font-size: 26px;
            color: #E2E8F0;
            margin-top: 6px;
            font-weight: normal;
        }
        
        /* Forzar que el botón de Streamlit se alinee al centro exacto */
        div.stButton {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
        }
        
        /* Estilo personalizado del Botón Rojo */
        div.stButton > button:first-child {
            background-color: #FF0000 !important;
            color: white !important;
            font-family: 'Georgia', serif !important;
            font-size: 19px !important;
            font-weight: bold !important;
            border-radius: 24px !important;
            padding: 10px 38px !important;
            border: none !important;
            box-shadow: 0px 5px 15px rgba(0,0,0,0.4) !important;
            transition: all 0.3s ease;
        }
        
        div.stButton > button:first-child:hover {
            transform: scale(1.05);
            background-color: #CC0000 !important;
            box-shadow: 0px 7px 20px rgba(0,0,0,0.6) !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    col_izq, col_centro, col_der = st.columns([1, 6, 1])
    
    with col_centro:
        st.markdown('<div class="contenedor-centro">', unsafe_allow_html=True)
        
        # CONTROL DE CARGA DEL LOGO (.png)
        ruta_logo = os.path.join("assets", "logo_uni.png")
        
        if os.path.exists(ruta_logo):
            st.image(ruta_logo, width=260)
        else:
            st.warning("⚠️ Archivo no detectado. Verifique que el nombre sea 'logo_uni.jpeg' dentro de la carpeta assets.")
        
        # TÍTULO EN DOS LÍNEAS
        st.markdown("""
            <h1 class="titulo-portada">
                Calculadora de Riesgo de una Grúa de Torre
                <span class="sub-linea">Sáez TL-50-5T</span>
            </h1>
        """, unsafe_allow_html=True)
        
        # BOTÓN INTERACTIVO CENTRAL
        if st.button("Ir a la calculadora"):
            st.session_state.pagina_actual = "calculadora"
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # PIE DE PÁGINA CORPORATIVO
        col_pie_izq, col_pie_der = st.columns(2)
        with col_pie_izq:
            st.markdown("""<p style="color: #7A8B9E; font-family: Georgia, serif; font-size: 13px; margin: 0;">© tangydiplomat - Todos los derechos reservados 2026</p>""", unsafe_allow_html=True)
        with col_pie_der:
            st.markdown("""<p style="text-align: right; color: #FFFFFF; font-family: Georgia, serif; font-size: 15px; font-weight: bold; margin: 0;">Junio 2026</p>""", unsafe_allow_html=True)

# =========================================================================
# VISTA 2: NÚCLEO DE LA CALCULADORA
# =========================================================================
else:
    st.markdown("""
    <style>
        .stApp {
            background-color: #1E1E1E !important;
        }
        h1, h2, h3, p, span, label {
            font-family: sans-serif !important;
        }
    </style>
    """, unsafe_allow_html=True)

    if st.button("⬅️ Volver a la Portada"):
        st.session_state.pagina_actual = "home"
        st.rerun()
        
    st.title("🏗️ Calculadora de Riesgo Estructural y Operativo")
    st.markdown("Análisis probabilístico y mecánico para la Grúa Torre **Sáez TL-50-5T**")
    st.markdown("---")
    
    pestana_analisis, pestana_historial, pestana_graficas, pestana_exportar = st.tabs([
        "📊 Área de Calculadora", "📜 Historial", "📈 Gráficas", "📥 Exportar Datos"
    ])
    
    with pestana_analisis:
        col_izq, col_der = st.columns([1, 2])
        
        with col_izq:
            st.subheader("Datos de Operación y Configuración")
            st.markdown("*Ingrese los parámetros obligatorios de trabajo (Valores mayores a 0):*")
            
            carga_suspendida = st.number_input("Carga suspendida actual (kg)", min_value=10.0, value=1200.0, step=50.0)
            radio_operacion = st.number_input("Radio de operación / Alcance del carro (m)", min_value=1.0, max_value=50.0, value=25.0, step=0.5)
            velocidad_viento = st.number_input("Velocidad del viento (km/h)", min_value=0.0, value=22.0, step=1.0)
            horas_sin_mto = st.number_input("Horas acumuladas sin mantenimiento", min_value=0.0, value=120.0, step=10.0)
            horas_turno_operador = st.number_input("Horas de turno continuo del operador", min_value=0.5, value=4.0, step=0.5)
            
            st.markdown("---")
            st.markdown("**Especificaciones Geométricas y de Masa (Plano):**")
            altura_torre = st.number_input("Altura total de la torre (m)", min_value=1.0, value=34.7, step=1.0)
            longitud_pluma = st.number_input("Longitud total de la pluma (m)", min_value=5.0, value=50.0, step=1.0)
            longitud_contra = st.number_input("Longitud de la contrapluma (m)", min_value=2.0, value=12.15, step=0.1)
            ancho_base_chasis = st.number_input("Ancho de la base del chasis (m)", min_value=1.0, value=3.8, step=0.1)
            
            st.markdown("---")
            st.markdown("**Masas de Componentes (kg):**")
            masa_torre = st.number_input("Masa estructural de la torre (kg)", min_value=100.0, value=8500.0, step=100.0)
            masa_pluma = st.number_input("Masa estructural de la pluma (kg)", min_value=100.0, value=3200.0, step=50.0)
            masa_contrapluma = st.number_input("Masa de la contrapluma (kg)", min_value=50.0, value=1100.0, step=50.0)
            masa_lastre = st.number_input("Masa de los bloques de lastre superior (kg)", min_value=100.0, value=9700.0, step=100.0)
            distancia_lastre = st.number_input("Distancia del lastre al eje central (m)", min_value=0.5, value=10.5, step=0.1)
            area_expuesta = st.number_input("Área estructural expuesta al viento (m2)", min_value=0.5, value=14.5, step=0.5)
    
            datos_entrada = {
                "carga_suspendida": carga_suspendida, "radio_operacion": radio_operacion, 
                "velocidad_viento": velocidad_viento, "horas_sin_mto": horas_sin_mto, 
                "horas_turno_operador": horas_turno_operador, "altura_torre": altura_torre, 
                "longitud_pluma": longitud_pluma, "longitud_contra": longitud_contra, 
                "ancho_base_chasis": ancho_base_chasis, "masa_torre": masa_torre, 
                "masa_pluma": masa_pluma, "masa_contrapluma": masa_contrapluma, 
                "masa_lastre": masa_lastre, "distancia_lastre": distancia_lastre, 
                "area_expuesta": area_expuesta
            }
            
            guardar_registro = st.button("Registrar simulación en Historial")
    
        # PROCESAR CÁLCULOS
        res = calcular_analisis_grua(datos_entrada)
        
        if guardar_registro:
            datos_respaldo = datos_entrada.copy()
            datos_respaldo['Fecha'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            datos_respaldo['Riesgo'] = res['riesgo']
            datos_respaldo['Prob. Falla (%)'] = res['prob_falla']
            datos_respaldo['Momento Volcamiento'] = res['margen']
            
            st.session_state.historial = pd.concat([st.session_state.historial, pd.DataFrame([datos_respaldo])], ignore_index=True)
            st.success("¡Análisis guardado exitosamente!")
    
        with col_der:
            bg_alerta = "#388E3C" if res['riesgo'] == "BAJO" else ("#F57C00" if res['riesgo'] == "MEDIO" else "#D32F2F")
            
            st.markdown(f"""
            <div style="background-color:{bg_alerta}; padding:18px; border-radius:5px; margin-bottom:20px;">
                <h2 style="color:white; margin:0; font-family:sans-serif;">Riesgo operativo: {res['riesgo']} ({res['prob_falla']}%)</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.subheader("Resultados de la Evaluación de Seguridad")
            
            exceso_peso_val = res.get('exceso_weight', res.get('exceso_peso', 0.0))
            st.info(f"**Capacidad del Plano Técnico:** \nCarga Máxima permitida a {radio_operacion}m: **{res['carga_maxima_plano']} kg** \nExceso determinado: {exceso_peso_val} kg")
            
            if res['sobrecarga']:
                st.error("🚨 ALERTA: La carga ingresada supera la capacidad de resistencia del plano para este radio.")
                
            st.warning(f"**Estabilidad y Desplazamiento Estático:** \nCentro de masa del sistema: x = {res['x_cm']} m | y = {res['y_cm']} m  \nMasa total suspendida: {res['masa_total_superior']} kg")
            st.success(f"**Comportamiento Dinámico:** \nMomento de inercia rotacional estimado: **{res['inercia']} kg·m²**")
            
            st.metric(label="Condición Física del Chasis Inferior", value=res['estabilidad'], delta=f"Margen contra volcamiento: {res['margen']} N·m")
    
    # HISTORIAL PERSISTENTE
    with pestana_historial:
        st.header("Historial de Operaciones Registradas")
        if st.session_state.historial.empty:
            st.info("El historial se encuentra vacío. Registre simulaciones en la pestaña del Calculador.")
        else:
            st.dataframe(st.session_state.historial, use_container_width=True)
    
    # GRÁFICAS DEL HISTORIAL (SE CORRIGIÓ EL MÉTODO GRID)
    with pestana_graficas:
        st.header("📈 Análisis Estadístico y de Comportamiento")
        if st.session_state.historial.empty:
            st.info("Para visualizar los gráficos de comportamiento, registre al menos 2 simulaciones con datos diferentes en el Historial.")
        else:
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.subheader("Evolución de la Probabilidad de Falla")
                fig1, ax1 = plt.subplots(figsize=(6, 4))
                ax1.plot(st.session_state.historial.index + 1, st.session_state.historial['Prob. Falla (%)'], marker='o', color='#FF0000', linewidth=2)
                ax1.set_xlabel("Número de Simulación")
                ax1.set_ylabel("Probabilidad de Falla (%)")
                ax1.grid(True, linestyle='--', alpha=0.5)  # <-- Línea corregida aquí
                st.pyplot(fig1)
                
            with col_g2:
                st.subheader("Distribución de Niveles de Riesgo")
                fig2, ax2 = plt.subplots(figsize=(6, 4))
                conteo_riesgos = st.session_state.historial['Riesgo'].value_counts()
                colores = ['#388E3C' if x == 'BAJO' else ('#F57C00' if x == 'MEDIO' else '#D32F2F') for x in conteo_riesgos.index]
                ax2.bar(conteo_riesgos.index, conteo_riesgos.values, color=colores)
                ax2.set_ylabel("Cantidad de Registros")
                st.pyplot(fig2)
    
    # EXPORTAR REGISTROS
    with pestana_exportar:
        st.header("Exportación de Datos para Auditoría")
        if st.session_state.historial.empty:
            st.info("No hay datos disponibles para generar reportes en este momento.")
        else:
            csv_file = st.session_state.historial.to_csv(index=False).encode('utf-8')
            st.download_button(label="Descargar reporte integral en formato CSV", data=csv_file, file_name="auditoria_grua_saez.csv", mime="text/csv")
