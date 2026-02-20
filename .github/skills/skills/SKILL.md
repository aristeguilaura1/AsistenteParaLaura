---
name: revisar-automatizacion
description: Revisa y mejora scripts de automatización Python con enfoque en Selenium, notificaciones, y sincronización de repositorios. Analiza calidad de código, robustez, manejo de errores, y sugiere mejoras específicas para scripts de automatización empresarial.
---

# Skill: Revisar Automatización

## Propósito
Esta skill está diseñada para revisar y mejorar scripts de automatización Python, especialmente aquellos que usan:
- **Selenium WebDriver** para automatización web
- **Scripts de sincronización Git** 
- **Sistemas de notificación por email**
- **Automatización de tareas empresariales**

## Cuándo Usar Esta Skill
Utiliza esta skill cuando necesites:
- Revisar calidad de código en scripts de automatización
- Detectar problemas de robustez y manejo de errores
- Optimizar flujos de automatización con Selenium
- Mejorar scripts de notificación y sincronización
- Refactorizar código duplicado
- Implementar mejores prácticas en Python

## Palabras Clave
`automatización`, `selenium`, `webdriver`, `script`, `python`, `git`, `notificación`, `email`, `robustez`, `refactorizar`, `mejorar código`, `calidad`, `timecard`, `sync`

---

## Instrucciones Detalladas

### 1. Análisis de Calidad de Código

Cuando revises código de automatización, evalúa estos aspectos:

#### ✅ Estructura y Organización
- **Separación de responsabilidades**: Una clase o función = una responsabilidad
- **Código duplicado**: Identificar bloques repetidos > 10 líneas
- **Complejidad ciclomática**: Funciones no deben exceder 50 líneas
- **Configuración vs Lógica**: Separar valores hardcodeados

#### ⚠️ Robustez y Manejo de Errores
- **Excepciones específicas**: Evitar `except Exception` genérico
- **Reintentos automáticos**: Implementar con backoff exponencial
- **Logging estructurado**: Usar `logging` en lugar de `print()`
- **Verificación de estados**: Validar que las acciones se completaron correctamente

#### 🔧 Selenium Best Practices
- **Esperas explícitas**: Usar `WebDriverWait` en lugar de `time.sleep()`
- **Selectores robustos**: Preferir IDs > CSS > XPath
- **Manejo de elementos**: Verificar existencia antes de interactuar
- **Cleanup**: Asegurar cierre del driver en `finally` block

#### 📊 Mantenibilidad
- **Constantes**: Extraer magic numbers y strings
- **Type hints**: Agregar anotaciones de tipos
- **Docstrings**: Documentar funciones complejas
- **Tests**: Sugerir casos de prueba críticos

---

### 2. Plantillas de Refactorización

#### Extracción de Constantes
```python
# ❌ ANTES
time.sleep(5)
if total == "40":
    # ...

# ✅ DESPUÉS
class Config:
    TIMEOUT_CARGA = 5
    HORAS_SEMANA = 40

time.sleep(Config.TIMEOUT_CARGA)
if float(total) == Config.HORAS_SEMANA:
    # ...
```

#### Eliminación de Código Duplicado
```python
# ❌ ANTES
# Código repetido en múltiples lugares

# ✅ DESPUÉS
def _metodo_reutilizable(self, parametros):
    """Extrae lógica común"""
    # Implementación única
    pass
```

#### Logging Estructurado
```python
# ❌ ANTES
print("Error al guardar")

# ✅ DESPUÉS
import logging

logger = logging.getLogger(__name__)
logger.error("Error al guardar horas", extra={
    'usuario': username,
    'intentos': retry_count
})
```

#### Manejo de Excepciones Específico
```python
# ❌ ANTES
try:
    element.click()
except Exception as e:
    print(f"Error: {e}")

# ✅ DESPUÉS
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException,
    ElementClickInterceptedException
)

try:
    element.click()
except ElementClickInterceptedException:
    logger.warning("Elemento bloqueado, esperando...")
    time.sleep(2)
    element.click()
except NoSuchElementException:
    logger.error("Elemento no encontrado")
    return False
except TimeoutException:
    logger.error("Timeout esperando elemento")
    return False
```

---

### 3. Checklist de Revisión

Al revisar un script de automatización, verifica:

**Configuración y Setup**
- [ ] Credenciales/secretos NO están hardcodeados
- [ ] Rutas de archivos son configurables
- [ ] URLs son constantes nombradas
- [ ] Timeouts son configurables

