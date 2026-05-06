"""
Script para enviar email con resumen de mejoras realizadas al AsistenteParaLaura
"""
import os
import time
from datetime import datetime

# Destinatarios
email_laura = "laura_aristegui@epamneoris.com"
email_mati = "matias_munoz@epamneoris.com"
email_mauro = "mauro_centurion@epamneoris.com"
destinatarios = f"{email_laura};{email_mati};{email_mauro}"

# Fecha de hoy
fecha_hoy = datetime.now().strftime("%d/%m/%Y")

asunto = f"🚀 Mejoras Implementadas - AsistenteParaLaura | {fecha_hoy}"

cuerpo = f"""Hola equipo,

🎉 NUEVAS MEJORAS IMPLEMENTADAS

Les comparto las mejoras realizadas hoy al AsistenteParaLaura (bot de carga automática de TimeCard):

═══════════════════════════════════════════════
📧 MEJORAS EN EMAIL DE NOTIFICACIÓN
═══════════════════════════════════════════════

   ✅ Diseño corporativo EPAM-NEORIS
      • Secciones con separadores visuales
      • Iconos de colores para mejor lectura
      • Formato limpio y profesional

   🔗 Link directo al TimeCard
      • URL del navegador incluida en el email
      • Acceso rápido post-carga
      • Link clickeable automático

   📊 Información detallada
      • Resumen de días cargados
      • Detección de feriados
      • Totales de horas (previas + nuevas)
      • Validaciones automáticas

═══════════════════════════════════════════════
⚡ POPUP DE CONFIRMACIÓN
═══════════════════════════════════════════════

   🎨 Diseño eléctrico EPAM-NEORIS
      • Colores corporativos (azul eléctrico #00D4FF)
      • Patrón hexagonal de fondo
      • Animaciones y efectos hover

   🔘 Botón directo al TimeCard
      • Abre el navegador en la URL correcta
      • Efecto hover profesional
      • Mensaje de confirmación claro

   💬 Recordatorio visual
      • "Recordá submitear antes del viernes"
      • Confirmación de carga exitosa

═══════════════════════════════════════════════
🛠️ MEJORAS TÉCNICAS
═══════════════════════════════════════════════

   ⚙️ Captura de URL
      • Guarda URL del navegador antes de cerrar
      • Se incluye en email y popup
      • Permite acceso rápido posterior

   🎯 UX mejorada
      • Feedback visual claro
      • Navegación simplificada
      • Proceso más intuitivo

   📬 Sistema de notificación de mejoras (¡NUEVO!)
      • Script automático: enviar_mejoras.py
      • Envío de email al equipo cada vez que hay mejoras
      • Resumen detallado de cambios implementados
      • Documentación automática de evolución del proyecto

═══════════════════════════════════════════════
📋 ARCHIVOS ACTUALIZADOS
═══════════════════════════════════════════════

   • carga_horas_simple.py (script principal)
   • preview_email.py (preview del email)
   • preview_popup.py (preview del popup)
   • enviar_mejoras.py (notificación automática de mejoras) ⭐ NUEVO

═══════════════════════════════════════════════
🔄 PRÓXIMOS PASOS
═══════════════════════════════════════════════

   ✓ Sistema operativo y funcional
   ✓ Listo para uso en producción
   📌 Ejecutar: python carga_horas_simple.py
   
   💡 Nuevas mejoras:
      • Se notificarán automáticamente usando enviar_mejoras.py
      • Todo el equipo estará al tanto de cambios
      • Documentación continua del proyecto

═══════════════════════════════════════════════

Cualquier duda o sugerencia, por favor comentar.

Saludos,
AsistenteParaLaura Dev Team
{fecha_hoy}"""

# Encodear para mailto
subject_encoded = asunto.replace(" ", "%20")
body_encoded = cuerpo.replace("\n", "%0D%0A").replace(" ", "%20")

mailto_link = f"mailto:{destinatarios}?subject={subject_encoded}&body={body_encoded}"

print("📧 ENVÍO DE EMAIL DE MEJORAS")
print("="*70)
print(f"📅 Fecha: {fecha_hoy}")
print(f"👥 Para: Laura, Mati, Mauro")
print(f"📌 Asunto: {asunto}")
print("="*70)
print("\n📄 CONTENIDO:")
print(cuerpo)
print("\n" + "="*70)
print("\n🔓 Abriendo Outlook con el email...")

os.startfile(mailto_link)
time.sleep(3)

print("✅ Email abierto en Outlook")
print("💡 Revisá el contenido y presioná Ctrl+Enter para enviar")
print("\n✨ ¡Listo para compartir las mejoras con el equipo!")
