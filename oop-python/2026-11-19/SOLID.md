# 클래스 설계 5원칙 S.O.L.I.D

## 0.한눈에 보기

|약자|원칙|한 줄 요약|위반 시 증상|
|---|---|---|---|
|S|SRP:단일 책임 원칙(Single Responsible Principle)|클래스를 바꿀 이유는 하나뿐이어야 한다|한 클래스가 계산도, 출력도, 저장도 함|
|O|OCP:개방-폐쇄 원칙(Open-Closed Principle)|확장에는 열려 있고 수정에는 닫혀 있어야 한다|기능 추가마다 `if/elif`를 늘림|
|L|LSP:리스코프 치환 원칙(Liskov Substitution Principle)|자식 객체는 부모 객체 자리에 그대로 대체될 수 있어야 한다|자식으로 바꾸면 결과가 이상해짐|
|I|ISP:인터페이스 분리 원칙(Interface Segregation Principle)|쓰지 않는 메서드 구현을 강요하지 않는다|`raise NotImplementedError`로 때우는 메서드|
|D|DIP:의존성 역전 원칙(Dependency Inversion Principle)|구체 클래스가 아니라 추상화에 의존한다|클래스 안에서 다른 구체 클래스를 직접 생성|

**파이썬의 "인터페이스"**

파이썬에는 Java의 `interface` 키워드가 없다. 대신 `abc` 모듈의 추상 클래스로 "이 메서드는 반드시 구현하라"는 약속을 만든다.

---

## 1.S: 단일 책임 원칙(SRP)

```python
import json
import math

# [위반]: 계산과 출력 형식을 한 클래스가 모두 책임
class AreaCalculatorBad:
    def __init__(self, shapes):
        self.shapes = shapes

    def sum(self):
        return sum(s.area() for s in self.shapes)

    def output_html(self):
        return f"<h1>넓이 합: {self.sum():.2f}</h1>"
    # JSON, CSV가 필요해지면 계산 클래스를 계속 수정해야 함


# [개선]: 계산 책임 / 출력 책임 분리
class Square:
    def __init__(self, length):
        self.length = length
    def area(self):
        return self.length ** 2

class Circle:
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return math.pi * self.radius ** 2

class AreaCalculator:                 # 책임 1: 넓이 합 계산
    def __init__(self, shapes):
        self.shapes = shapes
    def sum(self):
        return sum(s.area() for s in self.shapes)

class SumCalculatorOutputter:        # 책임 2: 결과 출력 형식
    def __init__(self, calculator):
        self.calculator = calculator
    def html(self):
        return f"<h1>넓이 합: {self.calculator.sum():.2f}</h1>"
    def json(self):
        return json.dumps({"sum": round(self.calculator.sum(), 2)})

calc = AreaCalculator([Circle(2), Square(5), Square(6)])
out = SumCalculatorOutputter(calc)
print(out.html())
print(out.json())
```

---

## 2.O: 개방-폐쇄 원칙(OCP)

```python
import math
from abc import ABC, abstractmethod

# [위반]: 새 도형이 생길 때마다 계산기 코드를 수정해야 함
class AreaCalculatorBad:
    def __init__(self, shapes):
        self.shapes = shapes
    def sum(self):
        total = 0
        for s in self.shapes:
            if s["type"] == "square":
                total += s["length"] ** 2
            elif s["type"] == "circle":
                total += math.pi * s["radius"] ** 2
            # 삼각형 추가? -> elif를 또 써야 함 (수정에 열려 있음)
        return total


# [개선]: 도형이 스스로 넓이를 계산 -> 계산기는 수정 없이 확장
class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

class Square(Shape):
    def __init__(self, length):
        self.length = length
    def area(self):
        return self.length ** 2

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return math.pi * self.radius ** 2

class Triangle(Shape):               # 새 도형 추가: 기존 코드 수정 0줄
    def __init__(self, base, height):
        self.base, self.height = base, height
    def area(self):
        return self.base * self.height / 2

class AreaCalculator:
    def __init__(self, shapes):
        self.shapes = shapes
    def sum(self):
        return sum(s.area() for s in self.shapes)

print(round(AreaCalculator([Square(2), Circle(1), Triangle(4, 3)]).sum(), 2))

try:
    class Hexagon(Shape):            # area()를 구현하지 않으면?
        pass
    Hexagon()
except TypeError as e:
    print("TypeError:", e)
```

---

## 3.L: 리스코프 치환 원칙(LSP)

