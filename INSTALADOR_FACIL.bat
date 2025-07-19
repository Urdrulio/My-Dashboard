@echo off
chcp 65001 >nul
title 🎯 StrategySim Enterprise - Instalador Automático
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🎯 StrategySim Enterprise                    ║
echo ║              Instalador Automático v1.0                     ║
echo ║                                                              ║
echo ║          ¡Instala todo automáticamente en 1 click!          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📋 Este instalador hará todo automáticamente:
echo    ✅ Verificar Python
echo    ✅ Crear directorio del proyecto
echo    ✅ Crear todos los archivos necesarios
echo    ✅ Instalar dependencias
echo    ✅ Crear acceso directo en el escritorio
echo    ✅ Ejecutar la aplicación
echo.

pause

echo.
echo 🔍 Paso 1/6: Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no está instalado. 
    echo.
    echo 📥 Descargando Python automáticamente...
    echo    Por favor, instala Python cuando se abra el navegador
    echo    ¡Asegúrate de marcar "Add Python to PATH"!
    start https://www.python.org/downloads/
    echo.
    echo ⏳ Presiona cualquier tecla DESPUÉS de instalar Python...
    pause
    
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Python sigue sin estar disponible. Reinicia este script.
        pause
        exit /b 1
    )
)
echo ✅ Python encontrado!

echo.
echo 📁 Paso 2/6: Creando directorio del proyecto...
set "PROJECT_DIR=%USERPROFILE%\Desktop\StrategySim-Enterprise"
if not exist "%PROJECT_DIR%" mkdir "%PROJECT_DIR%"
cd /d "%PROJECT_DIR%"
echo ✅ Directorio creado en: %PROJECT_DIR%

echo.
echo 📝 Paso 3/6: Creando archivos del proyecto...

echo streamlit^>=1.28.0> requirements.txt
echo pandas^>=1.5.0>> requirements.txt
echo plotly^>=5.15.0>> requirements.txt
echo numpy^>=1.24.0>> requirements.txt
echo sqlalchemy^>=2.0.0>> requirements.txt
echo scikit-learn^>=1.3.0>> requirements.txt

echo Date,Revenue,Profit_Margin,Operating_Costs,Customer_Count,Market_Share,Employee_Count,R^&D_Investment,Customer_Satisfaction,Product_Lines,Region,Sales_Channel> sample_sap_data.csv
echo 2022-01-01,10500000,0.18,6300000,51200,0.22,2050,180000,4.1,Product_A,EMEA,Direct>> sample_sap_data.csv
echo 2022-02-01,10750000,0.19,6450000,52100,0.23,2080,185000,4.2,Product_B,Americas,Partner>> sample_sap_data.csv
echo 2022-03-01,11200000,0.17,6600000,53200,0.24,2120,190000,4.3,Product_C,APAC,Online>> sample_sap_data.csv

echo ✅ Archivos básicos creados

echo.
echo 📦 Paso 4/6: Instalando dependencias...
echo    (Esto puede tomar 2-3 minutos...)
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt

echo.
echo 🔧 Paso 5/6: Creando archivos de la aplicación...
echo    (Descargando código fuente...)

powershell -Command "& {
$appContent = @'
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import random
from datetime import datetime, timedelta

st.set_page_config(
    page_title=\"StrategySim Enterprise - Demo\",
    page_icon=\"🎯\",
    layout=\"wide\"
)

