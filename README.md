# 🎯 AsistenteParaLaura - CargaHorasSimple V4

Automatización semanal para carga de horas en el sistema NEORIS Timecard.

## 🚀 Archivo Principal

**`carga_horas_simple.py`** - CargaHorasSimple V4 - ANTI SUNDAY

### ✅ Garantías del Sistema:
- 🚫 **NUNCA toca addr1** (Sunday) 
- ✅ **SOLO procesa addr2-addr6** (Monday-Friday)
- ✅ **40 horas exactas** distribuidas en días laborables
- ✅ **No interfiere** con pestañas Chrome existentes
- ✅ **Email automático** con copia a Matías Muñoz

## 🎪 Uso Semanal

```bash
python carga_horas_simple.py
```

## 📊 Mapeo de Días

```
🚫 addr1 = Sunday    -> EXCLUIDO
✅ addr2 = Monday    -> 8 horas  
✅ addr3 = Tuesday   -> 8 horas
✅ addr4 = Wednesday -> 8 horas
✅ addr5 = Thursday  -> 8 horas
✅ addr6 = Friday    -> 8 horas
```

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

## 📧 Email Automático

El sistema envía automáticamente email de confirmación:
- **Para:** laura_aristegui@epamneoris.com  
- **CC:** matias_munoz@epamneoris.com
- **Contenido:** Resumen completo de las 40 horas cargadas

## 🛡️ Características de Seguridad

### 🚫 Anti-Sunday Protection
- **Triple filtro** para evitar cargar horas en Sunday
- **Verificación explícita** que NO sea addr1
- **Confirmación visual** en cada día procesado

### ✅ Verificación Automática
- **Hours_TC = 40** validado automáticamente
- **Persistencia confirmada** después del guardado
- **Reporte detallado** de días procesados vs. excluidos

### 🌐 Navegador Independiente
- **Nueva ventana** exclusiva para el agente
- **Respeta pestañas existentes** de Chrome
- **No interfiere** con el trabajo del usuario

## 📈 Proceso Automático

1. **Inicialización**: Nueva ventana Chrome del agente
2. **Navegación**: Acceso automático a timecard NEORIS
3. **Procesamiento**: Solo addr2-addr6 (Monday-Friday)
4. **Carga**: 8 horas por día laborable (total 40)
5. **Verificación**: Hours_TC = 40 confirmado
6. **Guardado**: Persistencia automática de datos
7. **Email**: Confirmación con copia a Matías
8. **Finalización**: Opción de cerrar ventana del agente

## 🎯 Versión Actual: V4 - ANTI SUNDAY

**Fecha:** 06/02/2026  
**Estado:** ✅ Funcional y probado  
**Última mejora:** Exclusión absoluta de addr1 (Sunday)  

---

*AsistenteParaLaura - Automatización confiable para tu timecard semanal* 🚀
