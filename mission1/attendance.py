from typing import get_origin

hash_name_to_id = {}
number_of_user = 0

points = [0] * 100
grade = [0] * 100
hash_id_to_name = [''] * 100
wednesday = [0] * 100
weekend = [0] * 100

def main():
    content = read_file()
    process_user_input_from_content(content)
    process_bonus_points()
    make_grade()
    print_grade()
    print_removed_player()

def read_file():
    try:
        with open("attendance_weekday_500.txt", encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
    return content

def process_user_input_from_content(content):
    lines = content.split("\n")
    for line in lines:
        user_info = line.strip().split()
        if len(user_info) == 2:
            user_name, user_day = user_info
            process_user_input(user_name, user_day)

def process_bonus_points():
    for i in range(1, number_of_user + 1):
        if wednesday[i] > 9:
            points[i] += 10
        if weekend[i] > 9:
            points[i] += 10

def make_grade():
    for i in range(1, number_of_user + 1):
        if points[i] >= 50:
            grade[i] = 1
        elif points[i] >= 30:
            grade[i] = 2
        else:
            grade[i] = 0

def print_grade():
    for i in range(1, number_of_user + 1):
        print(f"NAME : {hash_id_to_name[i]}, POINT : {points[i]}, GRADE : ", end="")
        if grade[i] == 1:
            print("GOLD")
        elif grade[i] == 2:
            print("SILVER")
        else:
            print("NORMAL")

def print_removed_player():
    print("\nRemoved player")
    print("==============")
    for i in range(1, number_of_user + 1):
        if grade[i] not in (1, 2) and wednesday[i] == 0 and weekend[i] == 0:
            print(hash_id_to_name[i])

def process_user_input(user_name, day_of_week):
    global number_of_user
    if is_new_user(user_name):
        add_user(user_name)
    user_id = get_user_id(user_name)
    special_day_count(day_of_week, user_id)
    points[user_id] += get_points_of_day(day_of_week)

def is_new_user(user_name):
    return user_name not in hash_name_to_id

def add_user(user_name):
    global number_of_user
    number_of_user += 1
    hash_name_to_id[user_name] = number_of_user
    hash_id_to_name[number_of_user] = user_name

def get_user_id(user_name):
    return hash_name_to_id[user_name]

def special_day_count(day_of_week, user_id):
    if day_of_week == "wednesday":
        wednesday[user_id] += 1
    if day_of_week == "saturday" or day_of_week == "sunday":
        weekend[user_id] += 1

def get_points_of_day(day_of_week):
    points_add = 1
    if is_wednesday(day_of_week):
        points_add = 3
    elif is_weekend(day_of_week):
        points_add = 2
    return points_add

def is_wednesday(day_of_week):
    return day_of_week == "wednesday"

def is_weekend(day_of_week):
    return day_of_week == "saturday" or day_of_week == "sunday"

if __name__ == "__main__":
    main()