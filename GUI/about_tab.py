import customtkinter as ctk
from PIL import Image
import webbrowser
import os
import tkinter as tk

class AboutTab:
    def __init__(self, parent):
        self.parent = parent

        # ----------------- Función para animar separadores -----------------
        def add_hover_animation(frame, color_normal, color_hover):
            def on_enter(e):
                frame.configure(fg_color=color_hover)
            def on_leave(e):
                frame.configure(fg_color=color_normal)
            frame.bind("<Enter>", on_enter)
            frame.bind("<Leave>", on_leave)

        # Frame principal limpio y centrado
        self.main_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # ----------------- Título principal -----------------
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="PS2 GAME DOWNLOADER",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#4B8BBE"
        )
        self.title_label.pack(pady=(20,10))

        # ----------------- Separador decorativo superior -----------------
        self.separator_top = ctk.CTkFrame(self.main_frame, height=2, fg_color="#306998")
        self.separator_top.pack(fill="x", padx=50, pady=(0,20))
        add_hover_animation(self.separator_top, "#306998", "#4B8BBE")

        # ----------------- Descripción larga -----------------
        descripcion_texto = (
            "PS2 Game Downloader es una aplicación completa diseñada para los amantes de "
            "la PlayStation 2. Con esta herramienta, puedes descargar tus juegos favoritos "
            "de manera rápida y sencilla, manteniendo todo organizado y accesible.\n\n"
            "Además de la descarga de juegos, la aplicación te permite gestionar tus unidades "
            "USB de manera eficiente, asegurando que estén preparadas correctamente para ser "
            "utilizadas con tu consola PS2 a través de OPL (Open PS2 Loader). Puedes crear las "
            "carpetas necesarias automáticamente, verificar el espacio disponible y conocer el "
            "formato del dispositivo.\n\n"
            "Con una interfaz moderna y fácil de usar basada en CustomTkinter, PS2 Game Downloader "
            "ofrece un flujo de trabajo intuitivo: filtra y busca juegos rápidamente, inicia descargas "
            "con control de pausa y cancelación, y observa la velocidad y el progreso de cada descarga "
            "en tiempo real. Todo pensado para que tu experiencia sea eficiente y agradable."
        )
        self.descripcion_label = ctk.CTkLabel(
            self.main_frame,
            text=descripcion_texto,
            wraplength=600,
            justify="center",
            font=ctk.CTkFont(size=16),
            text_color="#CCCCCC"
        )
        self.descripcion_label.pack(pady=(0,20))

        # ----------------- Separador decorativo inferior -----------------
        self.separator_bottom = ctk.CTkFrame(self.main_frame, height=2, fg_color="#4B8BBE")
        self.separator_bottom.pack(fill="x", padx=50, pady=(0,20))
        add_hover_animation(self.separator_bottom, "#4B8BBE", "#306998")

        # ----------------- Frame de botones con fondo más oscuro -----------------
        self.botones_frame = ctk.CTkFrame(self.main_frame, fg_color="#333333", corner_radius=10)
        self.botones_frame.pack(pady=10, padx=50, fill="x")

        # ----------------- Texto encima de los botones -----------------
        self.botones_label = ctk.CTkLabel(
            self.botones_frame,
            text="REDES E INFORMACIÓN",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#4B8BBE"
        )
        self.botones_label.pack(pady=(10,20))

        # Función para abrir enlaces
        def abrir_url(url):
            webbrowser.open(url)

        # ----------------- Contenedor de botones -----------------
        botones_contenedor = ctk.CTkFrame(self.botones_frame, fg_color="transparent")
        botones_contenedor.pack(pady=(0,10))

        # Ruta de los iconos en la carpeta Images
        ruta_actual = os.path.dirname(__file__)
        github_icon = ctk.CTkImage(Image.open(os.path.join(ruta_actual, "Images/github.png")), size=(24,24))
        facebook_icon = ctk.CTkImage(Image.open(os.path.join(ruta_actual, "Images/facebook.png")), size=(24,24))
        web_icon = ctk.CTkImage(Image.open(os.path.join(ruta_actual, "Images/web.png")), size=(24,24))

        # ----------------- Botones con icono a la izquierda -----------------
        self.github_button = ctk.CTkButton(
            botones_contenedor, text="GitHub", image=github_icon, compound="left", width=140,
            command=lambda: abrir_url("https://github.com/tu_usuario")
        )
        self.github_button.pack(side="left", padx=10)

        self.facebook_button = ctk.CTkButton(
            botones_contenedor, text="Facebook", image=facebook_icon, compound="left", width=140,
            command=lambda: abrir_url("https://facebook.com/tu_usuario")
        )
        self.facebook_button.pack(side="left", padx=10)

        self.web_button = ctk.CTkButton(
            botones_contenedor, text="Mi Web", image=web_icon, compound="left", width=140,
            command=lambda: abrir_url("https://tuweb.com")
        )
        self.web_button.pack(side="left", padx=10)

        # ----------------- Información de derechos con efecto oro animado -----------------
        canvas_width = 600
        canvas_height = 40
        bg_color = "#1C1C1C"  # Ajusta según el fondo de tu app
        self.canvas_derechos = tk.Canvas(
            self.main_frame, width=canvas_width, height=canvas_height, bg=bg_color, highlightthickness=0
        )
        self.canvas_derechos.pack(pady=20)

        texto = "2025 © BLUENXTEAM"
        font_derechos = ("Helvetica", 16, "bold")
        colores = ["#FFD700", "#FFC200", "#FFB000", "#FFA000", "#FF8C00"]

        espacio_letra = 16
        ancho_total = len(texto) * espacio_letra
        x_start = (canvas_width - ancho_total) / 2

        # Dibujar letras y guardar IDs para animación
        self.letras_ids = []
        for i, letra in enumerate(texto):
            color = colores[i % len(colores)]
            letra_id = self.canvas_derechos.create_text(
                x_start + i * espacio_letra,
                canvas_height/2,
                text=letra,
                font=font_derechos,
                fill=color,
                anchor="w"
            )
            self.letras_ids.append(letra_id)

        # ----------------- Animación de brillo -----------------
        self.animacion_offset = 0

        def animar():
            for i, letra_id in enumerate(self.letras_ids):
                # Cálculo de color dinámico para efecto brillo
                index = (i + self.animacion_offset) % len(colores)
                self.canvas_derechos.itemconfig(letra_id, fill=colores[index])
            self.animacion_offset = (self.animacion_offset + 1) % len(colores)
            self.canvas_derechos.after(150, animar)  # velocidad del brillo

        animar()
