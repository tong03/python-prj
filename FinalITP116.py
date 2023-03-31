# NAME: Tri Tong
# ID: 1373376919
# DATE: 2022-12-01
# DESCRIPTION: Create a major database from the major requirements file and compare with user's coursework
# to make class recommendations for the intended major

from typing import IO, Dict, List


# make a Student class to hold their coursework and use class methods for displaying purposes
class Student:
    def __init__(self, full_name: str):
        self.full_name = full_name
        # courses attribute is empty and would be loaded once coursework file is ran
        self.courses = []

    # display the student's full name
    def display_name(self) -> str:
        return f"Name: {self.full_name}"


# open the desired data file and return its content
def open_file(file_type: str) -> IO:
    # user input of the data file name
    file_name = input(f'Enter the {file_type} file name: ')
    # set file_pointer as None to start loop initially
    file_pointer = None
    # use try-except block to open file in case run time error
    while file_pointer is None:
        try:
            # attempt to open input file name in read mode
            file_pointer = open(file_name, "r")
        except IOError:
            # if error occur display message and prompt input again before re-checking loop condition
            print(f"\nError occurred while attempting to open '{file_name}' file.\n"
                  f"Please make sure that the file name is correct and that the file exist.")
            file_name = input(f'Enter the {file_type} name: ')
    return file_pointer


# read major requirements data and process it into a nested dictionary
def create_database(fp: IO) -> Dict[str, Dict[str, int]]:
    # create the big dictionary hosting all the majors
    database = {}
    # skip the first line, which is the referenced formatting of the data
    fp.readline()
    # read second line to start while loop
    line_pointer = fp.readline()
    # run loop as long as line pointer is nothing and at least 1
    while line_pointer is not None and len(line_pointer) >= 1:
        # check if the line is a major name indicated by ">" at the start of the line
        if line_pointer[0] == ">":
            # set major name to the rest of the line
            major = line_pointer[1:].strip()
            # turn major name to lower case
            major = major.lower()
            # create nested major dictionary to hold courses for that major [dictionary key]
            database[major] = {}
            # since last line was a major name line, following lines would be courses for that major
            line_pointer = fp.readline()
            # check that the line is a course line indicated by "-" at the start of the line
            # also have to check that the line has at least 1 character to check the second condition
            while len(line_pointer) >= 1 and line_pointer[0] == "-":
                # turn line into list with 2 elements, separating between the comma
                course = line_pointer[1:].split(',')
                # set course_id to equal the first element of list
                course_id = course[0].strip()
                # set units to equal second element of list
                units = course[1].strip()
                # add the course_id into the major's course dictionary
                database[major][course_id] = int(units)
                # read the next line to loop back and re-check the loop condition
                line_pointer = fp.readline()
    return database


# read student's coursework data and process it into a list for that student instance
def student_courses(fp: IO) -> List[Student]:
    # list containing student class
    student_profile = []
    # first line of file is student full name
    full_name = fp.readline().strip()
    # second line is total classes taken for the student
    size = int(fp.readline())
    # initialize and add student instance to the list of student class
    student_profile.append(Student(full_name))
    # iterate over the total classes to add into the student's courses attribute
    for i in range(size):
        # read new line and remove trailing characters
        line = fp.readline().strip()
        # set course to the line starting from index 1 to skip "-"
        course = line[1:]
        # add class to student's courses attribute, reference first index because only 1 student
        student_profile[0].courses.append(course)

    return student_profile


# prompt user for intended major, separate function because called multiple times
def ask_major() -> str:
    # User input prompt asking for desired major, lowercase their input to resolve case-sensitive issues
    major = input("Enter your intended major from (don't include space): \n"
                  "-Lifespan Health\n"
                  "-Human Development and Aging\n").lower()
    # check if the input is human development and aging since it has 2 tracks
    if major == "humandevelopmentandaging":
        # create the 2 tracks into a track_list
        track_list = ("socialscience", "healthscience")
        # prompt user to choose the track they want, not case-sensitive
        track = input("Enter the track you want for this major (no space):\n"
                      "-Social Science\n"
                      "-Health Science\n").lower()
        # loop to keep prompting if their answer isn't the 2 given tracks
        while track not in track_list:
            # give user feedback
            print("Please enter a proper track.")
            # prompt user to choose again
            track = input("Enter the track you want for this major (no space):\n"
                          "-Social Science\n"
                          "-Health Science\n").lower()
        # check if track chosen is social science
        if track == "socialscience":
            # set track to ss for abbreviation
            track = "ss"
            # add abbreviation to end of major --> correspond with the major name format in database
            major += track
        else:
            # set track to hs for abbreviation of health science
            track = "hs"
            # add abbreviation to end of major
            major += track
    return major


