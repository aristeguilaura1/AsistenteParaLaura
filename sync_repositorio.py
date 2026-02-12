"""
sync_repositorio.py - Sincroniza cambios y notifica a Matías
Uso: python sync_repositorio.py "mensaje del commit"
"""

import sys
import subprocess
import os

def sync_y_notificar(mensaje_commit=None):
    """Realiza push y notifica cambios a Matías"""
    
    try:
        # Verificar si hay cambios
        print("🔍 Verificando cambios...")
        status = subprocess.check_output(['git', 'status', '--porcelain']).decode().strip()
        
        if not status:
            print("✅ No hay cambios pendientes")
            return True
        
        print(f"📝 Cambios encontrados:\n{status}\n")
        
        # Stage de cambios
        print("📦 Preparando cambios...")
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Si no hay mensaje, pedir uno
        if not mensaje_commit:
            mensaje_commit = input("📝 Ingresa mensaje del commit: ").strip()
            if not mensaje_commit:
                print("❌ Mensaje de commit requerido")
                return False
        
        # Commit
        print(f"💾 Haciendo commit: {mensaje_commit}")
        subprocess.run(['git', 'commit', '-m', mensaje_commit], check=True)
        
        # Push
        print("🚀 Subiendo a repositorio...")
        subprocess.run(['git', 'push'], check=True)
        print("✅ Push exitoso")
        
        # Notificar a Matías
        print("\n📧 Notificando a Matías...")
        resultado_notificacion = subprocess.run(
            ['python', 'notificador_cambios.py'],
            capture_output=False
        )
        
        if resultado_notificacion.returncode == 0:
            print("\n🎉 Cambios sincronizados y notificación enviada")
            return True
        else:
            print("\n⚠️ Cambios sincronizados pero fallo en notificación")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en git: {e}")
        return False
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False

if __name__ == "__main__":
    # Obtener mensaje del commit de argumentos
    mensaje = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    
    exito = sync_y_notificar(mensaje)
    sys.exit(0 if exito else 1)