**Selenium WebDriver**
- [ ] Driver se cierra correctamente (try-finally)
- [ ] Usa esperas explícitas (WebDriverWait)
- [ ] Maneja elementos obsoletos (StaleElementReferenceException)
- [ ] Screenshots en caso de error para debugging

**Robustez**
- [ ] Reintentos en operaciones críticas
- [ ] Validación de precondiciones
- [ ] Verificación de postcondiciones
- [ ] Logging de eventos importantes

**Mantenibilidad**
- [ ] Sin código duplicado > 10 líneas
- [ ] Funciones < 50 líneas
- [ ] Nombres descriptivos
- [ ] Comentarios solo donde es necesario

**Testing**
- [ ] Lógica de negocio separada de UI
- [ ] Funciones testables unitariamente
- [ ] Casos edge considerados

---

### 4. Priorización de Mejoras

Clasifica las mejoras sugeridas en:

#### 🔴 Prioridad ALTA (Hacer Inmediatamente)
- Bugs críticos que afectan funcionalidad
- Código duplicado extenso (>50 líneas)
- Falta de manejo de errores en operaciones críticas
- Memory leaks o recursos no liberados
- Credenciales expuestas

#### 🟡 Prioridad MEDIA (Esta Semana)
- Código duplicado moderado (10-50 líneas)
- Funciones muy largas (>100 líneas)
- Falta de logging
- Magic numbers/strings
- Manejo de excepciones genérico

#### 🟢 Prioridad BAJA (Cuando Haya Tiempo)
- Mejoras de estilo
- Optimizaciones de performance menores
- Documentación adicional
- Tests unitarios
- Type hints

---

### 5. Ejemplos de Salida

Cuando uses esta skill, proporciona:

1. **Puntuación general** (X/10) con justificación
2. **Lista de fortalezas** del código actual
3. **Problemas críticos** con ubicación exacta (líneas)
4. **Código refactorizado** con ejemplos específicos
5. **Plan de acción** priorizado
6. **Estimación de esfuerzo** (minutos/horas)

#### Formato de Respuesta:
```markdown
# 🔍 Revisión de Calidad - [nombre_archivo]

## 📊 Análisis General
**Puntuación: X/10**

### ✅ Fortalezas
- Punto fuerte 1
- Punto fuerte 2

### 🔴 Problemas Críticos
1. [Título del problema] (líneas X-Y)
   - Descripción
   - Impacto
   - Solución con código

### 🟡 Problemas de Mantenibilidad
[...]

### 🟢 Mejoras Sugeridas
[...]

## 📋 Plan de Acción
- [ ] Alta: Tarea 1 (30 min)
- [ ] Media: Tarea 2 (1 hora)
- [ ] Baja: Tarea 3 (2 horas)
```

---

## Ejemplos de Uso

### Ejemplo 1: Revisar Script de Selenium
```
Revisa el código de carga_horas_simple.py enfocándote en robustez y duplicación
```

### Ejemplo 2: Optimizar Manejo de Errores
```
Analiza el manejo de excepciones en sync_repositorio.py y sugiere mejoras
```

### Ejemplo 3: Refactorizar Código Duplicado
```
Encuentra código duplicado en notificador_cambios.py y propón una refactorización
```

### Ejemplo 4: Mejorar Logging
```
Revisa el logging actual y sugiere implementar logging estructurado
```

---

## Criterios de Éxito

Una revisión exitosa debe:
- ✅ Identificar problemas reales y priorizarlos
- ✅ Proporcionar código de ejemplo funcional
- ✅ Considerar el contexto del negocio
- ✅ Ser accionable (no solo teórico)
- ✅ Incluir estimaciones de esfuerzo
- ✅ Mantener balance entre perfección y pragmatismo

---

## Notas Adicionales

- **Contexto empresarial**: Considera que estos scripts corren en entornos productivos
- **Velocidad vs Calidad**: Prioriza cambios que dan máximo valor con mínimo esfuerzo
- **Backward compatibility**: Asegura que refactorizaciones no rompan funcionalidad existente
- **Iterativo**: Es mejor hacer mejoras incrementales que grandes reescrituras

---

## Comandos Relacionados

- `/explicar` - Para entender código complejo antes de refactorizar
- `/tests` - Para generar tests después de refactorizar
- `/documentar` - Para documentar código mejorado
- `@workspace` - Para buscar patrones similares en otros archivos