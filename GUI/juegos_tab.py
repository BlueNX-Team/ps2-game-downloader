import customtkinter as ctk
import platform
import urllib.request
from urllib.error import URLError, HTTPError
import threading
import os
import time
from PIL import Image
import tkinter as tk
from tkinter import filedialog
import io

class JuegosTab:
    def __init__(self, parent):
        self.parent = parent
        self.selected_game_frame = None
        self.juegos_data = []
        self.ruta_descarga = os.path.expanduser("~/Descargas/JuegosPS2")
        self.descarga_thread = None
        self.descarga_activa = False
        self.descarga_pausada = False
        self.descarga_cancelada = False
        self.ruta_archivo_actual = None

        # Título
        self.label = ctk.CTkLabel(parent, text="Gestión de Juegos", font=ctk.CTkFont(size=18, weight="bold"))
        self.label.pack(pady=10)

        # Frame principal
        self.main_frame = ctk.CTkFrame(parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # -------------------- Frame izquierdo --------------------
        self.left_frame = ctk.CTkFrame(self.main_frame)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=(0,10), pady=10)

        # Label para mostrar el icono del juego
        self.icon_label = ctk.CTkLabel(self.left_frame, text="No Icono")
        self.icon_label.pack(padx=10, pady=(0,10), fill="both", expand=True)

        # -------------------- Frames de información de descarga ABAJO DEL FRAME IZQUIERDO --------------------
        self.info_frame = ctk.CTkFrame(self.left_frame)
        self.info_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        # Tamaño y descargado
        self.tamano_frame = ctk.CTkFrame(self.info_frame)
        self.tamano_frame.pack(fill="x", pady=5)
        self.tamano_label = ctk.CTkLabel(self.tamano_frame, text="Tamaño: 0 MB | Descargado: 0 MB")
        self.tamano_label.pack(padx=10, pady=5, anchor="w")

        # Velocidad
        self.velocidad_frame = ctk.CTkFrame(self.info_frame)
        self.velocidad_frame.pack(fill="x", pady=5)
        self.velocidad_label = ctk.CTkLabel(self.velocidad_frame, text="Velocidad: 0 MB/s")
        self.velocidad_label.pack(padx=10, pady=5, anchor="w")

        # Tiempo estimado
        self.tiempo_frame = ctk.CTkFrame(self.info_frame)
        self.tiempo_frame.pack(fill="x", pady=5)
        self.tiempo_label = ctk.CTkLabel(self.tiempo_frame, text="Tiempo estimado: 0h 0m")
        self.tiempo_label.pack(padx=10, pady=5, anchor="w")

        # -------------------- Frame derecho --------------------
        self.right_container = ctk.CTkFrame(self.main_frame)
        self.right_container.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)

        # Frame superior derecho: búsqueda + botones
        self.search_frame = ctk.CTkFrame(self.right_container, height=50, fg_color="transparent")
        self.search_frame.pack(fill="x", pady=(0,10), padx=10)

        # Entry búsqueda
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Filtrar por nombre", textvariable=self.search_var, width=300)
        self.search_entry.pack(side="left", pady=10, padx=(0,10))
        self.search_var.trace_add("write", lambda *args: self.filtrar_juegos())

        # Selector de categoría
        self.categoria_var = ctk.StringVar(value="Todas")
        self.categoria_selector = ctk.CTkOptionMenu(
            self.search_frame,
            values=["Todas", "Accion", "Aventura", "Deportes", "Puzzle"],
            variable=self.categoria_var,
            command=lambda value: self.filtrar_juegos()
        )
        self.categoria_selector.pack(side="left", pady=10)

        # Botón carpeta
        ruta_icono = os.path.join(os.path.dirname(__file__), "Images", "folder.png")
        folder_image = ctk.CTkImage(Image.open(ruta_icono), size=(24,24))
        self.folder_button = ctk.CTkButton(
            self.search_frame,
            image=folder_image,
            text="",
            width=30, height=30,
            fg_color="#4B8BBE",
            hover_color="#306998",
            command=self.seleccionar_carpeta_descarga
        )
        self.folder_button.pack(side="left", padx=(10,0), pady=10)

        # Botón Descargar
        self.download_button = ctk.CTkButton(
            self.search_frame, text="Descargar", fg_color="#4CAF50", hover_color="#45A049", command=self.iniciar_descarga
        )
        self.download_button.pack(side="left", padx=(10,0), pady=10)

        # Botón Pausar/Reanudar
        self.pause_button = ctk.CTkButton(
            self.search_frame, text="Pausar", fg_color="#FFC107", hover_color="#FFB300", command=self.pausar_reanudar_descarga
        )
        self.pause_button.pack(side="left", padx=(10,0), pady=10)

        # Botón Cancelar
        self.cancel_button = ctk.CTkButton(
            self.search_frame, text="Cancelar", fg_color="#F44336", hover_color="#D32F2F", command=self.cancelar_descarga
        )
        self.cancel_button.pack(side="left", padx=(10,0), pady=10)

        # -------------------- Barra de progreso --------------------
        self.progress_bar = ctk.CTkProgressBar(self.right_container)
        self.progress_bar.pack(fill="x", padx=10, pady=(0,10))
        self.progress_bar.set(0)

        # Frame scrollable para tarjetas
        self.right_frame = ctk.CTkScrollableFrame(self.right_container)
        self.right_frame.pack(fill="both", expand=True, padx=10, pady=(0,10))

        # Cargar juegos y habilitar scroll
        self.cargar_juegos()
        self._enable_mousewheel(self.right_frame)

    # -------------------- Cargar juegos desde GitHub --------------------
    def cargar_juegos(self):
        url = "https://raw.githubusercontent.com/BlueNX-Team/ps2-game-downloader/refs/heads/main/juegos.ini"
        try:
            with urllib.request.urlopen(url) as response:
                data = response.read().decode("utf-8")

            self.juegos_data = []
            in_section = False
            for line in data.splitlines():
                line = line.strip()
                if not line:
                    continue
                if line.startswith("[") and line.endswith("]"):
                    in_section = line[1:-1] == "Juegos"
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
                    categoria = "Desconocida"
                    icono_url = ""
                    for p in parts[1:]:
                        if p.startswith("categoria="):
                            categoria = p.replace("categoria=", "").strip()
                        if p.startswith("icono="):
                            icono_url = p.replace("icono=", "").strip()
                    self.juegos_data.append({"nombre": nombre, "categoria": categoria, "url": url_part, "icono": icono_url})

            self.mostrar_tarjetas(self.juegos_data)

        except Exception as e:
            ctk.CTkLabel(self.right_frame, text=f"Error cargando juegos: {e}").pack(pady=5, padx=10)

    # -------------------- Mostrar tarjetas --------------------
    def mostrar_tarjetas(self, juegos_filtrados):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        for juego in juegos_filtrados:
            frame_juego = ctk.CTkFrame(self.right_frame, corner_radius=5, fg_color="#444444")
            frame_juego.pack(fill="x", pady=5, padx=10)

            container = ctk.CTkFrame(frame_juego, fg_color="transparent")
            container.pack(fill="x", pady=5, padx=5)

            indicador = ctk.CTkFrame(container, width=20, height=20, fg_color="gray", corner_radius=5)
            indicador.pack(side="left", padx=(0,10))
            indicador.pack_propagate(False)

            nombre_label = ctk.CTkLabel(container, text=juego["nombre"].replace("_"," "), font=ctk.CTkFont(size=14))
            nombre_label.pack(side="left", anchor="w")

            for widget in (frame_juego, container, indicador, nombre_label):
                widget.bind("<Button-1>", lambda e, f=frame_juego: self.seleccionar_tarjeta(f))

            threading.Thread(target=self.verificar_link, args=(juego["url"], indicador), daemon=True).start()

    # -------------------- Filtrar --------------------
    def filtrar_juegos(self):
        texto = self.search_var.get().lower()
        categoria = self.categoria_var.get()
        filtrados = []

        for juego in self.juegos_data:
            if texto in juego["nombre"].lower():
                if categoria == "Todas" or juego["categoria"] == categoria:
                    filtrados.append(juego)
        self.mostrar_tarjetas(filtrados)

    # -------------------- Selección --------------------
    def seleccionar_tarjeta(self, frame):
        if self.selected_game_frame:
            self.selected_game_frame.configure(fg_color="#444444")
        frame.configure(fg_color="#555555")
        self.selected_game_frame = frame

        # Actualizar el icono del juego seleccionado
        index = self.right_frame.winfo_children().index(frame)
        juego = self.juegos_data[index]

        if "icono" in juego and juego["icono"]:
            try:
                with urllib.request.urlopen(juego["icono"]) as response:
                    img_data = response.read()
                pil_image = Image.open(io.BytesIO(img_data))

                # Obtener ancho del left_frame y limitar altura
                ancho_frame = self.left_frame.winfo_width() - 20
                alto_frame = 200
                pil_image.thumbnail((ancho_frame, alto_frame), Image.LANCZOS)

                icono_ctk = ctk.CTkImage(pil_image, size=pil_image.size)
                self.icon_label.configure(image=icono_ctk, text="")
                self.icon_label.image = icono_ctk
            except Exception as e:
                print(f"No se pudo cargar el icono: {e}")
                self.icon_label.configure(image=None, text="No Icono")
        else:
            self.icon_label.configure(image=None, text="No Icono")

    # -------------------- Verificar link --------------------
    def verificar_link(self, url, indicador_frame):
        if not url:
            color = "red"
        else:
            try:
                req = urllib.request.Request(url, method="HEAD")
                with urllib.request.urlopen(req, timeout=5):
                    color = "green"
            except (HTTPError, URLError):
                color = "red"

        if indicador_frame.winfo_exists():
            indicador_frame.after(0, lambda: indicador_frame.configure(fg_color=color))

    # -------------------- Descarga --------------------
    def iniciar_descarga(self):
        if not self.selected_game_frame:
            print("Selecciona un juego primero")
            return

        index = self.right_frame.winfo_children().index(self.selected_game_frame)
        juego = self.juegos_data[index]

        if not juego["url"]:
            print("No hay URL para este juego")
            return

        if self.descarga_thread and self.descarga_thread.is_alive():
            print("Ya hay una descarga en curso")
            return

        self.descarga_activa = True
        self.descarga_pausada = False
        self.descarga_cancelada = False
        self.ruta_archivo_actual = os.path.join(self.ruta_descarga, f"{juego['nombre']}.iso")
        self.pause_button.configure(text="Pausar")
        self.progress_bar.set(0)
        self.tamano_label.configure(text="Tamaño: 0 MB | Descargado: 0 MB")
        self.velocidad_label.configure(text="Velocidad: 0 MB/s")
        self.tiempo_label.configure(text="Tiempo estimado: 0h 0m")
        self.descarga_thread = threading.Thread(target=self.descargar_juego, args=(juego["url"], juego["nombre"]), daemon=True)
        self.descarga_thread.start()

    def descargar_juego(self, url, nombre):
        try:
            os.makedirs(self.ruta_descarga, exist_ok=True)
            with urllib.request.urlopen(url) as response, open(self.ruta_archivo_actual, "wb") as out_file:
                total_size = int(response.getheader('Content-Length', 0))
                downloaded = 0
                chunk_size = 1024*1024
                start_time = time.time()

                while True:
                    if self.descarga_cancelada:
                        self.progress_bar.set(0)
                        self.tamano_label.configure(text="Tamaño: 0 MB | Descargado: 0 MB")
                        self.velocidad_label.configure(text="Velocidad: 0 MB/s")
                        self.tiempo_label.configure(text="Tiempo estimado: Cancelada")
                        if os.path.exists(self.ruta_archivo_actual):
                            os.remove(self.ruta_archivo_actual)
                        break
                    if self.descarga_pausada:
                        continue
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    out_file.write(chunk)
                    downloaded += len(chunk)

                    if total_size > 0:
                        self.progress_bar.set(downloaded/total_size)

                    mb_total = total_size / (1024**2)
                    mb_descargado = downloaded / (1024**2)
                    self.tamano_label.configure(text=f"Tamaño: {mb_total:.2f} MB | Descargado: {mb_descargado:.2f} MB")

                    tiempo_transcurrido = time.time() - start_time
                    velocidad = mb_descargado / tiempo_transcurrido if tiempo_transcurrido > 0 else 0
                    self.velocidad_label.configure(text=f"Velocidad: {velocidad:.2f} MB/s")

                    if velocidad > 0:
                        tiempo_restante = (mb_total - mb_descargado)/velocidad
                    else:
                        tiempo_restante = 0
                    horas = int(tiempo_restante // 3600)
                    minutos = int((tiempo_restante % 3600) // 60)
                    self.tiempo_label.configure(text=f"Tiempo estimado: {horas}h {minutos}m")

        except Exception as e:
            print(f"Error al descargar: {e}")
        finally:
            self.descarga_activa = False
            self.descarga_pausada = False
            self.descarga_cancelada = False
            self.ruta_archivo_actual = None

    def pausar_reanudar_descarga(self):
        if not self.descarga_activa:
            return
        self.descarga_pausada = not self.descarga_pausada
        self.pause_button.configure(text="Reanudar" if self.descarga_pausada else "Pausar")

    def cancelar_descarga(self):
        if not self.descarga_activa:
            return
        self.descarga_cancelada = True
        self.progress_bar.set(0)
        self.tamano_label.configure(text="Tamaño: 0 MB | Descargado: 0 MB")
        self.velocidad_label.configure(text="Velocidad: 0 MB/s")
        self.tiempo_label.configure(text="Tiempo estimado: Cancelada")
        if self.ruta_archivo_actual and os.path.exists(self.ruta_archivo_actual):
            os.remove(self.ruta_archivo_actual)

    # -------------------- Seleccionar carpeta --------------------
    def seleccionar_carpeta_descarga(self):
        nueva_ruta = filedialog.askdirectory(title="Selecciona carpeta de descarga", initialdir=self.ruta_descarga)
        if nueva_ruta:
            self.ruta_descarga = nueva_ruta
            print(f"Ruta de descarga seleccionada: {self.ruta_descarga}")

    # -------------------- Scroll con rueda --------------------
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
