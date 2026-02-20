# 🎯 AsistenteParaLaura - CargaHorasSimple V5

Automatización semanal para carga de horas en el sistema NEORIS Timecard.

## 🚀 Archivo Principal

**`carga_horas_simple.py`** - CargaHorasSimple V5 - ANTI SUNDAY + DETECCIÓN FERIADOS

### ✅ Garantías del Sistema:
- 🚫 **NUNCA toca addr1** (Sunday) 
- ✅ **SOLO procesa addr2-addr6** (Monday-Friday)
- 🏖️ **DETECTA feriados automáticamente** y los salta
- ✅ **Calcula horas dinámicamente** según días laborables disponibles
- ✅ **No interfiere** con pestañas Chrome existentes
- ✅ **Email automático** con copia a Matías Muñoz
- ⚡ **100% automático** - Sin confirmaciones manuales

### 🏖️ Detección Inteligente de Feriados (NUEVO en V5)

El agente **detecta automáticamente** días con horas pre-cargadas (feriados) y los salta:

**Proceso de detección:**
1. **Verifica Hours_TC** al inicio (`//*[@id="Hours_TC"]`)
   - Si es > 0 → hay horas pre-cargadas, activar detección
2. **Por cada día** (Monday-Friday):
   - Lee `Mon_hours`, `Tue_hours`, `Wed_hours`, `Thu_hours`, `Fri_hours`
   - Si el valor > 0 → **SALTA ese día** (ya tiene horas)
   - Si el valor = 0 → **CARGA 8 horas** en ese día
3. **Calcula totales correctamente**: Horas previas + Horas nuevas

**Ejemplo con feriados lunes y martes:**
```
Inicio: Hours_TC = 16 horas (detectadas)

📅 Monday    → Mon_hours = 8 → 🏖️ SALTADO
📅 Tuesday   → Tue_hours = 8 → 🏖️ SALTADO
📅 Wednesday → Wed_hours = 0 → ✅ CARGAR 8h
📅 Thursday  → Thu_hours = 0 → ✅ CARGAR 8h
📅 Friday    → Fri_hours = 0 → ✅ CARGAR 8h

Resultado: 16 (previas) + 24 (nuevas) = 40 horas ✅
```

**Ventajas:**
- ✅ No duplica horas en feriados cargados por la empresa
- ✅ Funciona con cualquier cantidad de feriados
- ✅ Detección robusta basada en XPaths confiables
- ✅ Adaptación automática a semanas irregulares

## 🎪 Uso Semanal

```bash
python carga_horas_simple.py
```

**⚡ Proceso 100% automático** - Sin confirmaciones manuales necesarias

## 📊 Mapeo de Días

```
🚫 addr1 = Sunday    -> EXCLUIDO (nunca se procesa)
✅ addr2 = Monday    -> 8 horas (si Mon_hours = 0)
✅ addr3 = Tuesday   -> 8 horas (si Tue_hours = 0)
✅ addr4 = Wednesday -> 8 horas (si Wed_hours = 0)
✅ addr5 = Thursday  -> 8 horas (si Thu_hours = 0)
✅ addr6 = Friday    -> 8 horas (si Fri_hours = 0)
```

**Detección de feriados:** Si un día ya tiene horas > 0, se salta automáticamente.

## 🔧 Requisitos

- Python 3.8+
- Google Chrome instalado
- Conexión a internet
- Acceso a https://hc.neoris.net/timecard/
- Usuario ya autenticado en el timecard

## 📦 Instalación

```bash
# Instalar dependencias
python -m pip install selenium schedule webdriver-manager keyboard

# Ejecutar agente
python carga_horas_simple.py
```

## 📧 Sistema de Notificaciones

### Enviar notificación automática a Matías

Después de hacer cambios, usa:

```bash
# Con mensaje inline
python sync_repositorio.py "Tu mensaje de commit aquí"

# O sin mensaje (te pide escribirlo)
python sync_repositorio.py
```

**Qué hace:**
1. ✅ Verifica cambios pendientes
2. 📦 Prepara los archivos modificados
3. 💾 Realiza el commit
4. 🚀 Hace push al repositorio
5. 📧 Envía mail automático a Matías con detalles del cambio

## 📧 Email Automático

El sistema envía automáticamente email de confirmación:
- **Para:** laura_aristegui@epamneoris.com  
- **CC:** matias_munoz@epamneoris.com
- **Contenido:** Resumen de horas cargadas (incluye días procesados y feriados saltados)

## 🛡️ Características de Seguridad

### 🚫 Anti-Sunday Protection
- **Triple filtro** para evitar cargar horas en Sunday
- **Verificación explícita** que NO sea addr1
- **Confirmación visual** en cada día procesado

### ✅ Verificación Automática Inteligente
- **Hours_TC** validado automáticamente (considera horas previas + nuevas)
- **Detección de feriados** mediante X_hours (Mon_hours, Tue_hours, etc.)
- **Persistencia confirmada** después del guardado
- **Reporte detallado** de días procesados, feriados saltados y totales

### 🌐 Navegador Independiente
- **Nueva ventana** exclusiva para el agente
- **Respeta pestañas existentes** de Chrome
- **No interfiere** con el trabajo del usuario

## 📈 Proceso 100% Automático

1. **Inicialización**: Nueva ventana Chrome del agente
2. **Navegación**: Acceso automático a timecard NEORIS
3. **Detección inicial**: Verifica Hours_TC para detectar horas pre-cargadas
4. **Procesamiento**: Solo addr2-addr6 (Monday-Friday)
   - Por cada día: verifica X_hours (Mon_hours, Tue_hours, etc.)
   - Si > 0: SALTA (feriado/ya cargado)
   - Si = 0: CARGA 8 horas
5. **Guardado**: Persistencia automática de datos
6. **Verificación inteligente**: Valida horas previas + horas nuevas = total correcto
7. **Cierre navegador**: Automático al finalizar
8. **Email**: Envío automático con copia a Matías
9. **Finalización**: Sin intervención manual requerida

⚡ **Cero intervención manual** - El agente ejecuta todo el flujo de forma autónoma
🏖️ **Detección inteligente** - Salta automáticamente feriados pre-cargados

## 🎯 Versión Actual: V5.0 - ANTI SUNDAY + DETECCIÓN FERIADOS

**Fecha:** 20/02/2026  
**Características:** Detección inteligente de feriados, salto automático de días pre-cargados  
**Estado:** ✅ Funcional y probado  
**Última mejora:** Automatización completa sin confirmaciones manuales

### Changelog V4.1:
- ✅ Eliminadas confirmaciones manuales
- ✅ Cierre automático del navegador
- ✅ Envío automático de email
- ✅ Flujo 100% autónomo  

---

*AsistenteParaLaura - Automatización confiable para tu timecard semanal* 🚀
