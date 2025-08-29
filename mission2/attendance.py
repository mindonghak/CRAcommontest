from abc import ABC, abstractmethod


class FileReader:
    @staticmethod
    def read_file(file_name):
        content = ""
        try:
            with open(file_name, encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print("파일을 찾을 수 없습니다.")
        return content

class DayOfWeek:
    @staticmethod
    def is_wednesday(day_of_week):
        return day_of_week == "wednesday"

    @staticmethod
    def is_weekend(day_of_week):
        return day_of_week == "saturday" or day_of_week == "sunday"

class Points:
    @staticmethod
    def get_points_of_day(day_of_week):
        points_add = 1
        if DayOfWeek.is_wednesday(day_of_week):
            points_add = 3
        elif DayOfWeek.is_weekend(day_of_week):
            points_add = 2
        return points_add


class GradeGenerator:
    @staticmethod
    def make_grade(points):
        if points>= 50:
            grade = Gold()
        elif points>= 30:
            grade = Silver()
        else:
            grade = Normal()
        return grade

class Grade(ABC):
    @abstractmethod
    def print_grade(self):
        pass

class Gold(Grade):
    def print_grade(self):
        print("GOLD")

class Silver:
    def print_grade(self):
        print("SILVER")

class Normal:
    def print_grade(self):
        print("NORMAL")

class UserInfo:
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.wednesday = 0
        self.weekend = 0
        self.grade = None

    def special_day_count(self, day_of_week):
        if DayOfWeek.is_wednesday(day_of_week):
            self.wednesday += 1
        if DayOfWeek.is_weekend(day_of_week):
            self.weekend += 1

    def process_bonus_points(self):
        if self.wednesday > 9:
            self.points += 10
        if self.weekend > 9:
            self.points += 10

    def make_grade(self):
        self.grade = GradeGenerator.make_grade(self.points)

    def print_grade(self):
        print(f"NAME : {self.name}, POINT : {self.points}, GRADE : ", end="")
        self.grade.print_grade()

    def print_removed_player(self):
        if isinstance(self.grade, Normal)  and self.wednesday == 0 and self.weekend == 0:
            print(self.name)


class UserDatabase:
    def __init__(self):
        self.user_dictionary = {}

    def process_user_input_from_content(self, content):
        lines = content.split("\n")
        for line in lines:
            user_info = line.strip().split()
            if len(user_info) == 2:
                user_name, user_day = user_info
                self.process_user_input(user_name, user_day)

    def process_user_input(self, user_name, day_of_week):
        if user_name not in self.user_dictionary:
            self.user_dictionary[user_name] = UserInfo(user_name)
        user = self.user_dictionary[user_name]
        user.special_day_count(day_of_week)
        user.points += Points.get_points_of_day(day_of_week)



class Attendance:
    def __init__(self):
        self.user_database = UserDatabase()

    def update_user_info(self, filename):
        content = FileReader.read_file(filename)
        self.user_database.process_user_input_from_content(content)


    def update_points_and_grades(self):
        for user in self.user_database.user_dictionary.values():
            user.process_bonus_points()
        for user in self.user_database.user_dictionary.values():
            user.make_grade()

    def print_results(self):
        for user in self.user_database.user_dictionary.values():
            user.print_grade()
        print("\nRemoved player")
        print("==============")
        for user in self.user_database.user_dictionary.values():
            user.print_removed_player()

if __name__ == "__main__":
    attendance = Attendance()
    attendance.update_user_info("attendance_weekday_500.txt")
    attendance.update_points_and_grades()
    attendance.print_results()