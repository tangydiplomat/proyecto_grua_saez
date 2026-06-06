import numpy as np

def calcular_analisis_grua(datos):
    """
    Realiza los cálculos de ingeniería mecánica y análisis probabilístico
    para la grúa torre Sáez TLS 50 5T basados en los parámetros digitados.
    """
    # 1. Obtener la carga máxima nominal según la curva real del plano a ese radio
    radios_tabla = [2.0, 12.0, 26.0, 50.0]
    cargas_tabla = [5000, 5000, 2500, 1100]
    carga_maxima_plano = float(np.interp(datos['radio_operacion'], radios_tabla, cargas_tabla))
    
    # Evaluar variable independiente 1: Sobrecarga estructural
    sobrecarga_detectada = datos['carga_suspendida'] > carga_maxima_plano
    exceso_peso = max(0.0, datos['carga_suspendida'] - carga_maxima_plano)
    
    # 2. Análisis del Centro de Masa (CM) del sistema (Pluma + Carga + Lastre)
    # Momento respecto al eje de la torre en X
    momento_pluma = datos['masa_pluma'] * (datos['longitud_pluma'] / 2)
    momento_carga = datos['carga_suspendida'] * datos['radio_operacion']
    momento_contrapluma = datos['masa_contrapluma'] * (datos['longitud_contra'] / 2)
    momento_lastre = datos['masa_lastre'] * datos['distancia_lastre']
    
    # Balance de masas en X (se resta el lado opuesto de la contrapluma)
    masa_total_superior = datos['masa_pluma'] + datos['carga_suspendida'] + datos['masa_contrapluma'] + datos['masa_lastre']
    x_cm = (momento_pluma + momento_carga - momento_contrapluma - momento_lastre) / (masa_total_superior + 1e-5)
    y_cm = datos['altura_torre'] * 0.7  # Estimación geométrica con la pluma arriba
    
    # 3. Momento de Inercia Rotacional Aproximado (I = m * r^2)
    inercia_sistema = (datos['masa_pluma'] * (datos['longitud_pluma']**2) / 3) + (datos['carga_suspendida'] * (datos['radio_operacion']**2))
    
    # 4. Estabilidad Estática (Momentos de Volcamiento vs Estabilizador en la Base)
    # Fuerza del viento en Newtons aproximada: F = 0.5 * rho * V^2 * A * Cd
    fuerza_viento = 0.6125 * ((datos['velocidad_viento'] / 3.6)**2) * datos['area_expuesta'] * 1.2
    momento_viento = fuerza_viento * (datos['altura_torre'] / 2)
    
    masa_total_grua = masa_total_superior + datos['masa_torre']
    momento_estabilizador_base = masa_total_grua * 9.81 * (datos['ancho_base_chasis'] / 2)
    momento_volcamiento_total = (abs(x_cm) * masa_total_superior * 9.81) + momento_viento
    
    margen_seguridad = momento_estabilizador_base - momento_volcamiento_total
    estabilidad_estado = "Estable" if margen_seguridad > 0 else "Inestable (Riesgo de Volcamiento)"
    
    # 5. Evaluación Probabilística de Riesgo (Teorema de Bayes)
    p_falla = 0.005  # Probabilidad base de falla estructural bajo condiciones ideales
    
    # Condicionar la probabilidad según las 4 variables independientes del maestro
    if sobrecarga_detectada: p_falla += 0.45       # Variable 1: Sobrecarga
    if datos['horas_sin_mto'] > 500: p_falla += 0.20 # Variable 2: Deficiencias Mantenimiento
    if datos['velocidad_viento'] > 50: p_falla += 0.25 # Variable 3: Condiciones Ambientales
    if datos['horas_turno_operador'] > 8: p_falla += 0.10 # Variable 4: Errores Operación (Fatiga)
    
    p_falla_porcentaje = min(p_falla * 100, 100.0)
    
    if p_falla_porcentaje < 8:
        riesgo_texto = "BAJO"
    elif p_falla_porcentaje < 28:
        riesgo_texto = "MEDIO"
    else:
        riesgo_texto = "ALTO"
        
    return {
        "carga_maxima_plano": round(carga_maxima_plano, 1),
        "exceso_peso": round(exceso_peso, 1),
        "x_cm": round(x_cm, 3),
        "y_cm": round(y_cm, 3),
        "masa_total_superior": round(masa_total_superior, 1),
        "inercia": round(inercia_sistema, 2),
        "estabilidad": estabilidad_estado,
        "margen": round(margen_seguridad, 1),
        "prob_falla": round(p_falla_porcentaje, 2),
        "riesgo": riesgo_texto,
        "sobrecarga": sobrecarga_detectada
    }