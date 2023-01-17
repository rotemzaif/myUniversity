import unittest
from university import University

students_file_path = 'data/students_short.csv'
teachers_file_path = 'data/teachers_short.csv'
courses_file_path = 'data/courses.json'

class UniversityTest(unittest.TestCase):
    """ Test for University """

    def test_constructor(self):
        University("myUniversity")

    def test_all_methods_exists(self):
        uni = University("myUniversity")
        # university methods
        self.assertTrue(uni.get_person_by_id)
        self.assertTrue(uni.load_faculties)
        self.assertTrue(uni.load_courses)
        self.assertTrue(uni.add_course)
        self.assertTrue(uni.remove_course)
        self.assertTrue(uni.remove_person)


        # students methods
        self.assertTrue(uni.load_students)
        self.assertTrue(uni.get_students)
        self.assertTrue(uni.get_number_of_students)
        self.assertTrue(uni.get_number_of_students)
        self.assertTrue(uni.change_faculty)
        self.assertTrue(uni.add_student)

        # teachers methods
        self.assertTrue(uni.load_teachers)
        self.assertTrue(uni.get_teachers)
        self.assertTrue(uni.get_number_of_teachers)

        # general methods
        self.assertTrue(uni.get_top_10_students)
        self.assertTrue(uni.get_students_zip_code)
        self.assertTrue(uni.get_teachers_from)

    def test_get_person_by_id_student(self):
        uni = University("my_uny")
        uni.load_courses(courses_file_path)
        uni.add_student("883720579", "Sandie Leifeste", "Arts", "2008", "Rio Branco, Bulgaria, 6196762")
        sandie = uni.get_person_by_id("883720579")
        self.assertEqual(sandie.identity_number, "883720579")

    def test_get_faculties(self):
        uni = University("my_uny")
        uni.load_courses(courses_file_path)
        faculties = uni.get_faculties()
        self.assertEqual(len(faculties), 16)

    def test_load_courses(self):
        uni = University("my_uny")
        uni.load_courses(courses_file_path)
        self.assertEqual(len(uni.list_courses()), 173)

    def test_add_course_to_student(self):
        uni = University("my_uny")
        uni.load_courses(courses_file_path)
        uni.add_student("883720579", "Sandie Leifeste", "Arts", "2008", "Rio Branco, Bulgaria, 6196762")
        uni.add_course('883720579', 6000)
        courses = uni.get_courses("883720579")
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0]["id"], 6000)
        self.assertTrue(isinstance(courses[0], dict))

    def test_load_students(self):
        uni = University("my_uny")
        uni.load_courses(courses_file_path)
        uni.load_students(students_file_path)
        students = uni.get_students()
        self.assertEqual(len(students), 20)

    def test_add_student(self):
        uni = University("my_uny")
        uni.load_courses(courses_file_path)
        uni.add_student("883720579", "Sandie Leifeste", "Arts", "2008", "Rio Branco, Bulgaria, 6196762")
        sandie = uni.get_person_by_id("883720579")
        self.assertEqual(sandie.identity_number, "883720579")
        self.assertEqual(sandie.name, "Sandie Leifeste")
        self.assertEqual(sandie.faculty, "Arts")
        courses = uni.get_courses("883720579")
        self.assertEqual(len(courses), 0)
        self.assertEqual(sandie.start_date, "2008")
        self.assertEqual(sandie.address, "Rio Branco, Bulgaria, 6196762")

    def test_change_faculty(self):
        uni = University("my_uny")
        uni.load_courses(courses_file_path)
        uni.add_student("883720579", "Sandie Leifeste", "Arts", "2008", "Rio Branco, Bulgaria, 6196762")
        self.assertEqual(uni.get_number_of_students(), 1)
        self.assertEqual(len(uni.get_students()), 1)
        self.assertEqual(uni.get_students()[0].faculty, "Arts")
        uni.change_faculty("883720579", "Health")
        self.assertEqual(uni.get_number_of_students(), 1)
        self.assertEqual(len(uni.get_students()), 1)
        self.assertEqual(uni.get_students()[0].faculty, "Health")

    def test_get_courses_student(self):
        uni = University("my_uny")
        uni.load_courses(courses_file_path)
        uni.add_student("718929205", "Cindelyn Han", "Agriculture & Natural Resources", "2007",
                        "Shanghai, Egypt, 8440710")
        uni.add_course('718929205', 1100)
        uni.add_course('718929205', 1101)
        uni.add_course('718929205', 1102)
        uni.add_course('718929205', 1103)
        uni.add_course('718929205', 1104)
        uni.add_course('718929205', 1105)
        uni.add_course('718929205', 1106)
        courses = uni.get_courses("718929205")
        self.assertEqual(len(courses), 7)

    def test_load_teachers(self):
        uni = University("my_uny")
        uni.load_courses(courses_file_path)
        uni.load_teachers(teachers_file_path)
        teachers = uni.get_teachers()
        self.assertEqual(len(teachers), 20)

    def test_add_teacher(self):
        uni = University("my_uny")
        uni.load_courses(courses_file_path)
        uni.add_teacher("329622030", "Luci Erskine", "Communications & Journalism", "05/02/2003")
        luci = uni.get_person_by_id("329622030")
        self.assertEqual(luci.identity_number, "329622030")
        self.assertEqual(luci.name, "Luci Erskine")
        self.assertEqual(luci.faculties, ["Communications & Journalism"])
        courses = uni.get_courses("329622030")
        self.assertEqual(len(courses), 0)
        self.assertTrue(isinstance(courses, list))
        self.assertEqual(luci.start_date, "05/02/2003")

    def test_remove_teacher(self):
        uni = University("my_uny")
        uni.load_courses(courses_file_path)
        uni.add_teacher("329622030", "Luci Erskine", "Communications & Journalism", "05/02/2003")
        luci = uni.get_person_by_id("329622030")
        self.assertEqual(luci.identity_number, "329622030")
        uni.add_teacher("971169962", "Rosene Fillbert", "Education", "21/04/2013")
        rosene = uni.get_person_by_id("971169962")
        self.assertEqual(rosene.identity_number, "971169962")
        self.assertEqual(uni.get_number_of_teachers(), 2)
        self.assertEqual(len(uni.get_teachers()), 2)
        uni.remove_person("971169962")
        self.assertEqual(uni.get_number_of_teachers(), 1)
        self.assertEqual(len(uni.get_teachers()), 1)
        self.assertEqual(uni.get_teachers()[0].name, "Luci Erskine")

    def test_get_top_10_students(self):
        uni = University("my_uny")
        uni.load_courses(courses_file_path)
        uni.load_students(students_file_path)
        uni.add_course("645591116", 5200)
        uni.add_course("885227800", 5200)
        uni.add_course("547526213", 3201)
        uni.add_course("894237407", 5301)
        uni.add_course("608551548", 5000)
        uni.add_course("018913426", 5005)
        uni.add_course("822263539", 1901)
        uni.add_course("447113480", 1902)
        uni.add_course("995262665", 2602)
        uni.add_course("970138793", 2601)
        uni.add_course("953020087", 2601)
        top_10_students = uni.get_top_10_students()
        self.assertEqual(top_10_students,
                         ['Livvyy Leonard', 'Lelah Gladstone', 'Jere Cressida', 'Audrie Ivens', 'Minda Sigfrid',
                          'Yvonne Chabot', 'Edee Jorgan', 'Mariann Gino', 'Joeann Keily', 'Iseabal Jalbert'])

    def test_get_students_zip_code(self):
        uni = University("my_uny")
        uni.load_courses(courses_file_path)
        uni.add_student("883720579", "Sandie Leifeste", "Arts", "2008", "Rio Branco, Bulgaria, 6196762")
        zips = set(uni.get_students_zip_code())
        self.assertSetEqual(zips, {"Rio Branco 6196762"})

    def test_get_teachers_from(self):
        uni = University("my_uny")
        uni.load_courses(courses_file_path)
        uni.load_teachers(teachers_file_path)
        teachers_from = uni.get_teachers_from("01/01/1990")
        self.assertEqual(len(teachers_from), 20)


if __name__ == '__main__':
    unittest.main(verbosity=2)
