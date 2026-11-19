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

    def heal_full(self):
        self.current = self.max_hp

class Item:
    def __init__(self, name):
        self.name = name

class Monster(GameObject):
    def __init__(self, name, hp, element, exp_reward, drop=None):
        self.name = name
        self.hp = hp
        self.element = element
        self.exp_reward = exp_reward
        self.drop = drop

class Slime(Monster):
    def __init__(self):
        super().__init__(name="슬라임",
                         hp=HP(40),
                         element="풀",
                         exp_reward=60,
                         drop=Weapon(name="물의 창", element="물", power=25))

class Golem(Monster):
    def __init__(self):
        super().__init__(name="골렘",
                         hp=HP(120),
                         element="풀",
                         exp_reward=90,
                         drop=Item("강화석"))

class Dragon(Monster):
    def __init__(self):
        super().__init__(name="보스",
                         hp=HP(300),
                         element="불",
                         exp_reward=500)

class Weapon(Item):
    def __init__(self, name, element="", power=0, enhance=0):
        super().__init__(name=name)
        self.power = power
        self.element = Element(element)
        self.enhance = enhance

    def upgrade(self):
        self.enhance += 1
        self.power += 5

    def __str__(self):
        prefix = f"+{self.enhance} " if self.enhance else ""
        return f"{prefix}{self.name}[{self.element.name}]"

class Element:
    def __init__(self, name):
        self.name = name
    def multiplier(self, target):
        if target.element == self.name:
            return 1.0
        elif (target.element == "풀" and self.name == "불") or\
            (target.element == "물" and self.name == "풀") or\
            (target.element == "불" and self.name == "물"):
            return 2.0
        else:
            return 0.5

class Level:
    def __init__(self, character, level=1, exp=0):
        self.level = level
        self.exp = exp
        self.character = character
    def need(self):
        exp_need = self.level * 100
        return exp_need
    def gain(self, amount):
        self.exp += amount
        cnt = 0

        while self.exp >= self.need():
            self.exp -= self.need()
            self.level += 1
            cnt += 1
            self.character.hp.max_hp += 20
            self.character.hp.heal_full()

        return cnt
        
class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
    def add(self, item):
        if self.capacity == len(self.items):
            return False
        self.items.append(item)
        return True
    def take(self, name):
        for item in self.items:
            if item.name==name:
                self.items.remove(item)
                return item
        return None


class Skill:
    def __init__(self, name="", multiplier=0):
        self.name = name
        self.multiplier = multiplier

class Armor:
    def __init__(self, name="", defense=0):
        self.name = name
        self.defense = defense

class Character(GameObject):
    def __init__(self, name, max_hp, weapon, level, inventory=5):
        super().__init__(name=name)
        self.hp = max_hp
        self.weapon = weapon
        self.level = level
        self.inventory = Inventory(inventory)

    def attack(self, target):
        log = []
        if not target.hp.is_alive():
            return log

        mul = self.weapon.element.multiplier(target)
        damage = int(self.weapon.power * mul)
        target.hp.damage(damage)
        log.append(
            f"{self.name}의 {self.weapon} 공격! "
            f"{target.name}에게 {damage} 피해 (x{mul})"
        )

        if not target.hp.is_alive():
            cnt = self.level.gain(target.exp_reward)
            log.append(f"{target.name} 처치! EXP +{target.exp_reward}")

            if cnt > 0:
                log.append(
                    f"레벨 업! Lv.{self.level.level} "
                    f"(최대 HP {self.hp.max_hp})"
                )

            if target.drop is not None and self.inventory.add(target.drop):
                log.append(f"'{target.drop.name}' 획득!")

        return log

    def equip(self, name):
        item = self.inventory.take(name)
        if item is None:
            return False

        self.inventory.add(self.weapon)
        self.weapon = item
        return True

    def upgrade_weapon(self):
        if self.inventory.take("강화석") is None:
            return False

        self.weapon.upgrade()
        return True

    def use_skill(self):
        return int(self.weapon.power * self.skill.multiplier)

    def take_damage(self, amount):
        self.hp.damage(amount - self.armor.defense)
        return amount - self.armor.defense


class Warrior(Character):
    def __init__(self, name):
        super().__init__(name=name, 
                         max_hp=HP(150), 
                         weapon=Weapon(name="화염검",element="불",power=30),
                         level=Level(character=self))
class Wizard(Character):
    def __init__(self, name):
        super().__init__(name=name, 
                         max_hp=HP(90), 
                         weapon=Weapon("지팡이",8),
                         level=Level(character=self))

hero = Warrior("아서")

# 1) 슬라임 사냥
for line in hero.attack(Slime()):
    print(line)
print([i.name for i in hero.inventory.items])
print("---")

# 2) 골렘 사냥 (쓰러질 때까지 공격)
golem = Golem()
while golem.hp.is_alive():
    for line in hero.attack(golem):
        print(line)
print("---")

# 3) 보스전 준비: 무기 교체 + 강화
print(hero.equip("물의 창"), hero.weapon, [i.name for i in hero.inventory.items])
print(hero.upgrade_weapon(), hero.weapon, hero.weapon.power)
print("---")

# 4) 보스전
boss = Dragon()
turn = 0
while boss.hp.is_alive():
    turn += 1
    hero.attack(boss)
print(f"{turn}턴 만에 보스 처치! Lv.{hero.level.level}, EXP {hero.level.exp}")