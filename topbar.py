from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout


class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(20)  # Set the height of the custom title bar

        # Layout for the custom title bar
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Window title
        self.title_label = QLabel("Schedule")
        self.title_label.setStyleSheet("color: white; font-size: 16px;")
        layout.addWidget(self.title_label)

        # Spacer to push buttons to the right
        layout.addStretch()

        # Minimize button
        self.minimize_button = QPushButton("-")
        self.minimize_button.setFixedSize(25, 25)
        self.minimize_button.clicked.connect(self.on_minimize)
        layout.addWidget(self.minimize_button)

        # Close button
        self.close_button = QPushButton("X")
        self.close_button.setFixedSize(25, 25)
        self.close_button.clicked.connect(self.on_close)
        layout.addWidget(self.close_button)

        # Styling the title bar
        self.setStyleSheet("""
            background-color: #282c34;
            padding: 2px 10px;
            
            QPushButton {
                border: none;
                color: white;
                font-size: 5px;
            }
            
            QPushButton:hover {
                background-color: #ff5555;
            }
        """)

    def on_minimize(self):
        self.window().showMinimized()

    def on_close(self):
        self.window().close()