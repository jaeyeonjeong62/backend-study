class Salary:
    def __init__(self, base_pay, bonus, overtime):
        self.base_pay = base_pay
        self.bonus = bonus
        self.overtime = overtime

    def get_total(self):
        return self.base_pay+self.bonus+self.overtime

    def get_tax(self):
        return self.get_total()*0.1

    def get_net(self):
        return self.get_total()-self.get_tax()

class WorkHistory:
    def __init__(self, company, position, start_year, end_year):
        self.company = company
        self.position = position
        self.start_year = start_year
        self.end_year = end_year

    def get_years(self):
        return self.end_year - self.start_year

    def to_string(self):
        return "{}\t{}\t{}".format(self.company,
                            self.position,
                            self.get_years())

class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.dept = ""
        self.salary = salary
        self.histories = []

    def add_history(self, history):
        return self.histories.append(history)

    def get_career(self):
        sum = 0
        
        for year in self.histories:
            sum += year.get_years()
        return sum

    def to_string(self):
        return "{}\t{}\t{}".format(self.name,
                                   self.dept,
                                   str(self.get_career())+"년",
                                   self.salary.get_net())

class Company:
    def __init__(self, name):
        self.name = name
        self.departments = []

    def add_department(self,department):
        self.departments.append(department)

    def get_employee_count(self):
        cnt = 0
        for department in self.departments:
            cnt += len(department.employees)
        return cnt

    def get_payroll(self):
        sum = 0
        for department in self.departments:
            sum += department.get_payroll()
        return sum

    def print_report(self):
        for department in self.departments:
            department.print_members()

class Department:
    def __init__(self, name):
        self.name = name
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)
        employee.dept = self.name

    def get_payroll(self):
        sum = 0
        for employee in self.employees:
            sum += employee.salary
        return sum

    def get_avg_career(self):
        sum = 0
        for employee in self.employees:
            sum += employee.get_career()
        avg = sum / len(self.employees)
        return avg

    def print_members(self):
        for employee in self.employees:
            print(employee.to_string())



d1 = Department("개발팀")
d1.add_employee(Employee("김민수", Salary(300, 50, 20)))
d1.add_employee(Employee("이지은", Salary(320, 40, 30)))

d2 = Department("인사팀")
d2.add_employee(Employee("박준호", Salary(280, 60, 10)))

d3 = Department("영업팀")

e4=Employee("최서연", Salary(350, 30, 25))

d3.add_employee(e4)

works = [WorkHistory("데이터랩", "사원", 2000, 2004),
        WorkHistory("클라우드원", "사원", 2004, 2008),
        WorkHistory("넥스트AI", "사원", 2009, 2012)]

e4.add_history(works[0])
e4.add_history(works[1])
e4.add_history(works[2])

d4 = Department("마케팅팀")
d4.add_employee(Employee("한도윤", Salary(300, 70, 15)))

com = Company("블루웨이브")
com.add_department(d1)
com.add_department(d2)
com.add_department(d3)
com.add_department(d4)

com.print_report()