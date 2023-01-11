from csv import DictReader
from person import *
import json


class Course:
    def __init__(self, ID, name, faculty, points):
        self.ID = ID
        self.name = name
        self.faculty = faculty
        self.points = points

    def __repr__(self):
        return f'Course(ID: {self.ID}, name: {self.name}, faculty: {self.faculty}, points: {self.points})'


class University:
    def __init__(self, name):
        self.name = name
        self._courses = {}
        self._faculties = []
        self._students = {}
        self._teachers = {}

    ''' getters'''
    @property
    def students(self):
        return self._students

    @property
    def teachers(self):
        return self._teachers

    @property
    def courses(self):
        return self._courses

    @property
    def faculties(self):
        return self._faculties

    ''' university methods '''

    def load_university_data(self, students_file, teachers_file, courses_file):
        self.load_students(students_file)
        self.load_teachers(teachers_file)
        self.load_faculties(courses_file)
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
                except Exception as e:
                    print(f'exception occurred for student {student.name} (id: {student.identity_num}) whom id already exists in the system')

    def load_teachers(self, file_path):
        with open(file_path, 'r') as csvfile:
            teachers = DictReader(csvfile)
            for t in teachers:
                try:
                    teacher = Teacher(t['identity_number'], t['full_name'], faculty=t['faculty'],
                                      start_date=t['start_date'])
                    self.check_person_validity(teacher, self._teachers)
                    self._teachers[t['identity_number']] = teacher
                except Exception as e:
                    print(f'exception occurred for teacher {teacher.name} (id: {teacher.identity_num}) whom id already exists in the system')

    def load_faculties(self, file_path):
        with open(file_path, 'r') as f:
            courses = json.load(f)
        self._faculties = list(set(list(map(lambda d: d['faculty'], courses))))

    def load_courses(self, file_apth):
        with open(file_apth, 'r') as jsonfile:
            courses = json.load(jsonfile)
        for course in courses:
            self._courses[str(course['id'])] = Course(str(course['id']), course['name'], course['faculty'],
                                                      course['points'])

    def get_student_total_points(self, student_id):
        total = 0
        student = self.get_person_by_id(student_id)
        for course_id in student.courses:
            total += self.courses[course_id].points
        return total

    ''' courses methods'''

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
        if course_id not in self.courses.keys():
            raise ValueError(f'Course with id {course_id} does not exist.')
        person = self.get_person_by_id(person_id)
        course_name = self.courses[course_id].name
        course_points = self.courses[course_id].points
        person_type = person.person_type()
        course_faculty = self.courses[course_id].faculty
        if course_id in person.courses:
            raise ValueError(
                f'The course id {course_id} ({course_name}) is already enrolled to {person_type} {person.name} id: {person.identity_num}')
        if person_type == 'Teacher':
            if len(person.faculties) == 3 and course_faculty not in person.faculties:
                raise PermissionError(
                    f"Cannot add course '{course_name}' (id: {course_id}, faculty: {course_faculty}) to {person_type} "
                    f"{person.name} (id: {person_id}) since he/she already teaches in 3 other faculties")
            if len(person.courses) == 12:
                raise PermissionError(
                    f"Cannot add course '{course_name}' (id: {course_id}, faculty: {course_faculty}) to {person_type} "
                    f"{person.name} (id: {person_id}) since he/she already teaches in 12 courses")
        if person_type == 'Student':
            student_tot_points = self.get_student_total_points(person_id)
            if course_faculty != person.faculty:
                raise PermissionError(f'Cannot add course "{course_name}" (id: {course_id}) since it does not belong to the assigned faculty '
                                      f'of student {person.name} (id: {person_id})')
            if student_tot_points + course_points > 30:
                raise PermissionError(
                    f'Cannot add course "{course_name}" (id: {course_id}) since student {person.name} total courses points will exceed 30 points')
        person.add_course(course_id) if person_type == 'Student' else person.add_course(course_id, course_faculty)

    ''' persons methods'''

    def check_person_validity(self, person, persons_dict):
        person_id = person.identity_num
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

