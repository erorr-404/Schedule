class TimeStamp:
    def __init__(self, hour: int, minute: int):
        self.hour = hour
        self.minute = minute


class Subject:
    def __init__(self, name: str, importance: int, link: str):
        self.name = name
        self.importance = importance
        self.link = link


class Lesson:
    def __init__(self, subject: Subject, start: TimeStamp, end: TimeStamp):
        self.subject = subject
        self.start = start
        self.end = end


class Day:
    def __init__(self, day_number: int, lessons: list[Lesson]):
        if day_number in range(6):
            self.day_number = day_number
        else:
            self.day_number = None

        self.lessons = lessons


class Week:
    def __init__(self, days: list[Day]):
        if len(days) <= 5:
            self.days = days
        else:
            self.days = None