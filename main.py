import sys
from PySide6.QtWidgets import QApplication
import db_handler
import window
import asyncio
from qasync import QEventLoop


if __name__ == '__main__':
    db = db_handler.DBHandler()
    db.create_tables()
    db.close_db()

    app = QApplication(sys.argv)

    with open("styles.qss", "r") as file:
        app.setStyleSheet(file.read())

    # Integrate the event loop with asyncio using QEventLoop
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    main_window = window.MainWindow()
    main_window.show()

    # Start the event loop
    with loop:
        loop.run_forever()
