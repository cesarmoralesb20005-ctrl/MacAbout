# MacAbout 💻

**MacAbout** es una utilidad ligera y elegante inspirada en el diseño de macOS Sequoia para visualizar la información técnica de tu equipo. Fue desarrollada originalmente en **CachyOS (Linux)** y optimizada para ser totalmente funcional en **Windows**.

## 🚀 Características Principales

* **Detección Híbrida Automática**: El programa identifica si se está ejecutando en Windows o Linux y utiliza los comandos nativos correspondientes (`wmic` o archivos de sistema) para mostrar la información real.
* **Detección de Chasis**: Detecta automáticamente si el equipo es una **Laptop**, una **PC de Escritorio** o una **All-in-One** para mostrar la imagen adecuada (`about.png`, `aboutpc.png` o `aboutaio.png`).
* **Interfaz Estilo Tahoe**: Diseño minimalista con bordes redondeados, botones de control tipo semáforo y soporte para transparencias.
* **Información en Tiempo Real**: Muestra el Procesador, Gráficos (GPU), Memoria RAM total y el Usuario actual del sistema.
* **Acceso Rápido**: Incluye un botón de "Más información..." que abre las herramientas nativas del sistema (`kinfocenter` en Linux o `msinfo32` en Windows).

## 📦 Descargas (Releases)

Si solo quieres usar la aplicación sin instalar nada, ve a la sección de **[Releases](https://github.com/cesarmoralesb20005-ctrl/MacAbout/releases)** y descarga:
* **Windows**: El archivo `.exe` único.
* **Linux**: El binario ejecutable o AppImage.

## 🛠️ Desarrollo y Requisitos

Si deseas modificar el código o colaborar en el proyecto, necesitas tener instalado **Python 3.10+** y las siguientes librerías:

* **PyQt6**: Para la interfaz gráfica.
* **psutil**: Para la lectura de la memoria RAM.

### Instalación para desarrolladores:
1. Clona este repositorio:
   ```bash
   git clone [https://github.com/cesarmoralesb20005-ctrl/MacAbout.git](https://github.com/cesarmoralesb20005-ctrl/MacAbout.git)

# MacAbout
Basicamente, un programa que te muestra datos basicos de tu pc o laptop como si fuera "about this mac", funciona tanto para Windows como Linux.

