# 학생 리스트 (Students)를 선언해 주세요. 5명의 학생정보를 아래 속성으로 저장하세요
# 학생은 이름(name), 국어(korean),영어(english),수학(math),과학(science)속성갖는다

import random

students = []

names = ["재연", "소은", "예원", "서현", "상훈"]

for name in names:
    students.append({"name":name, "korean":0, "english":0, "math":0, "science":0})

for num in range(5):
    for key in list(students[num].keys())[1:]:
        students[num][key] = random.randint(1,100)

print(students)