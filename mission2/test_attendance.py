import pytest

from attendance import *
from unittest.mock import patch

def test_read_file_success(tmp_path):
    file_path = tmp_path / "test.txt"
    test_context = "Hello World"
    file_path.write_text(test_context)
    content = FileReader.read_file(str(file_path))
    assert content == test_context

def test_read_file_fail(capsys):
    content = FileReader.read_file("abc.txt")
    captured = capsys.readouterr()
    assert content == ""
    assert "파일을 찾을 수 없습니다." in captured.out


def test_day_of_week():
    assert DayOfWeek.is_wednesday("wednesday")
    assert not DayOfWeek.is_wednesday("monday")
    assert DayOfWeek.is_weekend("saturday")
    assert DayOfWeek.is_weekend("sunday")
    assert not DayOfWeek.is_weekend("monday")

def test_points():
    assert Points.get_points_of_day("monday") == 1
    assert Points.get_points_of_day("tuesday") == 1
    assert Points.get_points_of_day("wednesday") == 3
    assert Points.get_points_of_day("thursday") == 1
    assert Points.get_points_of_day("friday") == 1
    assert Points.get_points_of_day("saturday") == 2
    assert Points.get_points_of_day("sunday") == 2

def test_grade_generator():
    assert isinstance(GradeGenerator.make_grade(50), Gold)
    assert isinstance(GradeGenerator.make_grade(30), Silver)
    assert isinstance(GradeGenerator.make_grade(10), Normal)

def test_grade(capfd):
    grade = Gold()
    grade.print_grade()
    out, err = capfd.readouterr()
    assert "GOLD" in out
    grade = Silver()
    grade.print_grade()
    out, err = capfd.readouterr()
    assert "SILVER" in out
    grade = Normal()
    grade.print_grade()
    out, err = capfd.readouterr()
    assert "NORMAL" in out


def test_create_user_info():
    user_info = UserInfo("Jason")
    assert user_info.name == "Jason"
    assert user_info.points == 0
    assert user_info.weekend == 0
    assert user_info.wednesday == 0
    assert user_info.grade == None

def test_special_day_count():
    user_info = UserInfo("Jason")
    user_info.special_day_count("wednesday")
    assert user_info.wednesday == 1
    user_info.special_day_count("saturday")
    assert user_info.weekend == 1
    user_info.special_day_count("sunday")
    assert user_info.weekend == 2

def test_process_bonus_points():
    user_info = UserInfo("Jason")
    user_info.process_bonus_points()
    assert user_info.points == 0
    user_info.wednesday = 10
    user_info.process_bonus_points()
    assert user_info.points == 10
    user_info.weekend = 10
    user_info.process_bonus_points()
    assert user_info.points == 30

def test_make_grade():
    user_info = UserInfo("Jason")
    user_info.points = 10
    user_info.make_grade()
    assert isinstance(user_info.grade, Normal)
    user_info.points = 30
    user_info.make_grade()
    assert isinstance(user_info.grade, Silver)
    user_info.points = 50
    user_info.make_grade()
    assert isinstance(user_info.grade, Gold)

def test_print_grade(capfd):
    user_info = UserInfo("Jason")
    user_info.make_grade()
    user_info.print_grade()
    out, err = capfd.readouterr()
    assert "NAME : Jason, POINT : 0, GRADE : NORMAL" in out

def test_print_removed_player(capfd):
    user_info = UserInfo("Jason")
    user_info.make_grade()
    user_info.print_removed_player()
    out, err = capfd.readouterr()
    assert "Jason" in out

def test_userdata():
    user_database = UserDatabase()
    assert user_database.user_dictionary == {}

    content = "Jason monday"

    user_database.process_user_input_from_content(content)
    user = user_database.user_dictionary["Jason"]
    assert user.name == "Jason"
    assert user.points == 1

def test_attendance(tmp_path, capfd):
    attendance = Attendance()
    file_path = tmp_path / "test.txt"
    test_context = "JASON sunday"
    file_path.write_text(test_context)
    attendance.update_user_info(str(file_path))
    assert attendance.user_database.user_dictionary["JASON"].name == "JASON"
    assert attendance.user_database.user_dictionary["JASON"].points == 2

    attendance.update_points_and_grades()
    assert isinstance(attendance.user_database.user_dictionary["JASON"].grade, Normal)

    attendance.print_results()
    out, err = capfd.readouterr()
    assert "NORMAL" in out
    assert "Removed player" in out
    assert "JASON" in out
