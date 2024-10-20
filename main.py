import sys
from PySide6.QtWidgets import QApplication
import db_handler
import window


if __name__ == '__main__':
    db = db_handler.DBHandler()
    db.create_tables()
    db.close_db()

    app = QApplication(sys.argv)

    with open("styles.qss", "r") as file:
        app.setStyleSheet(file.read())

    main_window = window.MainWindow()
    main_window.show()
    sys.exit(app.exec())
