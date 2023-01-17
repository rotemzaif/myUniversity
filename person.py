from enum import Enum
class Person:
    def __init__(self, identity_number, full_name):
        self.name = full_name
        self.identity_number = identity_number
        self.courses = {}

    def person_type(self):
        # return type(self).__name__
        return self.__class__.__name__

    def add_course(self, course):
        self.courses[str(course['id'])] = course

    def remove_course(self, course):
        self.courses.pop(str(course['id']))


class Student(Person):
    def __init__(self, *args, faculty, start_date, address):
        self.faculty = faculty
        self.start_date = start_date
        self.address = address
        self._points = 0
        super().__init__(*args)

    @property
    def points(self):
        return self._points

    def get_total_courses_points(self):
        total = 0
        for course in self.courses:
            total += course.points
        return total

    def add_course(self, course):
        # self.courses[course.course_id] = course
        super().add_course(course)
        self._points += course['points']

    def __repr__(self):
        courses_id = list(map(lambda c: c['id'], self.courses))
        return f'Student(ID: {self.identity_number}, full name: {self.name}, courses: {courses_id}, faculty: {self.faculty}, ' \
               f'address: {self.address}, start_date: {self.start_date}, points: {self.points})'


class Teacher(Person):
    def __init__(self, *args, faculty, start_date):
        super().__init__(*args)
        self.faculties = [faculty]
        self.start_date = start_date

    def add_course(self, course):
        super().add_course(course)
        if course['faculty'] not in self.faculties:
            self.faculties.append(course['faculty'])

    def remove_course(self, course):
        super().remove_course(course)
        courses_faculties = list(map(lambda f: f['faculty'], self.courses.values()))
        if not course['faculty'] in courses_faculties:
            self.faculties.remove(course['faculty'])

    def __repr__(self):
        return f'Teacher(ID: {self.identity_number}, full name: {self.name}, faculties: {self.faculties}, start date: {self.start_date})'





