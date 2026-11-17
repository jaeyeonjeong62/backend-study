#딕셔너리를 리턴하는 함수를 선언

import random

def create_student(name,korean,math,english,science):
    return {
        "name":name,
        "korean":korean,
        "math":math,
        "english":english,
        "science":science
    }

names = ["소은","현종","승준","상훈","서현"]

students = [create_student(name, 
                           random.randint(1,100), 
                           random.randint(1,100),
                           random.randint(1,100),
                           random.randint(1,100)) for name in names]

print(students)