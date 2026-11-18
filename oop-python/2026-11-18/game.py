class GameObject:
    def __init__(self, name, x=0, y=0):
        self.name = name
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def info(self):
        return f"{self.name} ({self.x}, {self.y})"

class HP:
    def __init__(self, max_hp=0):
        self.max_hp = max_hp
        self.current = max_hp

    def damage(self, amount):
        self.current = max(0, self.current - max(0, amount))

    def is_alive(self):
        return self.current > 0

class Weapon:
    def __init__(self, name="", power=0):
        self.name = name
        self.power = power

class Skill:
    def __init__(self, name="", multiplier=0):
        self.name = name
        self.multiplier = multiplier

class Armor:
    def __init__(self, name="", defense=0):
        self.name = name
        self.defense = defense

class Character(GameObject):
    def __init__(self, name, max_hp, weapon, skill, armor):
        super().__init__(name=name)
        self.hp = max_hp
        self.weapon = weapon
        self.skill = skill
        self.armor = armor

    def attack(self):
        return self.weapon.power

    def use_skill(self):
        return int(self.weapon.power * self.skill.multiplier)

    def take_damage(self, amount):
        self.hp.damage(amount - self.armor.defense)
        return amount - self.armor.defense

    def change_weapon(self, weapon):
        self.weapon = weapon

class Warrior(Character):
    def __init__(self, name):
        super().__init__(name=name, 
                         max_hp=HP(150), 
                         weapon=Weapon("롱소드",20), 
                         skill=Skill("강타",1.5), 
                         armor=Armor("판금갑옷",10))

class Wizard(Character):
    def __init__(self, name):
        super().__init__(name=name, 
                         max_hp=HP(90), 
                         weapon=Weapon("지팡이",8), 
                         skill=Skill("파이어볼",4.0), 
                         armor=Armor("로브",2))


w = Warrior("아서")
z = Wizard("멀린")

print(w.attack(), w.use_skill(), z.use_skill())

print(w.take_damage(25), w.hp.current)

print(z.take_damage(25), z.hp.current), w.change_weapon(Weapon("전투도끼", 30))

print(w.attack(), w.use_skill())