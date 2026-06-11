# 🏗️ Calculadora de Riesgo Estructural: Sáez TL-50-5T

Esta es una herramienta de ingeniería diseñada para el análisis probabilístico y mecánico de la grúa torre **Sáez TL-50-5T**. El software permite a los operarios y encargados de seguridad evaluar, en tiempo real, la estabilidad de la maquinaria basándose en parámetros físicos reales y condiciones operativas.

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.14
* **Framework de Interfaz:** Streamlit
* **Librerías de Cálculo:** NumPy, Pandas
* **Visualización:** Matplotlib, Seaborn
* **Despliegue:** Streamlit Cloud

---

## 🎯 Contexto y Problemática

En la industria de la construcción, el vuelco de grúas torre es uno de los accidentes más críticos. La mayoría de los operarios dependen de tablas estáticas que no siempre consideran variables dinámicas como la velocidad del viento, el desgaste por horas de uso o la distribución real del lastre.

**Solución:** Nuestra aplicación automatiza la verificación de estabilidad, proporcionando un veredicto de riesgo (Bajo/Medio/Alto) basado en el cálculo de momentos de fuerza (Vuelco vs. Estabilización), permitiendo una toma de decisiones informada antes de levantar una carga.

---

## 🚀 Guía de Inicio Rápido

### 1. Requisitos previos

* Tener instalado Python (v3.14 o superior).
* Tener `pip` instalado.

### 2. Instalación

Desde la carpeta raíz del proyecto, instala las dependencias:

```bash
pip install -r requirements.txt

```

### 3. Ejecución

Ejecuta la aplicación en tu entorno local:

```bash
python -m streamlit run app.py

```

*(Se abrirá automáticamente en tu navegador en `http://localhost:8501`)*

---

## 🌟 Características Principales

* **Cálculos de Ingeniería:** Basados en el manual técnico `TL-50-5T_rev.05.pdf`, integrando el peso real de la contrapluma (1598 kg) y el lastre (9700 kg).
* **Análisis Dinámico:** Cálculo de momentos de inercia y equilibrio estático.
* **Historial y Auditoría:** Registro persistente de cada simulación para informes de seguridad laboral.
* **Visualización de Datos:** Gráficas comparativas de evolución de riesgo y probabilidad de falla.
* **Exportación:** Generación de reportes en formato CSV para auditorías externas.

---

## 📖 Lógica de la Aplicación

### Modelo de Cálculo

La aplicación utiliza un modelo de **Balance de Momentos**:


$$M_{vuelco} = (F_{carga} \cdot R_{operacion}) + (M_{pluma} \cdot \frac{L_{pluma}}{2})$$

$$M_{estabilizador} = (M_{lastre} \cdot D_{lastre}) + (M_{contra} \cdot \frac{L_{contra}}{2})$$

Si $M_{estabilizador} - M_{vuelco} > 0$, el sistema se clasifica como **ESTABLE**.

### Módulos del Sistema

* **`app.py`:** Gestiona el estado de la sesión, la interfaz de usuario (Streamlit) y la interacción con los formularios.
* **`src/calculos.py`:** Núcleo matemático que realiza las interpolaciones de carga y el análisis bayesiano de riesgos.

---

## 🛡️ Consideraciones Técnicas

Para asegurar la precisión de los datos, el sistema ha sido calibrado con los valores del fabricante. **Importante:** Cualquier modificación en la configuración de la grúa (cambio de longitud de pluma) requiere ajustar los valores de lastre en la sección de "Masas de Componentes" siguiendo la tabla técnica adjunta en el manual del fabricante.

---

## 📌 Entrega del Proyecto

* **Documentación:** Este manual técnico (Word/PDF).
* **Código:** Proyecto completo (ZIP o Repositorio GitHub).
* **Código QR:** Acceso directo a la App en tiempo real (para el stand del 18 de junio).

---

*Nota: Esta aplicación es una herramienta de apoyo a la toma de decisiones y no sustituye la inspección física obligatoria por personal certificado según la normativa vigente.*
