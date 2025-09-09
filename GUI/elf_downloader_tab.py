import customtkinter as ctk
import platform
import urllib.request
from urllib.error import URLError, HTTPError
import threading
import os
from tkinter import filedialog
from PIL import Image
import time

class ElfDownloaderTab:
    def __init__(self, parent):
        self.parent = parent
        self.selected_frame = None
        self.elfs_data = []
        self.ruta_descarga = os.path.expanduser("~/Descargas/ELFs")

        # ----------------- Título -----------------
        self.label = ctk.CTkLabel(
            parent,
            text="ELF Downloader",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#4B8BBE"
        )
        self.label.pack(pady=20)

        # ----------------- Separador -----------------
        self.separator = ctk.CTkFrame(parent, height=2, fg_color="#4B8BBE")
        self.separator.pack(fill="x", padx=50, pady=(0,20))

        # ----------------- Scrollable Frame -----------------
        self.scroll_frame = ctk.CTkScrollableFrame(parent)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self._enable_mousewheel(self.scroll_frame)

        # ----------------- Botón centrado debajo del scrollframe -----------------
        folder_image_path = os.path.join(os.path.dirname(__file__), "Images", "folder.png")
        folder_image_pil = Image.open(folder_image_path)
        folder_image = ctk.CTkImage(folder_image_pil, size=(24,24))

        self.bottom_button = ctk.CTkButton(
            parent,
            text="CARPETA DE DESCARGA",
            image=folder_image,
            compound="left",
            width=220,
            fg_color="#4CAF50",
            hover_color="#45A049",
            command=self.seleccionar_carpeta_descarga
        )
        self.bottom_button.pack(pady=20)

        # ----------------- Cargar ELF desde GitHub -----------------
        threading.Thread(target=self.cargar_elfs, daemon=True).start()

    # ----------------- Seleccionar carpeta de descarga -----------------
    def seleccionar_carpeta_descarga(self):
        nueva_ruta = filedialog.askdirectory(title="Selecciona carpeta de descarga ELF", initialdir=self.ruta_descarga)
        if nueva_ruta:
            self.ruta_descarga = nueva_ruta
            print(f"Carpeta de descarga seleccionada: {self.ruta_descarga}")

    # ----------------- Cargar ELF desde elf.ini -----------------
    def cargar_elfs(self):
        url = "https://raw.githubusercontent.com/BlueNX-Team/ps2-game-downloader/refs/heads/main/elf.ini"
        try:
            with urllib.request.urlopen(url) as response:
                data = response.read().decode("utf-8")

            self.elfs_data = []
            in_section = False
            for line in data.splitlines():
                line = line.strip()
                if not line:
                    continue
                if line.startswith("[") and line.endswith("]"):
                    in_section = line[1:-1] == "Elf"
                    continue
                if in_section and "=" in line:
                    parts = line.split(";")
                    nombre_url = parts[0].split("=", 1)
                    if len(nombre_url) < 2:
                        nombre = nombre_url[0].strip()
                        url_part = ""
                    else:
                        nombre = nombre_url[0].strip()
                        url_part = nombre_url[1].replace("url=", "").strip()
                    version = "Desconocida"
                    for p in parts[1:]:
                        if p.startswith("Version="):
                            version = p.replace("Version=", "").strip()
                    self.elfs_data.append({"nombre": nombre, "version": version, "url": url_part})

            self.mostrar_tarjetas(self.elfs_data)

        except Exception as e:
            ctk.CTkLabel(self.scroll_frame, text=f"Error cargando ELF: {e}").pack(pady=5, padx=10)

    # ----------------- Mostrar tarjetas con dot de estado -----------------
    def mostrar_tarjetas(self, elfs):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        for elf in elfs:
            frame = ctk.CTkFrame(self.scroll_frame, corner_radius=10, fg_color="#333333")
            frame.pack(fill="x", pady=8, padx=10)

            container = ctk.CTkFrame(frame, fg_color="transparent")
            container.pack(fill="x", pady=5, padx=5)

            # Dot de estado (rojo inicialmente)
            dot = ctk.CTkFrame(container, width=20, height=20, corner_radius=10, fg_color="red")
            dot.pack(side="left", padx=(5,10))
            dot.pack_propagate(False)

            # Verificar link en hilo separado
            threading.Thread(target=self.verificar_link, args=(elf["url"], dot), daemon=True).start()

            # Contenedor para nombre + versión en línea
            nombre_frame = ctk.CTkFrame(container, fg_color="transparent")
            nombre_frame.pack(side="left", fill="x", expand=True, anchor="w")

            # Nombre del ELF
            nombre_label = ctk.CTkLabel(
                nombre_frame,
                text=elf['nombre'],
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#FFFFFF"
            )
            nombre_label.pack(side="left", anchor="w")

            # Versión al lado derecho del nombre, color azul claro
            version_label = ctk.CTkLabel(
                nombre_frame,
                text=f"v{elf['version']}",
                font=ctk.CTkFont(size=12),
                text_color="#4FC3F7"  # Azul claro
            )
            version_label.pack(side="left", padx=(10,0), anchor="w")

            # Contenedor botón y progress
            botones_frame = ctk.CTkFrame(container, fg_color="transparent")
            botones_frame.pack(side="right", padx=5)

            # ProgressBar
            progress_bar = ctk.CTkProgressBar(botones_frame, width=120)
            progress_bar.set(0)
            progress_bar.pack(side="left", padx=(0,5), pady=5)

            # Botón Descargar
            descargar_btn = ctk.CTkButton(
                botones_frame,
                text="Descargar",
                width=90,
                fg_color="#4CAF50",
                hover_color="#45A049",
                command=lambda url=elf['url'], nombre=elf['nombre'], pb=progress_bar: threading.Thread(
                    target=self.descargar_elf, args=(url, nombre, pb), daemon=True
                ).start()
            )
            descargar_btn.pack(side="left", padx=5)

            # Bind hover y selección
            for widget in (frame, container, nombre_label, version_label):
                widget.bind("<Button-1>", lambda e, f=frame: self.seleccionar_tarjeta(f))
            frame.bind("<Enter>", lambda e, f=frame: f.configure(fg_color="#444444"))
            frame.bind("<Leave>", lambda e, f=frame: f.configure(fg_color="#555555" if f == self.selected_frame else "#333333"))

    # ----------------- Verificar link y actualizar dot -----------------
    def verificar_link(self, url, dot):
        try:
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=5):
                dot.after(0, lambda: dot.configure(fg_color="green"))
        except:
            dot.after(0, lambda: dot.configure(fg_color="red"))

    # ----------------- Selección -----------------
    def seleccionar_tarjeta(self, frame):
        if self.selected_frame:
            self.selected_frame.configure(fg_color="#333333")
        frame.configure(fg_color="#555555")
        self.selected_frame = frame

    # ----------------- Scroll -----------------
    def _enable_mousewheel(self, scrollframe: ctk.CTkScrollableFrame):
        sistema = platform.system()
        canvas = scrollframe._parent_canvas
        if sistema == "Windows":
            canvas.bind_all("<MouseWheel>", lambda e: self._on_mousewheel(e, canvas))
        else:
            canvas.bind_all("<Button-4>", lambda e: self._on_mousewheel_linux(-1, canvas))
            canvas.bind_all("<Button-5>", lambda e: self._on_mousewheel_linux(1, canvas))

    def _on_mousewheel(self, event, canvas):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_mousewheel_linux(self, direction, canvas):
        canvas.yview_scroll(direction, "units")

    # ----------------- Descargar ELF -----------------
    def descargar_elf(self, url, nombre, progress_bar):
        try:
            os.makedirs(self.ruta_descarga, exist_ok=True)
            ruta_archivo = os.path.join(self.ruta_descarga, f"{nombre}.ELF")

            with urllib.request.urlopen(url) as response, open(ruta_archivo, "wb") as out_file:
                total_size = int(response.getheader('Content-Length', 0))
                downloaded = 0
                chunk_size = 1024*1024

                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    out_file.write(chunk)
                    downloaded += len(chunk)

                    # Actualizar progressbar
                    if total_size > 0:
                        progress_bar.set(downloaded / total_size)

            print(f"Descarga completada: {ruta_archivo}")

        except Exception as e:
            print(f"Error descargando {nombre}: {e}")
