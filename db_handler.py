import sqlite3
from data import *

DATABASE_PATH = "schedule.db"
TASK_TABLE_NAME = "tasks"


class DBHandler:
    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.connection.cursor()
        self.create_tables()

    # Insert into the database example:
    # db = DBHandler()
    # db.create_tables()
    # db.insert_week(week)

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS TimeStamp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hour INTEGER NOT NULL,
            minute INTEGER NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Subject (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            importance INTEGER NOT NULL,
            link TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Lesson (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            start_id INTEGER NOT NULL,
            end_id INTEGER NOT NULL,
            FOREIGN KEY (subject_id) REFERENCES Subject(id),
            FOREIGN KEY (start_id) REFERENCES TimeStamp(id),
            FOREIGN KEY (end_id) REFERENCES TimeStamp(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Day (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day_number INTEGER NOT NULL,
            lesson_id INTEGER NOT NULL,
            FOREIGN KEY (lesson_id) REFERENCES Lesson(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Week (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day_id INTEGER NOT NULL,
            FOREIGN KEY (day_id) REFERENCES Day(id)
        )
        """)

        self.connection.commit()

    def find_subject(self, subject: Subject):
        """Check if a Subject already exists in the database and return its ID."""
        self.cursor.execute("SELECT id FROM Subject WHERE name = ? AND importance = ? AND link = ?",
                            (subject.name, subject.importance, subject.link))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def insert_subject(self, subject: Subject):
        """Insert a Subject only if it doesn't already exist and return its ID."""
        subject_id = self.find_subject(subject)
        if subject_id:
            return subject_id  # Subject already exists, return its ID

        # Subject doesn't exist, so insert it
        self.cursor.execute("INSERT INTO Subject (name, importance, link) VALUES (?, ?, ?)",
                            (subject.name, subject.importance, subject.link))
        self.connection.commit()
        return self.cursor.lastrowid

    def find_timestamp(self, timestamp: TimeStamp):
        """Check if a TimeStamp already exists in the database and return its ID."""
        self.cursor.execute("SELECT id FROM TimeStamp WHERE hour = ? AND minute = ?",
                            (timestamp.hour, timestamp.minute))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def insert_timestamp(self, timestamp: TimeStamp):
        """Insert a TimeStamp only if it doesn't already exist and return its ID."""
        timestamp_id = self.find_timestamp(timestamp)
        if timestamp_id:
            return timestamp_id  # TimeStamp already exists, return its ID

        # TimeStamp doesn't exist, so insert it
        self.cursor.execute("INSERT INTO TimeStamp (hour, minute) VALUES (?, ?)",
                            (timestamp.hour, timestamp.minute))
        self.connection.commit()
        return self.cursor.lastrowid

    def insert_lesson(self, lesson: Lesson):
        """Insert a Lesson object and return its ID."""
        subject_id = self.insert_subject(lesson.subject)  # This will handle subject uniqueness
        start_id = self.insert_timestamp(lesson.start)  # Handle timestamp uniqueness
        end_id = self.insert_timestamp(lesson.end)  # Handle timestamp uniqueness

        self.cursor.execute("INSERT INTO Lesson (subject_id, start_id, end_id) VALUES (?, ?, ?)",
                            (subject_id, start_id, end_id))
        self.connection.commit()
        return self.cursor.lastrowid

    def insert_day(self, day: Day):
        # Insert lessons and associate them with the day
        for lesson in day.lessons:
            lesson_id = self.insert_lesson(lesson)
            self.cursor.execute("INSERT INTO Day (day_number, lesson_id) VALUES (?, ?)",
                                (day.day_number, lesson_id))
        self.connection.commit()

    def insert_week(self, week: Week):
        """Insert a Week object and its days."""
        for day in week.days:
            self.insert_day(day)

        for day in week.days:
            self.cursor.execute("INSERT INTO Week (day_id) VALUES (?)", (day.day_number,))
        self.connection.commit()

    def close_db(self):
        self.connection.close()