```python
# [위반]: 정사각형은 직사각형이다(수학적으로)? -> 코드에서는 치환 불가
class Rectangle:
    def __init__(self, w, h):
        self._w, self._h = w, h
    def set_width(self, w):
        self._w = w
    def set_height(self, h):
        self._h = h
    def area(self):
        return self._w * self._h

class Square(Rectangle):
    def __init__(self, size):
        super().__init__(size, size)
    def set_width(self, w):            # 정사각형 유지를 위해 동작을 바꿈
        self._w = self._h = w
    def set_height(self, h):
        self._w = self._h = h

def resize_and_check(rect: Rectangle):
    rect.set_width(5)
    rect.set_height(4)
    return rect.area()                 # 사용하는 쪽은 20을 기대

print("Rectangle:", resize_and_check(Rectangle(1, 1)))
print("Square   :", resize_and_check(Square(1)))   # 16 -> 기대 깨짐


# [개선]: 공통 상위 타입은 '넓이를 가진다'까지만 약속
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self): ...

class Rect(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h
    def area(self):
        return self.w * self.h

class Sq(Shape):
    def __init__(self, size):
        self.size = size
    def area(self):
        return self.size ** 2

# 원문 예제: 반환 타입이 같아야 치환 가능
class AreaCalculator:
    def __init__(self, shapes):
        self.shapes = shapes
    def sum(self):
        return sum(s.area() for s in self.shapes)        # 항상 숫자 반환

class VolumeCalculator(AreaCalculator):
    def sum(self):
        return super().sum() * 2                        # [O] 숫자 반환 유지
        # return [super().sum()]                        # [X] 리스트 반환 -> 부모 대체 불가

shapes = [Rect(5, 4), Sq(4)]
for calc in (AreaCalculator(shapes), VolumeCalculator(shapes)):
    print(type(calc).__name__, "->", f"{calc.sum():,}")  # 둘 다 숫자로 다룸
```

---

## 4.I: 인터페이스 분리 원칙(ISP)

```python
from abc import ABC, abstractmethod

# [위반]: 모든 도형에 volume()을 강요
class ShapeInterfaceBad(ABC):
    @abstractmethod
    def area(self): ...
    @abstractmethod
    def volume(self): ...

class SquareBad(ShapeInterfaceBad):
    def __init__(self, l):
        self.l = l
    def area(self):
        return self.l ** 2
    def volume(self):                  # 2차원 도형인데 억지로 구현
        raise NotImplementedError("정사각형은 부피가 없음")


# [개선]: 작은 인터페이스로 분리 후 필요한 것만 조합
class ShapeInterface(ABC):
    @abstractmethod
    def area(self): ...

class ThreeDimensionalShapeInterface(ABC):
    @abstractmethod
    def volume(self): ...

class ManageShapeInterface(ABC):       # 계산기가 의존할 공통 인터페이스
    @abstractmethod
    def calculate(self): ...

class Square(ShapeInterface, ManageShapeInterface):
    def __init__(self, l):
        self.l = l
    def area(self):
        return self.l ** 2
    def calculate(self):
        return self.area()

class Cuboid(ShapeInterface, ThreeDimensionalShapeInterface, ManageShapeInterface):
    def __init__(self, w, h, d):
        self.w, self.h, self.d = w, h, d
    def area(self):                    # 겉넓이
        return 2 * (self.w * self.h + self.h * self.d + self.d * self.w)
    def volume(self):
        return self.w * self.h * self.d
    def calculate(self):
        return self.volume()

for s in [Square(3), Cuboid(2, 3, 4)]:
    print(type(s).__name__,
          "| 3D?", isinstance(s, ThreeDimensionalShapeInterface),
          "| calculate =", s.calculate())
```

---

## 5.D: 의존성 역전 원칙(DIP)

> "Entities must depend on abstractions, not on concretions. High-level modules must not depend on low-level modules, but they should depend on abstractions."
고수준 모듈은 저수준 모듈에 의존하면 안 되며, 둘 다 추상화에 의존해야 한다.
> 

**문제 상황**: 비즈니스 로직(`PasswordReminder`, 고수준)이 특정 DB(`MySQLConnection`, 저수준)를 **직접 생성**합니다. DB를 바꾸거나 테스트용 가짜 DB를 넣으려면 비즈니스 로직을 수정해야 합니다.

**해결**: `DBConnectionInterface`라는 추상화를 만들고, 실제 객체는 **바깥에서 주입**(Dependency Injection)합니다.

```python
from abc import ABC, abstractmethod

# [위반]: 상위 모듈이 구체 클래스(MySQL)에 직접 의존
class MySQLConnectionBad:
    def connect(self):
        return "MySQL 연결"

class PasswordReminderBad:
    def __init__(self):
        self.db = MySQLConnectionBad()   # DB를 바꾸려면 이 클래스를 수정해야 함


# [개선]: 상위·하위 모듈 모두 추상화(인터페이스)에 의존
class DBConnectionInterface(ABC):
    @abstractmethod
    def connect(self) -> str: ...

class MySQLConnection(DBConnectionInterface):
    def connect(self):
        return "MySQL 연결"

class PostgreSQLConnection(DBConnectionInterface):
    def connect(self):
        return "PostgreSQL 연결"

class FakeConnection(DBConnectionInterface):      # 테스트용 가짜 DB
    def connect(self):
        return "테스트용 가짜 연결"

class PasswordReminder:
    def __init__(self, db: DBConnectionInterface):   # 의존성 주입(DI)
        self.db = db
    def remind(self, user):
        return f"[{self.db.connect()}] {user}님께 비밀번호 재설정 메일 발송"

for db in (MySQLConnection(), PostgreSQLConnection(), FakeConnection()):
    print(PasswordReminder(db).remind("kim"))
```

