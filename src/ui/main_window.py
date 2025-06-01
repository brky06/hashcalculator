from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit,
    QLabel, QComboBox, QGroupBox, QGridLayout, QSizePolicy, QStyle, QApplication
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint
from PyQt5.QtGui import QFont, QPalette, QColor, QClipboard, QIcon

from utils.hash_utils import calculate_hash

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dark_mode = True  
        
        self.setWindowTitle("Hash Calculator")
        self.setGeometry(100, 80, 700, 450)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QGridLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        top_layout = QHBoxLayout()

        algo_group = QGroupBox("Algoritma Seçimi")
        algo_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        algo_layout = QHBoxLayout(algo_group)
        algo_layout.setContentsMargins(10, 10, 10, 10)

        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["MD2", "MD4", "MD5", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512", "blake2b", "blake2s", "SHAKE128", "SHAKE256", "CRC32"])

        combo_label = QLabel("Hash Algoritması:")
        combo_label.setFont(QFont("Arial", 10, QFont.Bold))

        algo_layout.addWidget(combo_label)
        algo_layout.addWidget(self.algo_combo)

        self.theme_button = QPushButton()
        self.theme_button.setFixedSize(60, 30) 
        self.theme_button.setStyleSheet("""
            QPushButton {
                border: 2px solid #555;
                border-radius: 15px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        self.theme_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarShadeButton))
        self.theme_button.clicked.connect(self.animate_theme_change)

        top_layout.addWidget(algo_group)
        top_layout.addWidget(self.theme_button)

        main_layout.addLayout(top_layout, 0, 0, 1, 2)

        text_group = QGroupBox("Metin")
        text_layout = QVBoxLayout(text_group)
        text_layout.setContentsMargins(10, 10, 10, 10)

        self.input_text = QTextEdit()
        self.input_text.setFont(QFont("Arial", 10))
        self.input_text.setPlaceholderText("Hash'lenecek metni giriniz...")
        text_layout.addWidget(self.input_text)

        self.hash_button = QPushButton("Hash Hesapla")
        self.hash_button.clicked.connect(self.calculate_hash)
        text_layout.addWidget(self.hash_button, alignment=Qt.AlignRight)

        main_layout.addWidget(text_group, 1, 0)

        result_group = QGroupBox("Sonuç")
        result_layout = QVBoxLayout(result_group)
        result_layout.setContentsMargins(10, 10, 10, 10)

        self.result_label = QLabel("Hash Sonucu:")
        self.result_label.setFont(QFont("Arial", 10, QFont.Bold))
        result_layout.addWidget(self.result_label)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        result_layout.addWidget(self.result_text)

        self.copy_button = QPushButton("Kopyala")
        self.copy_button.clicked.connect(self.copy_result_to_clipboard)
        result_layout.addWidget(self.copy_button, alignment=Qt.AlignRight)
        main_layout.addWidget(result_group, 1, 1)

        self.apply_theme()

    def toggle_theme(self):
        
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        if self.dark_mode:
            bg_color = "#2E2E2E"
            text_color = "#FFFFFF"
            widget_bg = "#3D3D3D"
            border_color = "#555"
            button_bg = "#5A5A5A"
            button_hover = "#707070"
            button_pressed = "#888888"
            self.theme_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarShadeButton))
        else:
            bg_color = "#F0F0F0"
            text_color = "#000000"
            widget_bg = "#FFFFFF"
            border_color = "#CCCCCC"
            button_bg = "#E0E0E0"
            button_hover = "#D0D0D0"
            button_pressed = "#C0C0C0"
            self.theme_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarUnshadeButton))

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(bg_color))
        self.setPalette(palette)

        group_style = f"""
            QGroupBox {{
                font-weight: bold;
                color: {text_color};
                border: 2px solid {border_color};
                border-radius: 6px;
                margin-top: 8px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }}
        """

        combo_style = f"""
            QComboBox {{
                font: 10pt 'Arial';
                color: {text_color};
                background-color: {widget_bg};
                border: 1px solid {border_color};
                border-radius: 4px;
                padding: 5px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {widget_bg};
                selection-background-color: {button_hover};
                color: {text_color};
            }}
        """

        text_style = f"""
            QTextEdit {{
                color: {text_color};
                background-color: {widget_bg};
                border: 1px solid {border_color};
                border-radius: 4px;
                padding: 6px;
            }}
            QTextEdit:hover {{
                background-color: {button_hover};
            }}
        """

        button_style = f"""
            QPushButton {{
                background-color: {button_bg};
                color: {text_color};
                font-weight: bold;
                font-size: 10pt;
                border-radius: 6px;
                border: 1px solid {border_color};
                padding: 6px 12px;
            }}
            QPushButton:hover {{
                background-color: {button_hover};
            }}
            QPushButton:pressed {{
                background-color: {button_pressed};
            }}
        """

        for group in self.findChildren(QGroupBox):
            group.setStyleSheet(group_style)

        self.algo_combo.setStyleSheet(combo_style)
        self.input_text.setStyleSheet(text_style)
        self.result_text.setStyleSheet(text_style)
        
        for button in self.findChildren(QPushButton):
            button.setStyleSheet(button_style)

        for label in self.findChildren(QLabel):
            label.setStyleSheet(f"color: {text_color};")

    def calculate_hash(self):
        text = self.input_text.toPlainText()
        algorithm = self.algo_combo.currentText().lower()
        result = calculate_hash(text, algorithm)
        self.result_text.setText(result)

    def copy_result_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.result_text.toPlainText())

    def animate_theme_change(self):
        self.anim = QPropertyAnimation(self.theme_button, b"pos")
        self.anim.setDuration(300)  
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        
        current_pos = self.theme_button.pos()
        
        if self.dark_mode:
            self.anim.setStartValue(current_pos)
            self.anim.setEndValue(QPoint(current_pos.x() + 30, current_pos.y()))
            self.theme_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarUnshadeButton))  
        else:
            self.anim.setStartValue(current_pos)
            self.anim.setEndValue(QPoint(current_pos.x() - 30, current_pos.y()))
            self.theme_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarShadeButton))  
        
        self.anim.start()
        
        self.dark_mode = not self.dark_mode
        self.apply_theme()
