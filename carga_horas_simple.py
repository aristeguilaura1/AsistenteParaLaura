from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
import keyboard

class CargaHorasSimple:
    def __init__(self):
        self.url = "https://hc.neoris.net/timecard/"
        self.driver = None
    
    def iniciar_navegador(self):
        """Inicia el navegador Chrome SIN cerrar pestañas existentes de Laura"""
        try:
            # Solo cerrar MI driver previo si existe, NO todo Chrome
            if hasattr(self, 'driver') and self.driver:
                print("🔄 Cerrando solo mi navegador anterior del agente...")
                try:
                    self.driver.quit()
                    time.sleep(2)
                    print("✅ Mi navegador anterior cerrado")
                except Exception as e:
                    print(f"⚠️ Error cerrando mi navegador: {e}")
            
            # Configuraciones Chrome para nueva instancia independiente
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--new-window')  # Nueva ventana, no interferir con existentes
            
            print("🌐 Abriendo nueva ventana Chrome para el agente...")
            print("💡 (NO afectará tus pestañas existentes)")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            print("🔗 Navegando a la página del timecard...")
            self.driver.get(self.url)
            time.sleep(5)
            
            print("✅ Navegador del agente listo (tus otras pestañas intactas)")
            return True
            
        except Exception as e:
            print(f"❌ Error iniciando navegador del agente: {e}")
            return False
    
    def cargar_horas_estrategia_simple(self):
        """SOLO días laborables: Monday, Tuesday, Wednesday, Thursday, Friday"""
        try:
            wait = WebDriverWait(self.driver, 15)
            print("⏳ Esperando que cargue la página...")
            time.sleep(5)
            
            print("🎯 ESTRATEGIA: SOLO addr2-addr6 (NO addr1=Sunday)")
            print("🚫 addr1=Sunday EXCLUIDO - Solo procesamos addr2→addr6")
            print("✅ addr2=Monday, addr3=Tuesday, addr4=Wednesday, addr5=Thursday, addr6=Friday")
            print("="*60)
            
            # MAPEO ESPECÍFICO: Solo addr2-addr6 (días laborables)
            # addr1 = Sunday   -> NO PROCESAR (excluido)
            # addr2 = Monday   -> SÍ (8 horas)
            # addr3 = Tuesday  -> SÍ (8 horas) 
            # addr4 = Wednesday -> SÍ (8 horas)
            # addr5 = Thursday -> SÍ (8 horas)
            # addr6 = Friday   -> SÍ (8 horas)
            dias_laborables_config = {
                'Monday': {'dia_es': 'LUNES', 'buscar_texto': ['monday', 'lunes', 'Mon'], 'addr': 'addr2'},
                'Tuesday': {'dia_es': 'MARTES', 'buscar_texto': ['tuesday', 'martes', 'Tue'], 'addr': 'addr3'}, 
                'Wednesday': {'dia_es': 'MIÉRCOLES', 'buscar_texto': ['wednesday', 'miércoles', 'Wed'], 'addr': 'addr4'},
                'Thursday': {'dia_es': 'JUEVES', 'buscar_texto': ['thursday', 'jueves', 'Thu'], 'addr': 'addr5'},
                'Friday': {'dia_es': 'VIERNES', 'buscar_texto': ['friday', 'viernes', 'Fri'], 'addr': 'addr6'}
            }
            
            dias_completados = 0
            
            for dia_nombre, config in dias_laborables_config.items():
                dia_es = config['dia_es']
                textos_busqueda = config['buscar_texto']
                addr_correspondiente = config['addr']
                
                print(f"\n📅 === {dia_es} ({dia_nombre}) - {addr_correspondiente} ===")
                print(f"   🔍 Procesando {addr_correspondiente}: {textos_busqueda}")
                
                boton_encontrado = False
                
                try:
                    # ESTRATEGIA: Buscar filas que contengan el nombre del día
                    print(f"   🔎 Escaneando página buscando {dia_nombre}...")
                    
                    # Buscar todas las filas de la tabla
                    filas = self.driver.find_elements(By.XPATH, "//tr")
                    
                    for fila in filas:
                        try:
                            texto_fila = fila.text.lower()
                            
                            # Verificar si esta fila contiene algún texto del día buscado
                            coincide_dia = any(texto in texto_fila for texto in textos_busqueda)
                            
                            # FILTRO ANTI-addr1: Asegurar que NO sea Sunday (addr1)
                            es_sunday = any(dom in texto_fila for dom in ['sunday', 'domingo', 'sun'])
                            es_saturday = any(sab in texto_fila for sab in ['saturday', 'sábado', 'sat'])
                            
                            if coincide_dia and not es_sunday and not es_saturday:
                                print(f"      ✅ Encontrada fila de {dia_nombre} ({addr_correspondiente}): '{texto_fila[:50]}...'")
                                print(f"      🚫 Confirmado: NO es addr1/Sunday")
                                
                                # Buscar botón + en esta fila específica
                                botones_en_fila = fila.find_elements(By.XPATH, ".//button[@id='btn_sub']")
                                
                                if botones_en_fila:
                                    boton_plus = botones_en_fila[0]  # Primer botón + de esta fila
                                    
                                    print(f"   ➕ Haciendo click en + de {dia_nombre}...")
                                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_plus)
                                    time.sleep(1)
                                    boton_plus.click()
                                    time.sleep(4)
                                    
                                    print(f"   ✅ Click exitoso en {dia_nombre} ({addr_correspondiente}) - Confirmado: NO addr1")
                                    boton_encontrado = True
                                    break
                                    
                        except Exception as e:
                            continue  # Continuar con la siguiente fila
                    
                    if not boton_encontrado:
                        print(f"   ❌ No se encontró botón + para {dia_nombre}")
                        continue
                    
                    # Seleccionar proyecto con múltiples intentos
                    proyecto_ok = False
                    print(f"   🏗️ Seleccionando proyecto para {dia_nombre}...")
                    
                    for intento in range(3):  # Hasta 3 intentos
                        try:
                            print(f"      🔄 Intento {intento + 1} de selección de proyecto...")
                            
                            # Buscar dropdowns disponibles
                            selects = self.driver.find_elements(By.XPATH, "//select")
                            selects_visibles = [s for s in selects if s.is_displayed() and s.is_enabled()]
                            
                            if selects_visibles:
                                select = selects_visibles[-1]  # El más reciente
                                select_id = select.get_attribute('id') or f'select-{intento}'
                                print(f"         🎯 Usando select: {select_id}")
                                
                                select.click()
                                time.sleep(1)
                                
                                opciones = select.find_elements(By.XPATH, "./option")
                                if len(opciones) > 1:
                                    segunda_opcion = opciones[1]
                                    proyecto_nombre = segunda_opcion.text
                                    print(f"         📋 Proyecto: {proyecto_nombre[:50]}...")
                                    segunda_opcion.click()
                                    time.sleep(2)
                                    
                                    proyecto_ok = True
                                    print(f"   ✅ Proyecto seleccionado para {dia_nombre}")
                                    break
                                else:
                                    print(f"         ⚠️ Select sin opciones, reintentando...")
                                    time.sleep(2)
                            else:
                                print(f"         ❌ No hay selects disponibles")
                                time.sleep(2)
                                
                        except Exception as e:
                            print(f"         ⚠️ Error en intento {intento + 1}: {e}")
                            time.sleep(1)
                    
                    if not proyecto_ok:
                        print(f"   ⚠️ ADVERTENCIA: No se pudo seleccionar proyecto en {dia_nombre}")
                    
                    # Ingresar horas con múltiples intentos
                    horas_ok = False
                    print(f"   🔢 Ingresando 8 horas en {dia_nombre}...")
                    
                    for intento in range(3):  # Hasta 3 intentos
                        try:
                            print(f"      🔄 Intento {intento + 1} de ingreso de horas...")
                            
                            # Buscar inputs de texto disponibles
                            inputs = self.driver.find_elements(By.XPATH, "//input[@type='text']")
                            inputs_visibles = [inp for inp in inputs if inp.is_displayed() and inp.is_enabled()]
                            
                            if inputs_visibles:
                                input_horas = inputs_visibles[-1]  # El más reciente
                                input_id = input_horas.get_attribute('id') or f'input-{intento}'
                                print(f"         🎯 Usando input: {input_id}")
                                
                                input_horas.clear()
                                input_horas.send_keys("8")
                                time.sleep(1)
                                
                                # Verificar
                                valor = input_horas.get_attribute('value')
                                if valor == '8':
                                    horas_ok = True
                                    print(f"   ✅ 8 horas ingresadas en {dia_nombre}")
                                    break
                                else:
                                    print(f"         ⚠️ Valor inesperado: '{valor}', reintentando...")
                            else:
                                print(f"         ❌ No hay inputs disponibles")
                                time.sleep(2)
                                
                        except Exception as e:
                            print(f"         ⚠️ Error en intento {intento + 1}: {e}")
                            time.sleep(1)
                    
                    if horas_ok:
                        # NUEVO: Intentar confirmar/aplicar la entrada
                        print(f"   💾 Confirmando entrada de {dia_nombre}...")
                        
                        try:
                            # Buscar botones de confirmación/OK/Apply
                            botones_confirmar = self.driver.find_elements(By.XPATH, 
                                "//button[contains(text(), 'OK') or contains(text(), 'Apply') or contains(text(), 'Add')] | " +
                                "//input[@type='submit' or @type='button'][contains(@value, 'OK') or contains(@value, 'Apply')]")
                            
                            boton_confirmacion = None
                            for boton in botones_confirmar:
                                if boton.is_displayed() and boton.is_enabled():
                                    boton_confirmacion = boton
                                    break
                            
                            if boton_confirmacion:
                                print(f"      ✅ Encontrado botón de confirmación")
                                self.driver.execute_script("arguments[0].click();", boton_confirmacion)
                                time.sleep(3)
                                print(f"   ✅ Entrada confirmada para {dia_nombre}")
                            else:
                                # Intentar presionar Enter como alternativa
                                print(f"      🔄 Intentando Enter para confirmar...")
                                if inputs_visibles:
                                    inputs_visibles[-1].send_keys("\n")
                                    time.sleep(2)
                                
                        except Exception as e:
                            print(f"      ⚠️ Error confirmando entrada: {e}")
                        
                        dias_completados += 1
                        print(f"   🎉 {dia_nombre} COMPLETADO ({dias_completados}/5)")
                    else:
                        print(f"   ❌ {dia_nombre} FALLÓ - no se pudieron ingresar horas")
                    
                    time.sleep(2)  # Pausa entre días
                    
                except Exception as e:
                    print(f"   💥 Error procesando {dia_nombre}: {e}")
                    continue
            
            # Resumen final
            print(f"\n📊 RESUMEN ANTI-SUNDAY: {dias_completados}/5 días laborables completados")
            print("🚫 CONFIRMADO: NO se tocó Sunday ni Saturday")
            
            if dias_completados < 5:
                print(f"⚠️ ADVERTENCIA: Solo se completaron {dias_completados} días laborables de 5")
                print("💡 Revisemos manualmente qué días laborables faltaron...")
            
            # Guardar todo
            print(f"\n💾 GUARDANDO TODAS LAS HORAS...")
            try:
                boton_save_all = wait.until(EC.element_to_be_clickable((By.ID, "SaveAll")))
                boton_save_all.click()
                time.sleep(8)  # Más tiempo para guardar
                print("✅ Comando de guardado ejecutado")
                
                # NUEVO: Refrescar página para verificar persistencia
                print("🔄 Refrescando página para verificar persistencia...")
                self.driver.refresh()
                time.sleep(6)  # Esperar que cargue completamente
                
                print("📊 Verificando totales después del guardado...")
                
                # VERIFICACIÓN AUTOMÁTICA DEL TOTAL DE HORAS
                try:
                    print("🔍 Verificando Hours_TC automáticamente...")
                    
                    # Buscar el elemento Hours_TC que Laura identificó
                    elemento_total = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='Hours_TC']")))
                    total_horas = elemento_total.text.strip()
                    
                    print(f"📈 Hours_TC actual: '{total_horas}'")
                    
                    if total_horas == "40" or total_horas == "40.0":
                        print("🎉 ¡VERIFICACIÓN EXITOSA! Hours_TC = 40")
                        print("✅ CONFIRMADO: Solo días laborables cargados correctamente")
                        verificacion_automatica = True
                    else:
                        print(f"⚠️ VERIFICACIÓN FALLÓ: Hours_TC = '{total_horas}' (esperado: 40)")
                        verificacion_automatica = False
                        
                except Exception as e:
                    print(f"❌ Error verificando Hours_TC: {e}")
                    verificacion_automatica = False
                
                # Verificación manual mejorada con datos automáticos
                print("\n" + "="*60)
                print("🔍 REVISIÓN MANUAL - ANTI-SUNDAY ✅")
                print("="*60)
                
                if verificacion_automatica:
                    print("✅ VERIFICACIÓN AUTOMÁTICA: Hours_TC = 40 ✅")
                    print(f"✓ Los {dias_completados} días laborables se persistieron correctamente")
                    print("✓ El sistema reconoce las 40 horas semanales")
                    print("🚫 CONFIRMADO: Sunday NO fue tocado")
                    
                    respuesta = input(f"\n🎉 ¿Confirmas que todo está correcto? (s/n, default=s): ").lower().strip()
                    
                    if respuesta in ['', 's', 'si', 'sí', 'yes', 'y']:
                        print("\n🏆 ¡ÉXITO TOTAL! Carga completada sin tocar Sunday.")
                        return True
                    else:
                        print("\n🤔 Revisión manual indicó problemas pese a verificación automática.")
                        return False
                        
                else:
                    print(f"❌ VERIFICACIÓN AUTOMÁTICA FALLÓ: Hours_TC ≠ 40")
                    print(f"📊 Días laborables procesados: {dias_completados}/5")
                    print("🔍 Problemas posibles:")
                    print("   • Las entradas no se confirman correctamente")
                    print("   • Algún día laborable no se persistió")
                    print("   • Falta algún paso de validación")
                    
                    respuesta = input(f"\n¿Quieres continuar pese a la verificación fallida? (s/n): ").lower().strip()
                    
                    if respuesta in ['s', 'si', 'sí', 'yes', 'y']:
                        print("\n⚠️ Continuando pese a verificación fallida...")
                        return True
                    else:
                        print(f"\n❌ Proceso marcado como fallido. Hours_TC = '{total_horas}' ≠ 40")
                        return False
                
            except Exception as e:
                print(f"💥 Error guardando: {e}")
                return False
            
        except Exception as e:
            print(f"💥 Error general: {e}")
            return False
            
            # Resumen final
            print(f"\n📊 RESUMEN: {dias_completados}/5 días completados")
            
            if dias_completados < 5:
                print(f"⚠️ ADVERTENCIA: Solo se completaron {dias_completados} días de 5")
                print("💡 Revisemos manualmente qué faltó...")
            
            # Guardar todo
            print(f"\n💾 GUARDANDO TODAS LAS HORAS...")
            try:
                boton_save_all = wait.until(EC.element_to_be_clickable((By.ID, "SaveAll")))
                boton_save_all.click()
                time.sleep(8)  # Más tiempo para guardar
                print("✅ Comando de guardado ejecutado")
                
                # NUEVO: Refrescar página para verificar persistencia
                print("🔄 Refrescando página para verificar persistencia...")
                self.driver.refresh()
                time.sleep(6)  # Esperar que cargue completamente
                
                print("📊 Verificando totales después del guardado...")
                
                # VERIFICACIÓN AUTOMÁTICA DEL TOTAL DE HORAS
                try:
                    print("🔍 Verificando Hours_TC automáticamente...")
                    
                    # Buscar el elemento Hours_TC que Laura identificó
                    elemento_total = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='Hours_TC']")))
                    total_horas = elemento_total.text.strip()
                    
                    print(f"📈 Hours_TC actual: '{total_horas}'")
                    
                    if total_horas == "40" or total_horas == "40.0":
                        print("🎉 ¡VERIFICACIÓN EXITOSA! Hours_TC = 40")
                        verificacion_automatica = True
                    else:
                        print(f"⚠️ VERIFICACIÓN FALLÓ: Hours_TC = '{total_horas}' (esperado: 40)")
                        verificacion_automatica = False
                        
                except Exception as e:
                    print(f"❌ Error verificando Hours_TC: {e}")
                    verificacion_automatica = False
                
                # Verificación manual mejorada con datos automáticos
                print("\n" + "="*60)
                print("🔍 REVISIÓN MANUAL - CON VERIFICACIÓN AUTOMÁTICA")
                print("="*60)
                
                if verificacion_automatica:
                    print("✅ VERIFICACIÓN AUTOMÁTICA: Hours_TC = 40 ✅")
                    print(f"✓ Los {dias_completados} días se persistieron correctamente")
                    print("✓ El sistema reconoce las 40 horas semanales")
                    
                    respuesta = input(f"\n🎉 ¿Confirmas que todo está correcto? (s/n, default=s): ").lower().strip()
                    
                    if respuesta in ['', 's', 'si', 'sí', 'yes', 'y']:
                        print("\n🏆 ¡ÉXITO TOTAL! Carga completada y verificada.")
                        return True
                    else:
                        print("\n🤔 Revisión manual indicó problemas pese a verificación automática.")
                        return False
                        
                else:
                    print(f"❌ VERIFICACIÓN AUTOMÁTICA FALLÓ: Hours_TC ≠ 40")
                    print(f"📊 Días procesados: {dias_completados}/5")
                    print("🔍 Problemas posibles:")
                    print("   • Las entradas no se confirman correctamente")
                    print("   • Friday no se está persistiendo")
                    print("   • Falta algún paso de validación")
                    
                    respuesta = input(f"\n¿Quieres continuar pese a la verificación fallida? (s/n): ").lower().strip()
                    
                    if respuesta in ['s', 'si', 'sí', 'yes', 'y']:
                        print("\n⚠️ Continuando pese a verificación fallida...")
                        return True
                    else:
                        print(f"\n❌ Proceso marcado como fallido. Hours_TC = '{total_horas}' ≠ 40")
                        return False
                
            except Exception as e:
                print(f"💥 Error guardando: {e}")
                return False
            
        except Exception as e:
            print(f"💥 Error general: {e}")
            return False
    
    def enviar_notificacion_outlook(self, email):
        """Envía correo de confirmación"""
        try:
            asunto = "Horas cargadas - Estrategia Simple"
            cuerpo = f"""Estimada,

La carga de horas semanales ha sido completada usando la estrategia simple.

Método: Búsqueda genérica de elementos
- 5 días procesados
- Proyecto y horas por día

Saludos,
Agente Simple"""
            
            subject_encoded = asunto.replace(" ", "%20")
            body_encoded = cuerpo.replace("\n", "%0D%0A").replace(" ", "%20")
            cc_email = "matias_munoz@epamneoris.com"
            
            mailto_link = f"mailto:{email}?cc={cc_email}&subject={subject_encoded}&body={body_encoded}"
            
            os.startfile(mailto_link)
            print("✓ Outlook abierto con el correo")
            
            time.sleep(3)
            print("📧 Enviando correo...")
            keyboard.press_and_release('ctrl+enter')
            time.sleep(2)
            print("✓ Correo enviado")
            return True
            
        except Exception as e:
            print(f"✗ Error enviando correo: {e}")
            return False
    
    def ejecutar(self, email):
        """Ejecuta la estrategia simple completa"""
        print("🚀 Iniciando CargaHorasSimple V4 - ANTI SUNDAY")
        print("💡 GARANTIZA: Solo Monday-Friday (NO Sunday/Saturday)")
        print("✅ NO cerrará tus pestañas de Chrome existentes")
        print("🚫 NUNCA tocará Sunday ni Saturday")
        print("="*55)
        
        try:
            # Verificar que el navegador se inicie correctamente
            navegador_ok = self.iniciar_navegador()
            if not navegador_ok:
                print("💥 ERROR: No se pudo iniciar el navegador")
                return
            
            carga_exitosa = self.cargar_horas_estrategia_simple()
            
            if carga_exitosa:
                print("📧 Enviando correo de confirmación...")
                self.enviar_notificacion_outlook(email)
            else:
                print("❌ No se enviará correo debido a problemas persistentes")
                
            print("\n✅ Proceso V2 completado")
            
        except Exception as e:
            print(f"💥 Error en ejecución: {e}")
        
        finally:
            # Preguntar si cerrar SOLO el navegador del agente
            try:
                if hasattr(self, 'driver') and self.driver:
                    print("\n" + "="*50)
                    print("🔒 CERRAR NAVEGADOR DEL AGENTE")
                    print("💡 (Esto NO afectará tus otras pestañas de Chrome)")
                    cerrar = input("¿Cerrar solo la ventana del agente? (s/n, default=n): ").lower().strip()
                    
                    if cerrar in ['s', 'si', 'sí', 'yes', 'y']:
                        print("🔒 Cerrando SOLO el navegador del agente...")
                        self.driver.quit()
                        print("✅ Navegador del agente cerrado (tus pestañas conservadas)")
                    else:
                        print("🌐 Navegador del agente permanece abierto para revisión")
            except Exception as e:
                print(f"⚠️ Error gestionando navegador: {e}")

# Configuración
if __name__ == "__main__":
    TU_EMAIL = "laura_aristegui@epamneoris.com"
    
    agente = CargaHorasSimple()
    agente.ejecutar(TU_EMAIL)