# return a dictionary with values 1 if the course is taken or 0 if not yet taken
def compare_courses(major_database: Dict[str, Dict[str, int]],
                    student_profile: List[Student]) -> (Dict[str, int], str):
    # create empty dictionary for comparison
    schedule = {}
    # run ask_major function and set it to major
    major = ask_major()
    # keep loop if nothing in the schedule, try-except block in case major doesn't exist in database
    while len(schedule) == 0:
        try:
            # attempt to iterate over the courses in the major dictionary of the database
            for course in major_database[major]:
                # check if course is also in student's coursework
                if course in student_profile[0].courses:
                    # set the course to value 1 in the comparison dictionary if it is
                    schedule[course] = 1
                else:
                    # set the course to value 0 in comparison dictionary if it isn't
                    schedule[course] = 0
        except KeyError:
            # except block give user feedback
            print(f"The major {major} doesn't exist in the database!\n"
                  f"Please try again with a valid major.\n")
            # prompt user for major input again to be executed again in try block
            major = ask_major()

    return schedule, major


# return a list of courses required to fulfill the major based on compare_courses
def course_req(schedule: Dict[str, int], database: Dict[str, Dict[str, int]], major: str) -> Dict[str, int]:
    # create a blank dictionary to hold all required courses
    req_suggested = {}
    # iterate over the compared dictionary from compare_courses()
    for course in schedule:
        # check if course is not taken yet --> indicate by a value 0
        if schedule[course] == 0:
            # add the course into the required dictionary and its value would be the course units
            req_suggested[course] = database[major][course]
    return req_suggested


# return a list of courses completed towards fulfilling the major based on compare_courses
def course_comp(schedule: Dict[str, int], database: Dict[str, Dict[str, int]], major: str) -> Dict[str, int]:
    # create blank dictionary to hold all completed courses
    req_completed = {}
    # iterate over compared dictionary from compare_courses()
    for course in schedule:
        # check if course is taken --> indicate by value 1
        if schedule[course] == 1:
            # add course into completed dictionary and its value would be the course units
            req_completed[course] = database[major][course]
    return req_completed


# calculate the total units of the major, coursework needed, and coursework completed
def units_calc(suggested: Dict[str, int],
               completed: Dict[str, int],
               database: Dict[str, Dict[str, int]], major: str) -> (int, int, int):
    # define 3 counter variables to start incrementing with their respective units
    major_u = 0
    required_u = 0
    completed_u = 0
    # iterate over the courses in the required courses dictionary
    for i in suggested:
        # add up the course units
        required_u += suggested[i]
    # iterate over the courses in completed courses dictionary
    for j in completed:
        # add up the course units
        completed_u += completed[j]
    # iterate over the courses in major dictionary
    for k in database[major]:
        # add up the course units
        major_u += database[major][k]

    return major_u, required_u, completed_u


# display the user's processed course information in a formatted way
def display_courses(suggested: Dict[str, int],
                    completed: Dict[str, int],
                    major: str, s_profile: List[Student],
                    major_u: int, required_u: int, completed_u: int) -> None:
    # print out user's information and their progress towards fulfilling major's core requirements
    print(f"\n{s_profile[0].display_name()} | Intended Major: {major} | Units: {major_u}")
    print(f"To fulfill the core major requirements, you still need {required_u} units:")
    print(f'You have completed {completed_u} units towards the requirements:')
    print(f"Required courses: {required_u} units")
    # iterate over the required course dictionary
    for course in suggested:
        # check if the value of the course is 12/20, which would print out a different message
        if suggested[course] == 12 or suggested[course] == 20:
            print(f'-{course}: {suggested[course]} units total (300/400 level courses)')
        # otherwise print the course in the dictionary and its corresponding units
        else:
            print(f'-{course}: {suggested[course]} units')
    print(f"Relevant courses completed: {completed_u} units")
    # iterate over the completed course dictionary
    for classes in completed:
        # print course in the dictionary and its corresponding units
        print(f'-{classes}: {completed[classes]} units')


# compile other functions and run the program
def main():
    # open the major requirements file
    requirements = open_file("major requirements")
    # open the courses taken file
    taken = open_file("student coursework")
    # using the major requirements file, create a database of course requirements
    major_data = create_database(requirements)
    # using the user's course taken file, create a student class object instance with list of courses
    # taken as attribute
    course_done = student_courses(taken)
    # compare the major database and courses taken from student instance to return the schedule plan
    # of courses for a major, as well as returning the intended major
    schedule, major = compare_courses(major_data, course_done)
    # based on the schedule course plan, make dictionary of suggested courses
    suggest = course_req(schedule, major_data, major)
    # based on schedule course plan, make dictionary of completed courses
    complete = course_comp(schedule, major_data, major)
    # calculate the total credits for the major, suggested course, and completed course
    major_u, required_u, completed_u = units_calc(suggest, complete, major_data, major)
    # print out the formatted course suggestions from the processed user input
    display_courses(suggest, complete, major, course_done, major_u, required_u, completed_u)
    # close the two files opened earlier
    requirements.close()
    taken.close()


# only run content of main() function if file executed as script -> top-level code environment
if __name__ == "__main__":
    main()
