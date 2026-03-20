import sys
import os
import psutil
import platform
import subprocess
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                             QHBoxLayout, QGridLayout, QFrame, QPushButton)
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QPixmap, QFont, QIcon, QCursor

class AcercaDeCesarHibrido(QWidget):
    def __init__(self):
        super().__init__()
        self.oldPos = QPoint()
        self.initUI()

    def obtener_info_sistema_hibrida(self):
        """Detecta hardware y OS de forma nativa para Windows y Linux."""
        try:
            sistema = platform.system()
            usuario = os.getlogin()
            ram = f"{round(psutil.virtual_memory().total / (1024**3))} GB DDR4"

            if sistema == "Windows":
                # --- LÓGICA PARA WINDOWS ---
                distro = f"Windows {platform.release()}"
                cpu = platform.processor()
                # Intentar sacar la GPU con WMIC (nativo de Windows)
                try:
                    gpu_out = subprocess.check_output("wmic path win32_VideoController get name", shell=True).decode()
                    gpu = gpu_out.split('\n')[1].strip()
                except:
                    gpu = "GPU Compatible"
                self.info_cmd = ["msinfo32"]

            else:
                # --- LÓGICA PARA LINUX (SIN GREP) ---
                distro = "Linux System"
                if os.path.exists("/etc/os-release"):
                    with open("/etc/os-release") as f:
                        for line in f:
                            if "PRETTY_NAME" in line:
                                distro = line.split("=")[1].strip().replace('"', '')

                cpu = "Procesador Genérico"
                if os.path.exists("/proc/cpuinfo"):
                    with open("/proc/cpuinfo") as f:
                        for line in f:
                            if "model name" in line:
                                cpu = line.split(":")[1].strip()
                                break

                try:
                    # Usamos lspci pero procesamos el texto con Python, no con grep
                    gpu_out = subprocess.check_output("lspci", shell=True).decode()
                    for line in gpu_out.split('\n'):
                        if "VGA" in line or "3D controller" in line:
                            gpu = line.split(':')[-1].strip()
                            break
                except:
                    gpu = "GPU compatible con Mesa"

                self.info_cmd = ["kinfocenter"]

            # Acortar textos muy largos
            cpu = (cpu[:33] + '..') if len(cpu) > 33 else cpu
            gpu = (gpu[:33] + '..') if len(gpu) > 33 else gpu

            datos_lista = [
                ("Procesador", cpu),
                ("Gráficos", gpu),
                ("Memoria", ram),
                ("Propietario", usuario)
            ]
            return distro, datos_lista

        except Exception as e:
            return "Sistema", [("Error", "No se detectó hardware")]

    def obtener_nombre_imagen(self):
        """Detecta el tipo de chasis del equipo y devuelve la imagen correspondiente."""
        imagen = "aboutpc.png"  # Por defecto PC
        try:
            sistema = platform.system()
            chassis_type = -1

            if sistema == "Windows":
                out = subprocess.check_output("wmic systemenclosure get chassistypes", shell=True).decode()
                # Limpiamos las llaves "{}" que devuelve WMIC y buscamos el primer número
                numeros = [int(s) for s in out.replace('{', '').replace('}', '').split() if s.isdigit()]
                if numeros:
                    chassis_type = numeros[0]
            else:
                if os.path.exists("/sys/class/dmi/id/chassis_type"):
                    with open("/sys/class/dmi/id/chassis_type") as f:
                        chassis_type = int(f.read().strip())

            # Clasificación de códigos SMBIOS comunes
            if chassis_type in [8, 9, 10, 11, 14, 30, 31, 32]:
                imagen = "about.png"        # Laptops, Notebooks y Convertibles
            elif chassis_type == 13:
                imagen = "aboutaio.png"     # All in One
        except Exception:
            pass
        return imagen

    def initUI(self):
        # Configuración de ventana estilo Tahoe
        self.setFixedSize(380, 530)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setStyleSheet("""
            QWidget#MainFrame {
                background-color: rgba(25, 25, 25, 0.96);
                border-radius: 28px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            QLabel { color: white; background: none; font-family: 'SF Pro Display', sans-serif; }
            QPushButton#CerrarBtn { background-color: #ff5f57; border: none; border-radius: 7px; }
            QPushButton#MinBtn { background-color: #febc2e; border: none; border-radius: 7px; }
            QLabel.LabelKey { color: rgba(255, 255, 255, 0.5); font-size: 13px; font-weight: bold; }
            QLabel.LabelVal { color: white; font-size: 13px; }
            QPushButton#MoreInfoBtn {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 8px 18px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton#MoreInfoBtn:hover { background-color: rgba(255, 255, 255, 0.2); }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.container = QWidget()
        self.container.setObjectName("MainFrame")
        main_layout.addWidget(self.container)

        layout_v = QVBoxLayout(self.container)
        layout_v.setContentsMargins(20, 15, 20, 15)

        # 1. BOTONES
        botones_layout = QHBoxLayout()
        self.btn_close = QPushButton()
        self.btn_close.setObjectName("CerrarBtn")
        self.btn_close.setFixedSize(14, 14)
        self.btn_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_close.clicked.connect(self.close)
        self.btn_min = QPushButton()
        self.btn_min.setObjectName("MinBtn")
        self.btn_min.setFixedSize(14, 14)
        self.btn_min.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_min.clicked.connect(self.showMinimized)
        botones_layout.addWidget(self.btn_close)
        botones_layout.addSpacing(10)
        botones_layout.addWidget(self.btn_min)
        botones_layout.addStretch()
        layout_v.addLayout(botones_layout)

        # 2. IMAGEN
        layout_v.addSpacing(2)
        self.img_label = QLabel()
        if getattr(sys, 'frozen', False):
            ruta_script = sys._MEIPASS
        else:
            ruta_script = os.path.dirname(os.path.abspath(__file__))
        nombre_img = self.obtener_nombre_imagen()
        ruta_imagen = os.path.join(ruta_script, nombre_img)
        if os.path.exists(ruta_imagen):
            pixmap = QPixmap(ruta_imagen)
        else:
            pixmap = QIcon.fromTheme("video-display").pixmap(200, 200)
        self.img_label.setPixmap(pixmap.scaled(240, 240, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_v.addWidget(self.img_label)
        layout_v.addSpacing(10)

        # 3. DETECCIÓN Y TÍTULO
        distro_name, datos_sistema = self.obtener_info_sistema_hibrida()
        title = QLabel(distro_name)
        title.setFont(QFont("SF Pro Display", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_v.addWidget(title)
        layout_v.addSpacing(5)

        # GRID DE INFO
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(8)
        for i, (key, val) in enumerate(datos_sistema):
            k_lbl = QLabel(key)
            k_lbl.setProperty("class", "LabelKey")
            k_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
            grid_layout.addWidget(k_lbl, i, 0)
            v_lbl = QLabel(val)
            v_lbl.setProperty("class", "LabelVal")
            v_lbl.setAlignment(Qt.AlignmentFlag.AlignLeft)
            grid_layout.addWidget(v_lbl, i, 1)
        layout_v.addWidget(grid_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        layout_v.addStretch()

        # 4. BOTÓN MÁS INFO
        layout_v.addSpacing(18)
        self.btn_more_info = QPushButton("Más información...")
        self.btn_more_info.setObjectName("MoreInfoBtn")
        self.btn_more_info.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_more_info.clicked.connect(lambda: subprocess.Popen(self.info_cmd, shell=True))
        layout_v.addWidget(self.btn_more_info, alignment=Qt.AlignmentFlag.AlignCenter)

        layout_v.addStretch()
        layout_v.addSpacing(15)

        # PIE DE PÁGINA (CRÉDITOS)
        copy = QLabel("™ and © 2026 Cesar Morales & Gemini AI.\nAll Rights Reserved.")
        copy.setStyleSheet("color: rgba(255, 255, 255, 0.2); font-size: 10px;")
        copy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_v.addWidget(copy)

    # Lógica de movimiento
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.oldPos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.oldPos)
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AcercaDeCesarHibrido()
    ex.show()
    qr = ex.frameGeometry()
    cp = ex.screen().availableGeometry().center()
    qr.moveCenter(cp)
    ex.move(qr.topLeft())
    sys.exit(app.exec())
