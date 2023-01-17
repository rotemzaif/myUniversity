from csv import DictReader
from itertools import islice
from person import *
import json
from datetime import datetime

students_file_path = 'data/students_short.csv'
teachers_file_path = 'data/teachers_short.csv'
courses_file_path = 'data/courses.json'


class Course:
    def __init__(self, course_id, name, faculty, points):
        self.course_id = course_id
        self.name = name
        self.faculty = faculty
        self.points = points

    def __repr__(self):
        return f'Course(ID: {self.course_id}, name: {self.name}, faculty: {self.faculty}, points: {self.points})'


class University:
    def __init__(self, name):
        self.name = name
        self.courses = {}
        self.faculties = []
        self._students = {}
        self._teachers = {}

    ''' getters'''

    @property
    def students(self):
        return self._students

    @property
    def teachers(self):
        return self._teachers

    ''' university methods '''

    def load_university_data(self, students_file, teachers_file, courses_file):
        self.load_students(students_file)
        self.load_teachers(teachers_file)
        # self.load_faculties(courses_file)
        self.load_courses(courses_file)

    def load_students(self, file_path):
        with open(file_path, 'r') as csvfile:
            students = DictReader(csvfile)
            for s in students:
                try:
                    student = Student(s['identity_number'], s['full_name'], faculty=s['faculty'],
                                      start_date=s['start_date'], address=s['address'])
                    self.check_person_validity(student, self._students)
                    self._students[s['identity_number']] = student
                except Exception:
                    print(
                        f'exception occurred for student {student.name} (id: {student.identity_number}) whom id already exists in the system')

    def load_teachers(self, file_path):
        with open(file_path, 'r') as csvfile:
            teachers = DictReader(csvfile)
            for t in teachers:
                try:
                    teacher = Teacher(t['identity_number'], t['full_name'], faculty=t['faculty'],
                                      start_date=t['start_date'])
                    self.check_person_validity(teacher, self._teachers)
                    self._teachers[t['identity_number']] = teacher
                except Exception:
                    print(
                        f'exception occurred for teacher {teacher.name} (id: {teacher.identity_number}) whom id already exists in the system')

    def load_faculties(self, file_path):
        with open(file_path, 'r') as f:
            courses = json.load(f)
        self.faculties = list(set(list(map(lambda d: d['faculty'], courses))))

    def load_courses(self, file_path):
        with open(file_path, 'r') as jsonfile:
            courses = json.load(jsonfile)
        for course in courses:
            course_dict = {"id": course['id'], "name": course['name'], "faculty": course['faculty'], "points": course['points']}
            self.courses[str(course['id'])] = course_dict
        self.load_faculties(file_path)

    def get_student_total_points(self, student_id):
        total = 0
        student = self.get_person_by_id(student_id)
        for course_id in student.courses.keys():
            total += self.courses[course_id]['points']
        return total

    def check_person_validity(self, person, persons_dict):
        person_id = person.identity_number
        person_type = person.person_type()
        if person_id in persons_dict.keys():
            raise ValueError(f'{person_type} with id {person_id} already exists in the university.')

    def get_person_by_id(self, person_id):
        if person_id in self.students.keys():
            return self.students[person_id]
        elif person_id in self.teachers.keys():
            return self.teachers[person_id]
        else:
            return None

    def get_faculties(self):
        """
        :return: all faculties collected from all the courses the university teaches.
        """
        return self.faculties

    def remove_person(self, identity_number):
        """
        Removes a person (student or teacher) from the University only if it has no courses enrolled to it
        :param identity_number: str - person (student or teacher) id number
        :return: None
        :error handling
            * NameError in case identity number is not in the university
            * PermissionError in case the person has any courses enrolled to it
        """
        person = self.get_person_by_id(identity_number)
        person_type = person.person_type()
        if not person:
            raise NameError(f'Given id number {identity_number} is not listed in the university')
        if len(person.courses) > 0:
            raise PermissionError(
                f"Cannot remove {person_type}: {person.name} (id: {person.identity_num}) "
                f"since he/she is enrolled to at least 1 course")
        self.students.pop(identity_number) if person_type == "Student" else self.teachers.pop(identity_number)

    def get_courses(self, identity_number):
        """
        Returns a list of courses the person (student/teacher) has enrolled to him
        :param identity_number: str - person id number
        :return: list of all course dictionaries the person (student/teacher) is enrolled in
        :error handling
            * NameError in case identity number is not in the system
        """
        person = self.get_person_by_id(identity_number)
        if not person:
            raise NameError(f'Given id number {identity_number} is not listed in the university')
        return list(person.courses.values()) if len(person.courses) > 0 else []


    ''' assistance methods '''
    def check_date_format(self, date_str):
        """
        Checks if the given date string is in dd/mm/yyyy format
        :param date_str: str - date string
        :return: bool - True if the date string is in the correct format, False otherwise
        """
        format = '%d/%m/%Y'
        try:
            result = bool(datetime.strptime(date_str, format))
            return result
        except ValueError:
            return False

    def compare_dates(self, date1, date2):
        """
        Converts given date strings to date objects and compares between the two dates objects
        :param date1: str - first date string
        :param date2: str - second date string
        :return: bool - True if date1 is similar or bigger than date2, False if otherwise
        """
        dt_obj1 = datetime.strptime(date1, '%d/%m/%Y')
        dt_obj2 = datetime.strptime(date2, '%d/%m/%Y')
        return True if dt_obj2 >= dt_obj1 else False

    ''' courses methods '''
    def get_course_by_id(self, course_id):
        """
        returns a course dictionary
        :param course_id: int
        :return: returns a course object
        """
        return self.courses[str(course_id)] if str(course_id) in self.courses.keys() else None

    def add_course(self, person_id, course_id):
        """
        Adds the course (by id) to the person with the given identity_number.
        :param person_id: str, identity number of the person
        :param course_id: str, id of the course
        :return: None
        :error handling
            * ValueError in case person id or course id is missing
        """
        if not self.get_person_by_id(person_id):
            raise ValueError(f'Person with id {person_id} does not exist.')
        if str(course_id) not in self.courses.keys():
            raise ValueError(f'Course with id {course_id} does not exist.')
        person = self.get_person_by_id(person_id)
        course = self.get_course_by_id(str(course_id))
        person_type = person.person_type()
        if str(course_id) in person.courses.keys():
            raise ValueError(
                f'The course id {course_id} ({course.name}) is already enrolled to {person_type} {person.name} id: {person.identity_num}')
        if person_type == 'Teacher':
            if len(person.faculties) == 3 and course.faculty not in person.faculties:
                raise PermissionError(
                    f"Cannot add course '{course.name}' (id: {course_id}, faculty: {course.faculty}) to {person_type} "
                    f"{person.name} (id: {person_id}) since he/she already teaches in 3 other faculties")
            if len(person.courses) == 12:
                raise PermissionError(
                    f"Cannot add course '{course.name}' (id: {course_id}, faculty: {course.faculty}) to {person_type} "
                    f"{person.name} (id: {person_id}) since he/she already teaches in 12 courses")
        if person_type == 'Student':
            student_tot_points = self.get_student_total_points(person_id)
            if course['faculty'] != person.faculty:
                raise PermissionError(
                    f'Cannot add course "{course.name}" (id: {course_id}) since it does not belong to the assigned faculty '
                    f'of student {person.name} (id: {person_id})')
            if student_tot_points + course['points'] > 30:
                raise PermissionError(
                    f'Cannot add course "{course.name}" (id: {course_id}) since student {person.name} total courses points will exceed 30 points')
        person.add_course(course)

    def remove_course(self, person_id, course_id):
        """
        Removes the course from the correct person (student/teacher)
        :param person_id: str, identity number of the person
        :param course_id: int, id of the course
        :return: None
        :error handling
            * given person id doesn't exist, raise ValueError
            * given course id doesn't, raise ValueError
            * If the person isn’t enrolled in the course, do nothing.
        """
        person = self.get_person_by_id(person_id)
        if not person:
            raise ValueError(f'Person with id {person_id} does not exist in the university.')
        if str(course_id) not in self.courses.keys():
            raise ValueError(f'course with id {course_id} is not listed in the university.')
        if str(course_id) in person.courses.keys():
            course = self.get_course_by_id(course_id)
            person.remove_course(course)

    def list_courses(self):
        """
        :return: a list of dictionaries of the courses offered
        """
        return list(self.courses.values())

    ''' students methods '''
    def get_students(self):
        return list(self.students.values())

    def get_number_of_students(self):
        return len(self.students)

    def change_faculty(self, identity_number, faculty):
        """
        changes the faculty of the student only if he has no courses enrolled in other faculties.
        :param identity_number: str - student id number
        :param faculty: str - faculty name
        :return: None
        :error handling
            * NameError in case identity number is not in the system
            * If the desired faculty is the same as current faculty, do nothing.
            * PermissionError If the student has courses enrolled in it from another faculty,
            * ValueError in case the faculty isn't listed in the University
        """
        if identity_number not in self.students.keys() or identity_number in self.teachers.keys():
            raise NameError(f'Given id number {identity_number} is not in the system')
        if faculty not in self.faculties:
            raise ValueError(f"Given faculty: {faculty} is not listed in the university")
        student = self.get_person_by_id(identity_number)
        if len(student.courses) > 0 and student.faculty != faculty:
            raise PermissionError(
                f"Cannot change the faculty for student: {student.name} since he is enrolled to courses in "
                f"the faculty: {student.faculty}")
        if len(student.courses) == 0 and student.faculty != faculty:
            student.faculty = faculty

    def add_student(self, identity_number, full_name, faculty, start_date, address):
        """
        Creates a new student in the system assigned with the relevant faculty.
        :param identity_number: str - The identity number of the person.
        :param full_name: str - The full name of the person.
        :param faculty: str - the faculty assigned to the person
        :param start_date: str - the start date of the student in YYYY format
        :param address: str - by default None since it is relevant only for students
        :return: None
        :error handling
            * NameError if identity number is already in the university
            * PermissionError if identity_number isn’t 9 digits
            * ValueError if the given faculty does not exist in the university
            * TypeError if start_year isn’t in the yyyy date format,
        """
        if identity_number in self.students.keys() or identity_number in self.teachers.keys():
            raise NameError(f'Given id number {identity_number} is already in the university')
        if not identity_number.isdigit() or len(identity_number) != 9:
            raise PermissionError(f'Invalid id number {identity_number}. ID number should be 9 digits')
        if faculty not in self.faculties:
            raise ValueError(f"Given faculty '{faculty}' is not listed in the university")
        if not str(start_date).isdigit() or len(str(start_date)) != 4:
            raise TypeError(f'Invalid start year format. Start year must be in the yyyy format')
        self.students[identity_number] = Student(identity_number, full_name, faculty=faculty, start_date=start_date, address=address)

    ''' teachers methods '''

    def get_teachers(self):
        """
        Returns a list of all teachers enrolled in the university
        :return: a list of teachers objects
        """
        return list(self.teachers.values())

    def get_number_of_teachers(self):
        """
        Returns the number of teachers enrolled in the university
        :return: int - number of teachers
        """
        return len(self.teachers)

    def add_teacher(self, identity_number, full_name, faculty, start_date):
        """
        Creates a new teacher in the system with a given faculty.
        :param identity_number: str - The identity number of the person.
        :param full_name: str - The full name of the person.
        :param faculty: str - the faculty assigned to the person
        :param start_date: str - the start date of the teacher in dd/mm/YYYY format
        :return: None
        :error handling
            * NameError if identity number is already in the university
            * PermissionError if identity_number isn’t 9 digits
            * ValueError if the given faculty does not exist in the university
            * TypeError if start_year isn’t in the dd/mm/yyyy date format,
        """
        if identity_number in self.students.keys() or identity_number in self.teachers.keys():
            raise NameError(f'Given id number {identity_number} is already in the university')
        if not identity_number.isdigit() or len(identity_number) != 9:
            raise PermissionError(f'Invalid id number {identity_number}. ID number should be 9 digits')
        if faculty not in self.faculties:
            raise ValueError(f"Given faculty '{faculty}' is not listed in the university")
        if not self.check_date_format(start_date):
            raise TypeError(f"Given start date '{start_date}' is not in the correct format (dd/mm/yyyy)")
        self.teachers[identity_number] = Teacher(identity_number, full_name, faculty=faculty, start_date=start_date)

    ''' general methods '''

    def get_top_10_students(self):
        """
        Return a list of students “full name”. Sorted by total course points (high to low).
        If multiple students share the same number of points, “inner sort” them lexicographically by their full name
        (Descending: Z to A).
        :return: a list of the top 10 students with most course points taken.
        """
        students_list_sorted_by_points = sorted(self.get_students(), key=lambda x: (x.points, x.name), reverse=True)
        students_names = list(map(lambda student: student.name, students_list_sorted_by_points))
        return list(islice(students_names, 10))

    def get_students_zip_code(self):
        """
        Returns a sorted unique list of strings with the student's city and zip codes - “city zip-code” format,
        e.g. “Haifa 922745”.
        :return: a unique (=no repetitions) list of all the students' zip code and cities in “city zip-code” format
        sorted alphabetically (from a to z).
        """
        if len(self.get_students()) == 0:
            return []
        zipcode_list = []
        for s in self.students.values():
            address = s.address
            city, country, zip_code = tuple(address.split(','))
            zipcode_list.append(f'{city.strip()} {zip_code.strip()}')
        return sorted(zipcode_list)

    def get_teachers_from(self, date_str):
        """
        Returns a sorted list of teachers' names of all teachers started after the given date, sorted by dates (old to new).
        If more than one teacher has the same start date, “inner sort” them lexicographically by their full name
        (Ascending: A to Z).
        :param date_str: str - start date in dd/mm/yyyy format.
        :return: a list of names of all teachers started after the given date sorted by dates (old to new).
        :error handling
            * ValueError - If the given date isn’t in dd/mm/yyyy format
            * if no teachers match the given date, return an empty list
        """
        if not self.check_date_format(date_str):
            raise ValueError(f'Given date: {date_str} is not in dd/mm/yyyy format')
        teachers_list = [t for t in self.get_teachers() if self.compare_dates(date_str, t.start_date)]
        teachers_list.sort(key=lambda x: (datetime.strptime(x.start_date, '%d/%m/%Y'), x.name))
        return list(map(lambda x: (x.name, x.start_date), teachers_list))
