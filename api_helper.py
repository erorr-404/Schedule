import asyncio
import aiohttp
from data import TimeStamp, Subject, Lesson, Day, Week

SCHEDULE = "http://vl4-timetable.pp.ua/data/timetable.json"
IMPORTANCE = "http://vl4-timetable.pp.ua/data/importance.json"
TIME = "http://vl4-timetable.pp.ua/data/time.json"
BOOKS = "http://vl4-timetable.pp.ua/data/books.json"
LINKS = "http://vl4-timetable.pp.ua/data/links.json"


class ApiHelper:
    async def get_schedule(self):
        urls = [SCHEDULE, IMPORTANCE, TIME, BOOKS, LINKS]
        # get raw data
        raw_data = await self.gather_all(urls)
        # divide raw data
        timetable, importance, time, books, links = raw_data

        subjects = []
        # iterate through all keys in links and create all subjects
        for l_key in links.keys():
            subjects.append(
                Subject(l_key, int(importance[l_key]), links[l_key]))

        # create time stamps in format: (TimeStamp(start), TimeStamp(end))
        time_stamps = []
        for key in time.keys():
            start_time_stamp = TimeStamp(
                time[key]["start"]["hour"], time[key]["start"]["minute"])
            end_time_stamp = TimeStamp(
                time[key]["end"]["hour"], time[key]["end"]["minute"])
            time_stamps.append((start_time_stamp, end_time_stamp))

        days = []
        for key in timetable.keys():
            switcher = {
                "monday": 0,
                "tuesday": 1,
                "wednesday": 2,
                "thursday": 3,
                "friday": 4
            }
            day_pos = switcher.get(key, -1)
            today_lessons = timetable.get(key, None)
            cur_day_lessons = []
            for index, lesson in enumerate(today_lessons):  # lesson: string
                subject = self.find_subject_with_name(lesson, subjects)
                if subject is None:
                    print(f"Cant find subject {lesson} in {today_lessons}")
                else:
                    cur_day_lessons.append(
                        Lesson(subject, time_stamps[index][0],
                               time_stamps[index][1]))
            days.append(Day(day_pos, cur_day_lessons))

        week = Week(days)
        return week

    def find_subject_with_name(self, name: str, subjects: list[Subject]):
        for subject in subjects:
            if subject.name == name:
                return subject
        return None

    async def gather_all(self, urls):
        results = await self.fetch_data(urls)
        return results

    async def fetch_data(self, urls: list[str]):
        """Fetch data from multiple URLs concurrently."""
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                # Schedule the fetch_json coroutine and add to the task list
                tasks.append(self.fetch_json(session, url))

            # Wait for all tasks to complete (run them concurrently)
            results = await asyncio.gather(*tasks)

            # Filter out None results if there were any failures
            return [result for result in results if result is not None]

    async def fetch_json(self, session, url):
        """Fetch JSON data asynchronously from a URL."""
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()  # Return the JSON response
            else:
                print(
                    f"Failed to fetch from {url}.",
                    f"Status code: {response.status}")
                return None
