# PS2 Game Downloader 🎮

[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/tu_usuario/ps2-game-downloader?style=social)](https://github.com/tu_usuario/ps2-game-downloader/stargazers)

**PS2 Game Downloader** es una aplicación moderna para descargar y gestionar juegos y ELFs para PlayStation 2. Su interfaz intuitiva basada en **CustomTkinter** permite manejar descargas, unidades USB y mantener todo organizado para usarlo con OPL (Open PS2 Loader).

---

## 🎯 Características principales

- **Descarga de juegos PS2**:
  - Filtrado por nombre y categoría.
  - Iconos de juego y estado de enlace.
  - Barra de progreso con velocidad y tiempo estimado.
  - Control de pausa, reanudación y cancelación.

- **Descarga de archivos ELF**:
  - Lista de ELFs desde GitHub con versión y estado del enlace.
  - Descarga individual con barra de progreso.
  - Selección de carpeta de descarga.

- **Gestión de USB**:
  - Detección automática de unidades USB.
  - Información de tamaño, espacio libre y formato.
  - Creación automática de carpetas CD y DVD para OPL.

- **Sección “Acerca de”**:
  - Información del proyecto y equipo.
  - Enlaces a GitHub, Facebook y página web.
  - Animación decorativa de derechos de autor.

---

## 🖼 Capturas de pantalla

### Pestaña Juegos
![Juegos](./GUI/Images/screenshots/juegos.png)

### Pestaña ELF
![ELF](./GUI/Images/screenshots/elf.png)

### Pestaña USB
![USB](./GUI/Images/screenshots/usb.png)

### Pestaña Acerca de
![Acerca de](./GUI/Images/screenshots/about.png)

> Nota: Coloca tus capturas en `GUI/Images/screenshots/` y ajusta los nombres si cambian.

---

## ⚙ Requisitos

- Python 3.10 o superior
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Pillow
- psutil

Instala dependencias con:

```bash
pip install customtkinter pillow psutil
