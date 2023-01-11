class Person:
    def __init__(self, identity_number, full_name):
        self.name = full_name
        self.identity_num = identity_number
        self.courses = []

    def person_type(self):
        # return type(self).__name__
        return self.__class__.__name__

    def add_course(self, course_id):
        self.courses.append(course_id)


class Student(Person):
    def __init__(self, *args, faculty, start_date, address):
        self.faculty = faculty
        self.start_date = start_date
        self.address = address
        super().__init__(*args)

    def get_total_courses_points(self):
        total = 0
        for course in self.courses:
            total += course.points
        return total

    def __repr__(self):
        return f'Student(ID: {self.identity_num}, full name: {self.name}, courses: {self.courses}, faculty: {self.faculty}, ' \
               f'address: {self.address}, start_date: {self.start_date})'


class Teacher(Person):
    def __init__(self, *args, faculty, start_date):
        super().__init__(*args)
        self.faculties = [faculty]
        self.start_date = start_date

    def add_course(self, course_id, course_faculty=None):
        self.courses.append(course_id)
        if course_faculty is not None and course_faculty not in self.faculties:
            self.faculties.append(course_faculty)

    def __repr__(self):
        return f'Teacher(ID: {self.identity_num}, full name: {self.name}, faculties: {self.faculties}, start date: {self.start_date})'






