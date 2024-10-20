from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from qasync import asyncSlot  # qasync integrates asyncio with PyQt
import api_helper
import db_handler
import json

with open("strings.json") as strings_json:
    strings = json.load(strings_json)


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

        self.label = QLabel("Home")
        self.layout.addWidget(self.label)

        self.default_schedule_contr_widget = QWidget()
        self.default_schedule_contr_layout = QHBoxLayout()
        self.default_schedule_contr_widget.setLayout(
            self.default_schedule_contr_layout)

        self.restore_schedule = QPushButton("Restore default schedule")
        self.restore_schedule.clicked.connect(self.fetch_button_clicked)
        self.default_schedule_contr_layout.addWidget(self.restore_schedule)

        self.restore_schedule_label = QLabel(
            strings.get("restore_label", "Error"))
        self.default_schedule_contr_layout.addWidget(
            self.restore_schedule_label)

        self.layout.addWidget(self.default_schedule_contr_widget)

    # This decorator allows async functions to be used in PyQt slots
    @asyncSlot()
    async def fetch_button_clicked(self):
        # Async task called when button is clicked
        print("Button pressed, starting async task...")
        api = api_helper.ApiHelper()
        self.schedule = await api.get_schedule()

        db = db_handler.DBHandler()
        await db.insert_week(self.schedule)


class BooksWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Books")
        self.layout.addWidget(self.label)
