# PS2 Game Downloader

**PS2 Game Downloader** es una aplicación moderna y completa para gestionar y descargar juegos y ELFs para PlayStation 2. Con una interfaz intuitiva basada en **CustomTkinter**, permite descargar juegos desde GitHub, gestionar unidades USB y mantener todo organizado para usarlo con tu consola a través de OPL (Open PS2 Loader).

---

## Características principales

- **Descarga de juegos PS2**:
  - Filtrado por nombre y categoría.
  - Visualización de iconos y estado de enlaces.
  - Barra de progreso con velocidad y tiempo estimado.
  - Control de pausa, reanudación y cancelación.

- **Descarga de archivos ELF**:
  - Lista de ELFs desde GitHub con versión y estado del link.
  - Descarga individual con barra de progreso.
  - Selección de carpeta de descarga.

- **Gestión de USB**:
  - Detección automática de USB conectados.
  - Información de tamaño total, espacio libre y formato.
  - Creación automática de carpetas CD y DVD para OPL.

- **Sección “Acerca de”**:
  - Información de la app y equipo.
  - Enlaces a GitHub, Facebook y página web.
  - Animación decorativa de derechos de autor.

---

## Requisitos

- Python 3.10 o superior
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Pillow
- psutil

Instala dependencias con:

```bash
pip install customtkinter pillow psutil
