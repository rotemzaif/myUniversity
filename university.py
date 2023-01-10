from crypt import methods
from csv import DictReader

import person
from person import *
import json

students_file_path = 'data/students_short.csv'
teachers_file_path = 'data/teachers_short.csv'
courses_file_path = 'data/courses.json'


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
        self._courses = []
        self.faculties = []
        self._persons = {}

    @property
    def persons(self):
        return self._persons

    @property
    def courses(self):
        return self._courses

    ''' persons methods'''

    def load_persons(self):
        with open(students_file_path, 'r') as csvfile:
            students = DictReader(csvfile)
            for s in students:
                try:
                    student = Student(s['identity_number'], s['full_name'], faculty=s['faculty'],
                                      start_date=s['start_date'], address=s['address'])
                    self.check_person_validity(student, self._persons)
                    self._persons[s['identity_number']] = student
                except Exception as e:
                    print(f'exception occurred for person {student} \nwhoms id already exists in the system')
        with open(teachers_file_path, 'r') as csvfile:
            teachers = DictReader(csvfile)
            for t in teachers:
                try:
                    teacher = Teacher(t['identity_number'], t['full_name'], faculty=t['faculty'],
                                      start_date=t['start_date'])
                    self.check_person_validity(teacher, self._persons)
                    self._persons[t['identity_number']] = teacher
                except Exception as e:
                    print(f'exception occurred for person {teacher} \nwhoms id already exists in the system')

    def check_person_validity(self, person, persons_dict):
        person_id = person.identity_num
        if person_id in persons_dict.keys():
            raise ValueError(f'Person with id {person_id} already exists.')

    def get_person_by_id(self, person_id):
        return self.persons.get(person_id, None)

    ''' faculties methods'''

    def get_faculties(self):
        with open(courses_file_path, 'r') as f:
            courses = json.load(f)
        faculties = list(set(list(map(lambda d: d['faculty'], courses))))
        return faculties

    ''' courses methods'''

    def load_courses(self):
        with open(courses_file_path, 'r') as jsonfile:
            courses = json.load(jsonfile)
        for course in courses:
            self._courses.append(Course(course['id'], course['name'], course['faculty'], course['points']))

    def add_course(self, person_id, course_id):
        """
        Adds the course (by id) to the person with the given identity_number.
        :param person_id: str, identity number of the person
        :param course_id: str, id of the course
        :return: None
        :error handling
            * ValueError in case person id or course id is missing
        """
        pass

