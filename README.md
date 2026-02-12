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
- ⚡ **100% automático** - Sin confirmaciones manuales

## 🎪 Uso Semanal

```bash
python carga_horas_simple.py
```

**⚡ Proceso 100% automático** - Sin confirmaciones manuales necesarias

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

## 📈 Proceso 100% Automático

1. **Inicialización**: Nueva ventana Chrome del agente
2. **Navegación**: Acceso automático a timecard NEORIS
3. **Procesamiento**: Solo addr2-addr6 (Monday-Friday)
4. **Carga**: 8 horas por día laborable (total 40)
5. **Verificación**: Hours_TC = 40 confirmado automáticamente
6. **Guardado**: Persistencia automática de datos
7. **Cierre navegador**: Automático al finalizar
8. **Email**: Envío automático con copia a Matías
9. **Finalización**: Sin intervención manual requerida

⚡ **Cero intervención manual** - El agente ejecuta todo el flujo de forma autónoma

## 🎯 Versión Actual: V4.1 - ANTI SUNDAY + TOTALMENTE AUTOMÁTICO

**Fecha:** 12/02/2026  
**Estado:** ✅ Funcional y probado  
**Última mejora:** Automatización completa sin confirmaciones manuales

### Changelog V4.1:
- ✅ Eliminadas confirmaciones manuales
- ✅ Cierre automático del navegador
- ✅ Envío automático de email
- ✅ Flujo 100% autónomo  

---

*AsistenteParaLaura - Automatización confiable para tu timecard semanal* 🚀
