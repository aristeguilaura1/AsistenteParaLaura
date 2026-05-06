"""
Script de preview para ver el diseño del email sin ejecutar la carga completa
"""
import os
import time

# Datos de ejemplo
dias_cargados = 5
feriados_saltados = 0
feriados_nombres = []
horas_previas = 0
horas_nuevas = 40
horas_totales = 40
url_navegador = "https://hc.neoris.net/timecard/"
email = "laura_aristegui@epamneoris.com"
cc_email = "matias_munoz@epamneoris.com;mauro_centurion@epamneoris.com"

# Construir resumen
if feriados_saltados > 0:
    resumen_feriados = f"\n   🏖️ Feriados: {', '.join(feriados_nombres)}"
else:
    resumen_feriados = ""

asunto = f"✅ Horas cargadas - Semana {dias_cargados} días"
cuerpo = f"""Hola Laura,

✅ CARGA COMPLETADA EXITOSAMENTE

───────────────────────────────────────────────
📊 RESUMEN DE LA SEMANA
───────────────────────────────────────────────
   ✅ Días cargados: {dias_cargados} días
   🚫 Feriados saltados: {feriados_saltados}{resumen_feriados}

───────────────────────────────────────────────
💼 DETALLE DE HORAS
───────────────────────────────────────────────
   • Horas previas: {horas_previas}h
   • Horas cargadas: {horas_nuevas}h
   • TOTAL SEMANAL: {horas_totales}h

───────────────────────────────────────────────
🔒 VALIDACIONES
───────────────────────────────────────────────
   🚫 Sunday/Saturday: NO procesados
   ✅ Detección de feriados: Automática
   ✅ Verificación de totales: OK

───────────────────────────────────────────────
🔗 ACCESO RÁPIDO
───────────────────────────────────────────────

   🌐 Link del timecard: {url_navegador}

   ⏰ Próximo paso: Submitear las horas antes del viernes

───────────────────────────────────────────────

Saludos,
AsistenteParaLaura | EPAM-NEORIS TimeCard Bot"""

subject_encoded = asunto.replace(" ", "%20")
body_encoded = cuerpo.replace("\n", "%0D%0A").replace(" ", "%20")

mailto_link = f"mailto:{email}?cc={cc_email}&subject={subject_encoded}&body={body_encoded}"

print("📧 Abriendo preview del email...")
print(f"✉️  Para: {email}")
print(f"📋 CC: {cc_email}")
print(f"📌 Asunto: {asunto}")
print("\n" + "="*70)
print("CONTENIDO DEL EMAIL:")
print("="*70)
print(cuerpo)
print("="*70)
print("\n🔓 Abriendo Outlook con el email de preview...")

os.startfile(mailto_link)
time.sleep(2)

print("✅ Email abierto en Outlook")
print("💡 Puedes revisar el diseño y cerrar sin enviar")