st.markdown(\"<h1 style='text-align: center; color: #667eea;'>🎯 StrategySim Enterprise - DEMO</h1>\", unsafe_allow_html=True)
st.markdown(\"<h3 style='text-align: center;'>¡Tu Juego de Estrategia Empresarial con Datos SAP!</h3>\", unsafe_allow_html=True)

st.markdown(\"\"\"
<div style='background: linear-gradient(135deg, #667eea 0%%, #764ba2 100%%); padding: 20px; border-radius: 10px; margin: 20px 0;'>
    <h2 style='color: white; text-align: center;'>🎮 VERSIÓN DEMO - FUNCIONALIDADES PRINCIPALES</h2>
</div>
\"\"\", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(\"\"\"
    <div style='background: #f093fb; padding: 15px; border-radius: 10px; text-align: center; color: white;'>
        <h3>📊 Dashboard</h3>
        <p>Visualiza KPIs empresariales en tiempo real</p>
    </div>
    \"\"\", unsafe_allow_html=True)

with col2:
    st.markdown(\"\"\"
    <div style='background: #4facfe; padding: 15px; border-radius: 10px; text-align: center; color: white;'>
        <h3>🎯 Preguntas Estratégicas</h3>
        <p>IA genera preguntas basadas en tus datos</p>
    </div>
    \"\"\", unsafe_allow_html=True)

with col3:
    st.markdown(\"\"\"
    <div style='background: #43e97b; padding: 15px; border-radius: 10px; text-align: center; color: white;'>
        <h3>🏆 Gamificación</h3>
        <p>Sistema de puntos y niveles</p>
    </div>
    \"\"\", unsafe_allow_html=True)

if st.button(\"🚀 EMPEZAR DEMO\", type=\"primary\"):
    st.balloons()
    
    # Datos de muestra
    data = {
        'Mes': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
        'Ingresos': [1050000, 1150000, 1250000, 1350000, 1450000, 1550000],
        'Clientes': [51200, 52500, 54100, 55800, 57200, 59100],
        'Satisfacción': [4.1, 4.3, 4.5, 4.7, 4.8, 5.0]
    }
    df = pd.DataFrame(data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.line(df, x='Mes', y='Ingresos', title='📈 Evolución de Ingresos', 
                      color_discrete_sequence=['#667eea'])
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.bar(df, x='Mes', y='Clientes', title='👥 Crecimiento de Clientes',
                     color_discrete_sequence=['#f093fb'])
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown(\"\"\"
    <div style='background: #fa709a; padding: 20px; border-radius: 15px; text-align: center; color: white; margin: 20px 0;'>
        <h2>🎯 Pregunta Estratégica de Ejemplo</h2>
        <p><strong>Los ingresos han crecido 47%% en 6 meses. ¿Cuál debe ser tu próxima estrategia?</strong></p>
    </div>
    \"\"\", unsafe_allow_html=True)
    
    estrategia = st.radio(
        \"Selecciona tu estrategia:\",
        [
            \"💰 Invertir agresivamente en marketing para acelerar el crecimiento\",
            \"🛡️ Consolidar posición actual y mejorar márgenes de beneficio\",
            \"🌍 Expandir a nuevos mercados geográficos\",
            \"🔬 Aumentar inversión en I+D para innovar productos\"
        ]
    )
    
    if st.button(\"✅ Confirmar Decisión\"):
        puntos = random.randint(80, 120)
        st.success(f\"🎉 ¡Excelente decisión! Has ganado {puntos} puntos\")
        st.markdown(f\"\"\"
        <div style='background: #43e97b; padding: 15px; border-radius: 10px; text-align: center; color: white;'>
            <h3>🏆 Puntuación: {puntos}/120</h3>
            <p>Nivel: Estratega Junior</p>
        </div>
        \"\"\", unsafe_allow_html=True)

st.markdown(\"\"\"
---
## 🎯 Características de la Versión Completa

- 📊 **Dashboard Completo**: 20+ visualizaciones interactivas
- 🤖 **IA Avanzada**: Generación automática de preguntas estratégicas
- 📈 **Predicciones**: Machine Learning para forecasting
- 🎮 **Gamificación Total**: Niveles, logros, desafíos
- 📁 **Datos Masivos**: Manejo de millones de registros SAP
- 🔍 **Análisis Profundo**: Correlaciones, riesgos, escenarios

### 💡 ¿Te Gusta el Demo?
¡Esta es solo una pequeña muestra! La versión completa incluye todas las funcionalidades avanzadas.

**📧 Contacto**: strategysim@empresa.com
\"\"\")
'@
Set-Content -Path 'app.py' -Value $appContent -Encoding UTF8
}"

echo ✅ Aplicación creada

echo.
echo 🖥️ Paso 6/6: Creando acceso directo...

echo @echo off> EJECUTAR_STRATEGYSIM.bat
echo title 🎯 StrategySim Enterprise>> EJECUTAR_STRATEGYSIM.bat
echo color 0A>> EJECUTAR_STRATEGYSIM.bat
echo echo.>> EJECUTAR_STRATEGYSIM.bat
echo echo 🚀 Iniciando StrategySim Enterprise...>> EJECUTAR_STRATEGYSIM.bat
echo echo.>> EJECUTAR_STRATEGYSIM.bat
echo echo ✅ La aplicación se abrirá en tu navegador>> EJECUTAR_STRATEGYSIM.bat
echo echo 🌐 URL: http://localhost:8501>> EJECUTAR_STRATEGYSIM.bat
echo echo.>> EJECUTAR_STRATEGYSIM.bat
echo echo ⚠️  Para cerrar la aplicación, cierra esta ventana>> EJECUTAR_STRATEGYSIM.bat
echo echo.>> EJECUTAR_STRATEGYSIM.bat
echo cd /d "%PROJECT_DIR%">> EJECUTAR_STRATEGYSIM.bat
echo streamlit run app.py>> EJECUTAR_STRATEGYSIM.bat

copy EJECUTAR_STRATEGYSIM.bat "%USERPROFILE%\Desktop\🎯 StrategySim Enterprise.bat" >nul

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    ✅ ¡INSTALACIÓN COMPLETA!                ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🎉 ¡Todo listo! Ahora puedes usar StrategySim Enterprise
echo.
echo 📁 Archivos instalados en: %PROJECT_DIR%
echo 🖥️ Acceso directo creado en el escritorio
echo.
echo 🚀 PARA EJECUTAR LA APLICACIÓN:
echo    1. Haz doble clic en "🎯 StrategySim Enterprise.bat" en tu escritorio
echo    2. O ejecuta "EJECUTAR_STRATEGYSIM.bat" desde la carpeta del proyecto
echo.
echo 🌐 La aplicación se abrirá automáticamente en: http://localhost:8501
echo.

set /p ejecutar="¿Quieres ejecutar StrategySim Enterprise ahora? (S/N): "
if /i "%ejecutar%"=="S" (
    echo.
    echo 🚀 Iniciando aplicación...
    start EJECUTAR_STRATEGYSIM.bat
)

echo.
echo 💡 Tip: Puedes ejecutar la aplicación cuando quieras desde el escritorio
echo.
pause