import customtkinter as ctk
from GUI.juegos_tab import JuegosTab
from GUI.usb_tab import USBTab
from GUI.about_tab import AboutTab
from GUI.elf_downloader_tab import ElfDownloaderTab
import platform

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mi App Modular")

        # Maximizar ventana según sistema operativo
        sistema = platform.system()
        if sistema == "Windows":
            self.state("zoomed")
        else:
            try:
                self.attributes("-zoomed", True)
            except:
                self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

        # Crear Tabs
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(padx=10, pady=10, expand=True, fill="both")

        # Agregar pestañas en el orden deseado
        self.tab_view.add("JUEGOS")
        self.tab_view.add("ELF")
        self.tab_view.add("USB")
        self.tab_view.add("Acerca de")

        # Inicializar cada pestaña
        JuegosTab(self.tab_view.tab("JUEGOS"))
        USBTab(self.tab_view.tab("USB"))
        ElfDownloaderTab(self.tab_view.tab("ELF"))
        AboutTab(self.tab_view.tab("Acerca de"))

if __name__ == "__main__":
    app = App()
    app.mainloop()
