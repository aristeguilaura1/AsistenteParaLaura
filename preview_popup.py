"""
Script de preview para ver el diseño del popup sin ejecutar la carga completa
"""
import tkinter as tk
from tkinter import messagebox
import webbrowser
import math

def mostrar_popup_preview():
    """Muestra el popup con el nuevo diseño EPAM-NEORIS - COLORES ELÉCTRICOS"""
    # Colores ELÉCTRICOS inspirados en la imagen
    COLOR_FONDO = "#0A1628"           # Azul muy oscuro
    COLOR_AZUL_ELECTRICO = "#00D4FF"  # Azul eléctrico brillante
    COLOR_AZUL_MEDIO = "#0099FF"      # Azul medio vibrante
    COLOR_NARANJA = "#FF8C00"         # Naranja brillante
    COLOR_NARANJA_CLARO = "#FFA500"   # Naranja claro
    COLOR_TEXTO_CLARO = "#FFFFFF"     # Blanco
    COLOR_TEXTO_GRIS = "#A0B0C0"      # Gris azulado
    
    # URL de ejemplo
    url_timecard = "https://hc.neoris.net/timecard/"
    
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

if __name__ == "__main__":
    print("🎨 Mostrando preview del popup con diseño EPAM-NEORIS...")
    mostrar_popup_preview()
