import customtkinter as ctk
import psutil
import platform
import os
from tkinter import messagebox

class USBTab:
    def __init__(self, parent):
        self.parent = parent

        # Título general
        self.label = ctk.CTkLabel(parent, text="Gestión de USB", font=ctk.CTkFont(size=18, weight="bold"))
        self.label.pack(pady=10)

        # Frame principal contenedor de left y right
        self.main_frame = ctk.CTkFrame(parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # -------------------- Frame izquierdo --------------------
        self.left_frame = ctk.CTkFrame(self.main_frame)
        self.left_frame.pack(side="left", fill="y", padx=(0,10), pady=10)

        # Selector de USB
        self.usb_selector_label = ctk.CTkLabel(self.left_frame, text="Selecciona un USB:")
        self.usb_selector_label.pack(pady=10)

        self.usb_optionmenu = ctk.CTkOptionMenu(self.left_frame, values=[], command=self.mostrar_info_usb)
        self.usb_optionmenu.pack(pady=10, padx=10)

        # Frames de información debajo del selector
        self.info_total_frame = ctk.CTkFrame(self.left_frame)
        self.info_total_frame.pack(fill="x", pady=(20,5), padx=10)
        self.info_total_label = ctk.CTkLabel(self.info_total_frame, text="Tamaño total: -")
        self.info_total_label.pack(padx=10, pady=5, anchor="w")

        self.info_libre_frame = ctk.CTkFrame(self.left_frame)
        self.info_libre_frame.pack(fill="x", pady=5, padx=10)
        self.info_libre_label = ctk.CTkLabel(self.info_libre_frame, text="Espacio libre: -")
        self.info_libre_label.pack(padx=10, pady=5, anchor="w")

        self.info_formato_frame = ctk.CTkFrame(self.left_frame)
        self.info_formato_frame.pack(fill="x", pady=5, padx=10)
        self.info_formato_label = ctk.CTkLabel(self.info_formato_frame, text="Formato: -")
        self.info_formato_label.pack(padx=10, pady=5, anchor="w")

        # -------------------- Frame derecho --------------------
        self.right_frame = ctk.CTkFrame(self.main_frame)
        self.right_frame.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)

        # Frame OPL dentro del right_frame
        self.opl_frame = ctk.CTkFrame(self.right_frame)
        self.opl_frame.pack(fill="x", padx=10, pady=10)

        self.opl_label = ctk.CTkLabel(self.opl_frame, text="OPL", font=ctk.CTkFont(size=16, weight="bold"))
        self.opl_label.pack(pady=(10,5))

        # Separador simple
        self.separator = ctk.CTkFrame(self.opl_frame, height=2, fg_color="gray")
        self.separator.pack(fill="x", padx=5, pady=(0,10))

        # Botón CREAR CARPETAS
        self.crear_carpetas_button = ctk.CTkButton(self.opl_frame, text="CREAR CARPETAS", command=self.crear_carpetas)
        self.crear_carpetas_button.pack(pady=5)

        # -------------------- Inicializar USB --------------------
        self.usb_actuales = []
        self.listar_usb()
        self.parent.after(3000, self.actualizar_usb)  # cada 3 segundos revisa cambios

    # -------------------- Funciones --------------------
    def listar_usb(self):
        usb_drives = []
        sistema = platform.system()
        partitions = psutil.disk_partitions(all=False)
        for p in partitions:
            if sistema == "Windows":
                if 'removable' in p.opts:
                    usb_drives.append(p.device)
            else:
                # Linux: montajes comunes de USB
                if p.mountpoint.startswith("/media") or p.mountpoint.startswith("/run/media"):
                    usb_drives.append(p.mountpoint)

        if not usb_drives:
            self.usb_optionmenu.configure(values=["No se detectaron USB"])
            self.usb_optionmenu.set("No se detectaron USB")
            self.limpiar_info_usb()
        else:
            self.usb_optionmenu.configure(values=usb_drives)
            if self.usb_optionmenu.get() not in usb_drives:
                self.usb_optionmenu.set(usb_drives[0])
                self.mostrar_info_usb(usb_drives[0])

        self.usb_actuales = usb_drives

    def actualizar_usb(self):
        # vuelve a listar y compara con anterior
        usb_previos = set(self.usb_actuales)
        self.listar_usb()
        usb_nuevos = set(self.usb_actuales)
        if usb_previos != usb_nuevos:
            # refrescar info si cambió
            if self.usb_actuales:
                self.mostrar_info_usb(self.usb_optionmenu.get())
        self.parent.after(3000, self.actualizar_usb)  # sigue verificando

    def mostrar_info_usb(self, usb_path):
        try:
            usage = psutil.disk_usage(usb_path)
            self.info_total_label.configure(text=f"Tamaño total: {usage.total // (1024**3)} GB")
            self.info_libre_label.configure(text=f"Espacio libre: {usage.free // (1024**3)} GB")
            partitions = psutil.disk_partitions()
            fs = next((p.fstype for p in partitions if p.device == usb_path or p.mountpoint == usb_path), "Desconocido")
            self.info_formato_label.configure(text=f"Formato: {fs}")
        except:
            self.limpiar_info_usb()

    def limpiar_info_usb(self):
        self.info_total_label.configure(text="Tamaño total: -")
        self.info_libre_label.configure(text="Espacio libre: -")
        self.info_formato_label.configure(text="Formato: -")

    def crear_carpetas(self):
        usb_path = self.usb_optionmenu.get()
        if not os.path.ismount(usb_path):
            messagebox.showerror("Error", "Selecciona un USB válido montado.")
            return
        try:
            os.makedirs(os.path.join(usb_path, "CD"), exist_ok=True)
            os.makedirs(os.path.join(usb_path, "DVD"), exist_ok=True)
            messagebox.showinfo("Éxito", f"Se crearon las carpetas CD y DVD en {usb_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron crear las carpetas:\n{e}")
