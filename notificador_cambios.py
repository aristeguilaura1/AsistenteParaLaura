"""
notificador_cambios.py - Notifica a Matías sobre cambios en el repositorio
"""

import os
import subprocess
import time

def obtener_ultimo_commit():
    """Obtiene información del último commit"""
    try:
        # Get latest commit hash
        commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()
        # Get latest commit message
        commit_msg = subprocess.check_output(['git', 'log', '-1', '--pretty=%B']).decode().strip()
        # Get latest commit author
        commit_author = subprocess.check_output(['git', 'log', '-1', '--pretty=%an']).decode().strip()
        
        return {
            'hash': commit_hash,
            'mensaje': commit_msg,
            'autor': commit_author
        }
    except Exception as e:
        print(f"Error obteniendo info del commit: {e}")
        return None

def obtener_archivos_modificados():
    """Obtiene lista de archivos modificados en el último commit"""
    try:
        archivos = subprocess.check_output(['git', 'log', '-1', '--name-status']).decode().strip().split('\n')[1:]
        return [f.strip() for f in archivos if f.strip()]
    except Exception as e:
        print(f"Error obteniendo archivos modificados: {e}")
        return []

def enviar_notificacion_matias(commit_info, archivos):
    """Envía mail de notificación a Matías sobre cambios"""
    import keyboard
    
    try:
        # Construcción del email
        asunto = f"AsistenteParaLaura: Nuevo commit ({commit_info['hash']})"
        
        archivos_lista = "\n".join([f"  • {arch}" for arch in archivos])
        
        cuerpo = f"""Hola Matías,

Se ha realizado un nuevo commit en el repositorio AsistenteParaLaura:

📝 Detalles del commit:
Commit: {commit_info['hash']}
Autor: {commit_info['autor']}
Mensaje: {commit_info['mensaje']}

📄 Archivos modificados:
{archivos_lista}

🔗 Repositorio: https://github.com/aristeguilaura1/AsistenteParaLaura

Saludos,
AsistenteParaLaura"""
        
        subject_encoded = asunto.replace(' ', '%20')
        body_encoded = cuerpo.replace('\n', '%0D%0A').replace(' ', '%20')
        email = 'matias_munoz@epamneoris.com'
        mailto_link = f'mailto:{email}?subject={subject_encoded}&body={body_encoded}'
        
        print("📧 Abriendo Outlook con notificación de cambios...")
        os.startfile(mailto_link)
        time.sleep(3)
        
        # Enviar automáticamente
        keyboard.press_and_release('ctrl+enter')
        time.sleep(1)
        
        print(f"✅ Notificación enviada a Matías")
        return True
        
    except Exception as e:
        print(f"❌ Error enviando notificación: {e}")
        return False

def notificar_cambios():
    """Función principal: notifica cambios a Matías"""
    print("🔔 Verificando cambios para notificar...")
    
    commit_info = obtener_ultimo_commit()
    if not commit_info:
        print("❌ No se pudo obtener información del commit")
        return False
    
    archivos = obtener_archivos_modificados()
    if not archivos:
        print("⚠️ No se encontraron archivos modificados")
        return False
    
    print(f"📝 Commit: {commit_info['mensaje']}")
    print(f"📄 Archivos modificados: {len(archivos)}")
    
    return enviar_notificacion_matias(commit_info, archivos)

if __name__ == "__main__":
    notificar_cambios()
