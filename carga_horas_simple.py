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
from dotenv import load_dotenv
import logging
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import webbrowser
import math

# Cargar configuración desde .env
load_dotenv()

class CargaHorasSimple:
    def __init__(self):
        # Cargar configuración desde variables de entorno
        self.url = os.getenv('TIMECARD_URL', 'https://hc.neoris.net/timecard/')
        self.horas_por_dia = int(os.getenv('HORAS_POR_DIA', '8'))
        self.email_cc = os.getenv('EMAIL_CC', 'matias_munoz@epamneoris.com')
        self.driver = None
        
        # Configurar logging
        self.timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.log_file = f'logs/carga_{self.timestamp}.log'
        self._configurar_logger()
        
        self.logger.info("="*70)
        self.logger.info("AsistenteParaLaura - CargaHorasSimple V5.2")
        self.logger.info(f"Inicio de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info("="*70)
        self.logger.info("⚙️ Configuración cargada desde .env:")
        self.logger.info(f"   📧 Email CC: {self.email_cc}")
        self.logger.info(f"   ⏰ Horas por día: {self.horas_por_dia}")
        self.logger.info(f"   🔗 URL: {self.url}")
        
        print("⚙️ Configuración cargada desde .env:")
        print(f"   📧 Email CC: {self.email_cc}")
        print(f"   ⏰ Horas por día: {self.horas_por_dia}")
        print(f"   📄 Log: {self.log_file}")
    
    def _configurar_logger(self):
        """Configura el sistema de logging"""
        # Crear directorio logs si no existe
        os.makedirs('logs', exist_ok=True)
        
        # Configurar logger
        self.logger = logging.getLogger('CargaHoras')
        self.logger.setLevel(logging.INFO)
        
        # Handler para archivo
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Formato del log
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # Limpiar handlers previos y agregar nuevo
        self.logger.handlers.clear()
        self.logger.addHandler(file_handler)
    
    def iniciar_navegador(self):
        """Inicia el navegador Chrome SIN cerrar pestañas existentes de Laura"""
        try:
            self.logger.info("Iniciando navegador Chrome...")
            # Solo cerrar MI driver previo si existe, NO todo Chrome
            if hasattr(self, 'driver') and self.driver:
                print("🔄 Cerrando solo mi navegador anterior del agente...")
                self.logger.info("Cerrando navegador anterior del agente")
                try:
                    self.driver.quit()
                    time.sleep(2)
                    print("✅ Mi navegador anterior cerrado")
                    self.logger.info("Navegador anterior cerrado correctamente")
                except Exception as e:
                    print(f"⚠️ Error cerrando mi navegador: {e}")
                    self.logger.warning(f"Error cerrando navegador anterior: {e}")
            
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
            self.logger.info("Navegador Chrome iniciado correctamente")
            return True
            
        except Exception as e:
            print(f"❌ Error iniciando navegador del agente: {e}")
            self.logger.error(f"Error iniciando navegador: {e}")
            return False
    
    def verificar_horas_iniciales(self):
        """Verifica si ya hay horas cargadas al inicio"""
        try:
            wait = WebDriverWait(self.driver, 10)
            elemento_hours = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='Hours_TC']")))
            horas_actuales = elemento_hours.text.strip()
            
            print(f"\n📊 Horas totales al inicio: {horas_actuales}")
            self.logger.info(f"Horas totales detectadas al inicio: {horas_actuales}")
            
            if horas_actuales not in ['0', '0.0', '']:
                print(f"⚠️ DETECTADAS horas pre-cargadas: {horas_actuales} horas")
                print("💡 Verificaré cada día para detectar feriados/entradas aprobadas")
                self.logger.info(f"Horas pre-cargadas detectadas: {horas_actuales} (posibles feriados)")
                return True, horas_actuales
            else:
                print("✅ No hay horas pre-cargadas")
                self.logger.info("No hay horas pre-cargadas, semana normal")
                return False, "0"
                
        except Exception as e:
            print(f"⚠️ Error verificando horas iniciales: {e}")
            self.logger.error(f"Error verificando horas iniciales: {e}")
            return False, "0"
    
    def verificar_horas_en_dia(self, dia_hours_id):
        """
        Verifica si un día específico ya tiene horas cargadas
        usando el XPath //*[@id="Mon_hours"], //*[@id="Tue_hours"], etc.
        """
        try:
            elemento_horas = self.driver.find_element(By.XPATH, f"//*[@id='{dia_hours_id}']")
            horas_dia = elemento_horas.text.strip()
            
            # Convertir a número para comparar
            try:
                horas_num = float(horas_dia) if horas_dia else 0
                if horas_num > 0:
                    return True, horas_num
                else:
                    return False, 0
            except ValueError:
                return False, 0
            
        except Exception as e:
            # Si no se encuentra el elemento, asumir que no hay horas
            return False, 0
    
    def cargar_horas_estrategia_simple(self):
        """SOLO días laborables: Monday, Tuesday, Wednesday, Thursday, Friday"""
        try:
            wait = WebDriverWait(self.driver, 15)
            print("⏳ Esperando que cargue la página...")
            time.sleep(5)
            
            # NUEVO: Verificar horas iniciales
            hay_horas_previas, horas_previas = self.verificar_horas_iniciales()
            
            print("\n🎯 ESTRATEGIA: SOLO addr2-addr6 (NO addr1=Sunday)")
            print("🏖️ DETECCIÓN: Saltará automáticamente días feriados ya aprobados")
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
                'Monday': {
                    'dia_es': 'LUNES', 
                    'buscar_texto': ['monday', 'lunes', 'Mon'], 
                    'addr': 'addr2',
                    'hours_id': 'Mon_hours'
                },
                'Tuesday': {
                    'dia_es': 'MARTES', 
                    'buscar_texto': ['tuesday', 'martes', 'Tue'], 
                    'addr': 'addr3',
                    'hours_id': 'Tue_hours'
                }, 
                'Wednesday': {
                    'dia_es': 'MIÉRCOLES', 
                    'buscar_texto': ['wednesday', 'miércoles', 'Wed'], 
                    'addr': 'addr4',
                    'hours_id': 'Wed_hours'
                },
                'Thursday': {
                    'dia_es': 'JUEVES', 
                    'buscar_texto': ['thursday', 'jueves', 'Thu'], 
                    'addr': 'addr5',
                    'hours_id': 'Thu_hours'
                },
                'Friday': {
                    'dia_es': 'VIERNES', 
                    'buscar_texto': ['friday', 'viernes', 'Fri'], 
                    'addr': 'addr6',
                    'hours_id': 'Fri_hours'
                }
            }
            
            dias_completados = 0
            dias_saltados_feriado = 0
            dias_saltados_nombres = []
            
            for dia_nombre, config in dias_laborables_config.items():
                dia_es = config['dia_es']
                textos_busqueda = config['buscar_texto']
                addr_correspondiente = config['addr']
                hours_id = config['hours_id']
                
                print(f"\n📅 === {dia_es} ({dia_nombre}) - {addr_correspondiente} ===")
                print(f"   🔍 Procesando {addr_correspondiente}: {textos_busqueda}")
                
                # NUEVO: Verificar si este día ya tiene horas cargadas
                if hay_horas_previas:
                    print(f"   🔎 Verificando {hours_id}...")
                    tiene_horas, horas_cargadas = self.verificar_horas_en_dia(hours_id)
                    
                    if tiene_horas:
                        print(f"      🏖️ DÍA CON HORAS DETECTADO: {dia_nombre} ya tiene {horas_cargadas} horas!")
                        print(f"         ⏭️ SALTANDO {dia_nombre} - No se cargará")
                        dias_saltados_feriado += 1
                        dias_saltados_nombres.append(dia_nombre)
                        continue
                    else:
                        print(f"      ✅ {hours_id} = 0, proceder a cargar")
                
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
            print(f"\n📊 RESUMEN ANTI-SUNDAY:")
            print(f"   ✅ Días cargados: {dias_completados}")
            print(f"   🏖️ Feriados saltados: {dias_saltados_feriado}")
            if dias_saltados_nombres:
                print(f"      Días feriados: {', '.join(dias_saltados_nombres)}")
            print(f"   📌 Total días procesables: {5 - dias_saltados_feriado}")
            print("   🚫 CONFIRMADO: NO se tocó Sunday ni Saturday")
            
            # Calcular horas esperadas
            horas_esperadas = (5 - dias_saltados_feriado) * 8
            
            try:
                horas_previas_num = float(horas_previas) if horas_previas else 0
            except:
                horas_previas_num = 0
            
            if horas_previas_num > 0:
                print(f"\n💡 Horas a cargar: {horas_esperadas}h (en {5 - dias_saltados_feriado} días × 8h)")
                print(f"   Horas previas: {horas_previas_num}h (feriados)")
                print(f"   Total esperado: {horas_previas_num + horas_esperadas}h")
            else:
                print(f"\n💡 Horas esperadas a cargar: {horas_esperadas} ({5 - dias_saltados_feriado} días × 8h)")
            
            dias_esperados = 5 - dias_saltados_feriado
            if dias_completados < dias_esperados:
                print(f"⚠️ ADVERTENCIA: Solo se completaron {dias_completados} días de {dias_esperados} procesables")
                print("💡 Revisemos manualmente qué días laborables faltaron...")
            
            # Caso especial: Si no hay días que cargar (todos son feriados)
            if dias_completados == 0 and dias_saltados_feriado == 5:
                print(f"\n🏖️ SEMANA COMPLETA CON FERIADOS/HORAS PREVIAS")
                print(f"✅ No hay días nuevos que cargar - Todo está completo")
                print(f"📊 Total semanal: {horas_previas_num}h")
                
                return {
                    'exito': True,
                    'dias_cargados': 0,
                    'feriados_saltados': dias_saltados_feriado,
                    'feriados_nombres': dias_saltados_nombres,
                    'horas_previas': horas_previas_num,
                    'horas_nuevas': 0,
                    'horas_totales': horas_previas_num
                }
            
            # Guardar solo si hay días nuevos cargados
            if dias_completados == 0:
                print("\n⚠️ No se cargaron días nuevos - Nada que guardar")
                return {'exito': False}
            
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
                    
                    # Calcular total esperado: horas previas + horas nuevas
                    try:
                        horas_previas_num = float(horas_previas) if horas_previas else 0
                    except:
                        horas_previas_num = 0
                    
                    horas_totales_esperadas = horas_previas_num + horas_esperadas
                    
                    print(f"📈 Hours_TC actual: '{total_horas}'")
                    print(f"📊 Cálculo: {horas_previas_num} (previas) + {horas_esperadas} (nuevas) = {horas_totales_esperadas} esperadas")
                    
                    # Comparar con las horas esperadas totales
                    if total_horas == str(int(horas_totales_esperadas)) or total_horas == f"{horas_totales_esperadas}":
                        print(f"🎉 ¡VERIFICACIÓN EXITOSA! Hours_TC = {horas_totales_esperadas}")
                        print(f"✅ CONFIRMADO: {dias_completados} días cargados + {dias_saltados_feriado} feriados = Correcto")
                        verificacion_automatica = True
                    else:
                        print(f"⚠️ VERIFICACIÓN FALLÓ: Hours_TC = '{total_horas}' (esperado: {horas_totales_esperadas})")
                        verificacion_automatica = False
                        
                except Exception as e:
                    print(f"❌ Error verificando Hours_TC: {e}")
                    verificacion_automatica = False
                
                # Verificación manual mejorada con datos automáticos
                print("\n" + "="*60)
                print("🔍 REVISIÓN MANUAL - ANTI-SUNDAY ✅")
                print("="*60)
                
                if verificacion_automatica:
                    print(f"✅ VERIFICACIÓN AUTOMÁTICA: Hours_TC = {horas_totales_esperadas} ✅")
                    print(f"✓ Los {dias_completados} días laborables se cargaron correctamente")
                    if dias_saltados_feriado > 0:
                        print(f"🏖️ {dias_saltados_feriado} día(s) feriado(s) fueron saltados correctamente")
                        print(f"   Feriados: {', '.join(dias_saltados_nombres)}")
                    print(f"✓ Total: {horas_previas_num} horas previas + {horas_esperadas} nuevas = {horas_totales_esperadas} horas")
                    print("🚫 CONFIRMADO: Sunday NO fue tocado")
                    print("\n🏆 ¡ÉXITO TOTAL! Carga completada correctamente.")
                    
                    # Retornar datos para el email
                    return {
                        'exito': True,
                        'dias_cargados': dias_completados,
                        'feriados_saltados': dias_saltados_feriado,
                        'feriados_nombres': dias_saltados_nombres,
                        'horas_previas': horas_previas_num,
                        'horas_nuevas': horas_esperadas,
                        'horas_totales': horas_totales_esperadas,
                        'url_navegador': self.driver.current_url if self.driver else self.url
                    }
                        
                else:
                    print(f"❌ VERIFICACIÓN AUTOMÁTICA FALLÓ: Hours_TC ≠ {horas_totales_esperadas}")
                    print(f"📊 Días laborables cargados: {dias_completados}")
                    print(f"🏖️ Feriados saltados: {dias_saltados_feriado}")
                    print("🔍 Problemas posibles:")
                    print("   • Las entradas no se confirman correctamente")
                    print("   • Algún día laborable no se persistió")
                    print("   • Falta algún paso de validación")
                    print(f"\n❌ Proceso marcado como fallido. Hours_TC = '{total_horas}' ≠ {horas_totales_esperadas}")
                    return {'exito': False}
                
            except Exception as e:
                print(f"💥 Error guardando: {e}")
                return {'exito': False}
            
        except Exception as e:
            print(f"💥 Error general: {e}")
            return {'exito': False}
            
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
    
    def enviar_notificacion_outlook(self, email, dias_cargados, feriados_saltados, feriados_nombres, horas_previas, horas_nuevas, horas_totales, url_navegador=None):
        """Envía correo de confirmación con detalles de la carga - Diseño EPAM-NEORIS"""
        try:
            # Construir resumen
            if feriados_saltados > 0:
                resumen_feriados = f"\n   🏖️ Feriados: {', '.join(feriados_nombres)}"
            else:
                resumen_feriados = ""
            
            # Usar la URL pasada o la URL por defecto
            if not url_navegador:
                url_navegador = self.url
            
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
            cc_email = self.email_cc  # Usar CC desde configuración
            
            mailto_link = f"mailto:{email}?cc={cc_email}&subject={subject_encoded}&body={body_encoded}"
            
            os.startfile(mailto_link)
            print("✓ Outlook abierto con el correo")
            print("💡 Revisá el contenido y presioná Ctrl+Enter para enviar")
            
            time.sleep(5)  # Más tiempo para que Outlook cargue
            print("\n📧 Intentando enviar automáticamente...")
            
            # Intentar enviar con atajo de teclado
            try:
                keyboard.press_and_release('ctrl+enter')
                time.sleep(2)
                print("✓ Comando de envío ejecutado")
                print("⚠️ Si el correo no se envió, presioná manualmente Ctrl+Enter")
            except Exception as e:
                print(f"⚠️ No se pudo enviar automáticamente: {e}")
                print("💡 Por favor, presioná Ctrl+Enter manualmente para enviar")
            
            return True
            
        except Exception as e:
            print(f"✗ Error enviando correo: {e}")
            return False
    
    def mostrar_popup_confirmacion(self, url_timecard):
        """Muestra popup con confirmación y botón para ir al timecard - Diseño EPAM-NEORIS ELÉCTRICO"""
        try:
            # Colores ELÉCTRICOS inspirados en la imagen
            COLOR_FONDO = "#0A1628"           # Azul muy oscuro
            COLOR_AZUL_ELECTRICO = "#00D4FF"  # Azul eléctrico brillante
            COLOR_AZUL_MEDIO = "#0099FF"      # Azul medio vibrante
            COLOR_NARANJA = "#FF8C00"         # Naranja brillante
            COLOR_NARANJA_CLARO = "#FFA500"   # Naranja claro
            COLOR_TEXTO_CLARO = "#FFFFFF"     # Blanco
            COLOR_TEXTO_GRIS = "#A0B0C0"      # Gris azulado
            
            # Crear ventana principal
            ventana = tk.Tk()
            ventana.title("EPAM-NEORIS | TimeCard")
            ventana.geometry("600x350")
            ventana.resizable(False, False)
            ventana.configure(bg=COLOR_FONDO)
            
            # Configurar para que aparezca al frente
            ventana.attributes('-topmost', True)
            ventana.focus_force()
            
            # Canvas para fondo con efectos eléctricos
            canvas = tk.Canvas(ventana, width=600, height=350, bg=COLOR_FONDO, highlightthickness=0)
            canvas.pack(fill='both', expand=True)
            
            # Crear efecto de fondo eléctrico con círculos y líneas
            # Círculos concéntricos en la esquina inferior izquierda (estilo rueda dentada)
            for i in range(6, 0, -1):
                radio = i * 25
                color_circulo = COLOR_AZUL_MEDIO if i % 2 == 0 else COLOR_AZUL_ELECTRICO
                canvas.create_oval(
                    -radio, 350 - radio,
                    radio, 350 + radio,
                    outline=color_circulo, width=2, fill=""
                )
            
            # Partículas naranjas flotantes (estilo datos/transmisión)
            for i in range(15):
                x = 400 + (i * 12) + (i % 3 * 5)
                y = 50 + (i * 15) - (i % 2 * 10)
                size = 3 + (i % 3)
                canvas.create_oval(
                    x - size, y - size,
                    x + size, y + size,
                    fill=COLOR_NARANJA, outline=""
                )
            
            # Líneas tech decorativas
            canvas.create_line(450, 80, 550, 80, fill=COLOR_NARANJA_CLARO, width=2)
            canvas.create_line(480, 100, 540, 100, fill=COLOR_NARANJA, width=1)
            
            # Hexágonos sutiles en el fondo
            for i in range(0, 700, 70):
                for j in range(0, 400, 60):
                    offset = 35 if (j // 60) % 2 else 0
                    canvas.create_polygon(
                        i + offset, j + 15,
                        i + offset + 15, j,
                        i + offset + 45, j,
                        i + offset + 60, j + 15,
                        i + offset + 45, j + 30,
                        i + offset + 15, j + 30,
                        fill="", outline="#1E2D3D", width=1
                    )
            
            # Frame principal sobre el canvas con fondo semitransparente
            frame = tk.Frame(canvas, bg=COLOR_FONDO, padx=30, pady=25)
            canvas.create_window(300, 175, window=frame)
            
            # Header con logos
            header_frame = tk.Frame(frame, bg=COLOR_FONDO)
            header_frame.pack(pady=(0, 15))
            
            # Logo EPAM con tipografía monoespaciada (MÁS GRANDE)
            logo_epam = tk.Label(
                header_frame,
                text="<epam>",
                font=("Courier New", 16, "bold"),
                fg=COLOR_TEXTO_CLARO,
                bg=COLOR_FONDO
            )
            logo_epam.pack()
            
            # Logo NEORIS con tipografía espaciada (MÁS GRANDE)
            logo_neoris = tk.Label(
                header_frame,
                text="N E O R I S",
                font=("Arial", 13, "normal"),
                fg=COLOR_TEXTO_CLARO,
                bg=COLOR_FONDO
            )
            logo_neoris.pack(pady=(3, 0))
            
            # Línea decorativa azul eléctrico
            linea = tk.Frame(frame, bg=COLOR_AZUL_ELECTRICO, height=3)
            linea.pack(fill='x', pady=(0, 20))
            
            # Título principal
            titulo = tk.Label(
                frame,
                text="✓ Carga Completada Exitosamente",
                font=("Segoe UI", 18, "bold"),
                fg=COLOR_AZUL_ELECTRICO,
                bg=COLOR_FONDO
            )
            titulo.pack(pady=(0, 15))
            
            # Mensaje principal
            mensaje = tk.Label(
                frame,
                text="Las horas semanales han sido cargadas correctamente.\nAhora puedes proceder a submitear en el TimeCard.",
                font=("Segoe UI", 11),
                fg=COLOR_TEXTO_CLARO,
                bg=COLOR_FONDO,
                justify="center"
            )
            mensaje.pack(pady=(0, 25))
            
            # Frame para botones
            frame_botones = tk.Frame(frame, bg=COLOR_FONDO)
            frame_botones.pack(pady=10)
            
            # Función para abrir el timecard
            def abrir_timecard():
                try:
                    webbrowser.open(url_timecard)
                    ventana.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo abrir el navegador: {e}")
            
            # Botón principal - Ir al Timecard (azul eléctrico, MÁS PEQUEÑO)
            btn_ir = tk.Button(
                frame_botones,
                text="→ Ir al TimeCard",
                font=("Segoe UI", 10, "bold"),
                bg=COLOR_AZUL_ELECTRICO,
                fg=COLOR_FONDO,
                activebackground=COLOR_AZUL_MEDIO,
                activeforeground=COLOR_FONDO,
                relief="flat",
                padx=25,
                pady=10,
                cursor="hand2",
                command=abrir_timecard,
                borderwidth=0
            )
            btn_ir.pack(side="left", padx=8)
            
            # Efecto hover para botón principal
            def on_enter_ir(e):
                btn_ir.config(bg="#34495E", fg=COLOR_TEXTO_CLARO)
            def on_leave_ir(e):
                btn_ir.config(bg=COLOR_AZUL_ELECTRICO, fg=COLOR_FONDO)
            btn_ir.bind("<Enter>", on_enter_ir)
            btn_ir.bind("<Leave>", on_leave_ir)
            
            # Botón secundario - Cerrar (EN NEGRITA)
            btn_cerrar = tk.Button(
                frame_botones,
                text="Cerrar",
                font=("Segoe UI", 10, "bold"),
                bg=COLOR_FONDO,
                fg=COLOR_TEXTO_GRIS,
                activebackground="#34495E",
                activeforeground=COLOR_TEXTO_CLARO,
                relief="flat",
                padx=25,
                pady=10,
                cursor="hand2",
                command=ventana.destroy,
                borderwidth=1,
                highlightbackground=COLOR_TEXTO_GRIS,
                highlightthickness=1
            )
            btn_cerrar.pack(side="left", padx=8)
            
            # Efecto hover para botón cerrar
            def on_enter_cerrar(e):
                btn_cerrar.config(bg="#34495E", fg=COLOR_TEXTO_CLARO)
            def on_leave_cerrar(e):
                btn_cerrar.config(bg=COLOR_FONDO, fg=COLOR_TEXTO_GRIS)
            btn_cerrar.bind("<Enter>", on_enter_cerrar)
            btn_cerrar.bind("<Leave>", on_leave_cerrar)
            
            # Footer con recordatorio
            footer_frame = tk.Frame(frame, bg=COLOR_FONDO)
            footer_frame.pack(pady=(20, 0))
            
            nota = tk.Label(
                footer_frame,
                text="💡 Recordá submitear las horas antes del viernes",
                font=("Segoe UI", 9),
                fg=COLOR_TEXTO_GRIS,
                bg=COLOR_FONDO
            )
            nota.pack()
            
            # Centrar ventana en la pantalla
            ventana.update_idletasks()
            x = (ventana.winfo_screenwidth() // 2) - (ventana.winfo_width() // 2)
            y = (ventana.winfo_screenheight() // 2) - (ventana.winfo_height() // 2)
            ventana.geometry(f"+{x}+{y}")
            
            # Iniciar loop
            ventana.mainloop()
            
        except Exception as e:
            print(f"⚠️ Error mostrando popup: {e}")
    
    def ejecutar(self, email):
        """Ejecuta la estrategia simple completa"""
        print("🚀 Iniciando CargaHorasSimple V5.2 - ANTI SUNDAY + DETECCIÓN FERIADOS + LOGGING")
        print("💡 GARANTIZA: Solo Monday-Friday (NO Sunday/Saturday)")
        print("🏖️ DETECTA: Feriados automáticamente (no carga si ya están aprobados)")
        print("✅ NO cerrará tus pestañas de Chrome existentes")
        print("🚫 NUNCA tocará Sunday ni Saturday")
        print("="*70)
        
        self.logger.info(f"Iniciando proceso de carga para: {email}")
        inicio_tiempo = time.time()
        
        try:
            # Verificar que el navegador se inicie correctamente
            navegador_ok = self.iniciar_navegador()
            if not navegador_ok:
                print("💥 ERROR: No se pudo iniciar el navegador")
                self.logger.error("Fallo al iniciar navegador - proceso abortado")
                return
            
            resultado = self.cargar_horas_estrategia_simple()
            
            # Cerrar navegador automáticamente
            print("\n🔒 Cerrando navegador del agente automáticamente...")
            if hasattr(self, 'driver') and self.driver:
                try:
                    self.driver.quit()
                    print("✅ Navegador cerrado")
                except Exception as e:
                    print(f"⚠️ Navegador ya cerrado o error: {e}")
            
            # Enviar correo automáticamente si la carga fue exitosa
            if resultado.get('exito', False):
                print("\n📧 Enviando correo de confirmación automáticamente...")
                self.logger.info("Carga exitosa - Enviando email de confirmación")
                self.logger.info(f"Resumen: {resultado['dias_cargados']} días cargados, {resultado['feriados_saltados']} feriados saltados")
                self.logger.info(f"Horas: {resultado['horas_previas']}h previas + {resultado['horas_nuevas']}h nuevas = {resultado['horas_totales']}h totales")
                self.enviar_notificacion_outlook(
                    email,
                    resultado['dias_cargados'],
                    resultado['feriados_saltados'],
                    resultado['feriados_nombres'],
                    resultado['horas_previas'],
                    resultado['horas_nuevas'],
                    resultado['horas_totales'],
                    resultado.get('url_navegador', self.url)
                )
                
                # Mostrar popup de confirmación
                url_timecard = resultado.get('url_navegador', self.url)
                print("\n🔔 Mostrando popup de confirmación...")
                self.logger.info("Mostrando popup de confirmación al usuario")
                self.mostrar_popup_confirmacion(url_timecard)
            else:
                print("❌ No se enviará correo debido a problemas persistentes")
                self.logger.error("Carga fallida - No se enviará correo")
            
            # Log de tiempo de ejecución
            tiempo_total = time.time() - inicio_tiempo
            minutos = int(tiempo_total // 60)
            segundos = int(tiempo_total % 60)
            self.logger.info(f"Tiempo de ejecución: {minutos}m {segundos}s")
            self.logger.info("="*70)
            self.logger.info("Proceso completado")
            self.logger.info("="*70)
                
            print("\n✅ Proceso completado")
            print(f"📄 Log guardado en: {self.log_file}")
            
        except Exception as e:
            print(f"💥 Error en ejecución: {e}")
            self.logger.error(f"Error crítico en ejecución: {e}", exc_info=True)
            # Intentar cerrar navegador incluso si hay error
            try:
                if hasattr(self, 'driver') and self.driver:
                    print("🔒 Cerrando navegador...")
                    self.driver.quit()
                    self.logger.info("Navegador cerrado después de error")
            except Exception as close_error:
                self.logger.error(f"Error cerrando navegador: {close_error}")
            
            # Log de finalización con error
            tiempo_total = time.time() - inicio_tiempo
            self.logger.info(f"Proceso finalizado con errores - Tiempo: {int(tiempo_total)}s")
            self.logger.info("="*70)
                
            print("\n❌ Proceso completado con errores")
            print(f"📄 Log guardado en: {self.log_file}")

# Configuración
if __name__ == "__main__":
    # Cargar email desde variable de entorno (más seguro y configurable)
    email_destinatario = os.getenv('EMAIL_DESTINATARIO', 'laura_aristegui@epamneoris.com')
    
    print("="*70)
    print("📧 Email destinatario:", email_destinatario)
    print("💡 Para cambiar, edita el archivo .env")
    print("="*70)
    
    agente = CargaHorasSimple()
    agente.ejecutar(email_destinatario)