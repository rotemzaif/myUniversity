class Person:
    def __init__(self, identity_number, full_name):
        self.name = full_name
        self.identity_num = identity_number
        self.courses = []

    def person_type(self):
        return type(self).__name__


class Student(Person):
    def __init__(self, *args, faculty, start_date, address):
        self.faculty = faculty
        self.start_date = start_date
        self.address = address
        super().__init__(*args)

    def __repr__(self):
        return f'Student(ID: {self.identity_num}, full name: {self.name}, courses: {self.courses}, faculty: {self.faculty}, ' \
               f'address: {self.address}, start_date: {self.start_date})'


class Teacher(Person):
    def __init__(self, *args, faculty, start_date):
        super().__init__(*args)
        self.faculties = []
        self.faculties.append(faculty)
        self.start_date = start_date

    def __repr__(self):
        return f'Teacher(ID: {self.identity_num}, full name: {self.name}, faculties: {self.faculties}, start date: {self.start_date})'






