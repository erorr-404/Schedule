from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton

import api_helper
import db_handler


class ScheduleWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Schedule")
        self.layout.addWidget(self.label)


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.schedule = None
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.layout)

        self.default_schedule_contr_widget = QWidget()
        self.default_schedule_contr_layout = QHBoxLayout()
        self.default_schedule_contr_widget.setLayout(self.default_schedule_contr_layout)

        self.restore_schedule = QPushButton("Restore default schedule")
        self.restore_schedule.clicked.connect(self.fetch_schedule)
        self.default_schedule_contr_layout.addWidget(self.restore_schedule)

        self.label = QLabel("Home")
        self.default_schedule_contr_layout.addWidget(self.label)

        self.layout.addWidget(self.default_schedule_contr_widget)

    def fetch_schedule(self):
        api = api_helper.ApiHelper()
        self.schedule = api.get_schedule()
        db = db_handler.DBHandler()
        db.insert_week(self.schedule)


class BooksWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Books")
        self.layout.addWidget(self.label)
