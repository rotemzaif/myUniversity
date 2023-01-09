class Person:
    def __init__(self, full_name, identity_num):
        self.name = full_name
        self.identity_num = identity_num
        self.courses = []


class Student(Person):
    def __init__(self, *args, faculty, start_date, address):
        super().__init__(*args)
        self.faculty = faculty
        self.start_date = start_date
        self.address = address

    def __repr__(self):
        return f'Student({self.name}, {self.identity_num}, {self.courses}, {self.faculty}, {self.address}, {self.start_date})'


class Teacher(Person):
    def __init__(self, *args, faculties, start_date):
        super().__init__(*args)
        self.faculties = faculties
        self.start_date = start_date

    def __repr__(self):
        return f'Teacher({self.name}, {self.identity_num}, {self.faculties}, {self.start_date})'






