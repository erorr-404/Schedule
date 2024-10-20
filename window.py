from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QTabWidget
from tabs import MainWidget, ScheduleWidget, BooksWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title and initial size
        self.setWindowTitle("Schedule")
        self.setWindowIcon(QIcon("images/icon.png"))
        self.setFixedSize(1280, 720)

        self.tab_widget = QTabWidget()
# Set the position of the tabs (Qt.TabPosition.West to place them on the left)
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.West)
        # Set the QTabWidget as the central widget
        self.setCentralWidget(self.tab_widget)

        self.home_tab = MainWidget()
        self.schedule_tab = ScheduleWidget()
        self.books_tab = BooksWidget()

        self.tab_widget.addTab(
            self.home_tab, QIcon("images/home.png"), "Home")
        self.tab_widget.addTab(
            self.schedule_tab, QIcon("images/calendar.png"), "Schedule")
        self.tab_widget.addTab(
            self.books_tab, QIcon("images/book.png"), "Books")

