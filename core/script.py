class Humanity:
    def __init__(self, name):
        self.name = name
        self.__species = "Homo Sapiens"  # Інкапсуляція

    def say_hello(self):
        print(f"\n[Людина]: Привіт, я {self.name}")

    def action(self):
        print(f"{self.name} займається повсякденними справами.")

    def get_species(self):
        return self.__species


class Student(Humanity):
    def __init__(self, name, group):
        super().__init__(name)
        self.group = group

    # Поліморфізм
    def action(self):
        print(f"Студент {self.name} з групи {self.group} пише лабораторну.")


# Список для зберігання всіх створених людей/студентів
people_list = []

print("--- Програма створення списку людей ---")

while True:
    print("\nКого ви хочете додати?")
    print("1 - Звичайну людину")
    print("2 - Студента")
    print("0 - Вихід та показ списку")

    choice = input("Ваш вибір: ")

    if choice == "0":
        break

    name = input("Введіть ім'я: ")

    if choice == "1":
        person = Humanity(name)
        people_list.append(person)
    elif choice == "2":
        group = input("Введіть групу: ")
        student = Student(name, group)
        people_list.append(student)
    else:
        print("Невірний вибір, спробуйте ще раз.")

# Демонстрація всіх зі списку
print("\n" + "=" * 30)
print("ВЕСЬ СПИСОК СТВОРЕНИХ ОБ'ЄКТІВ:")
for p in people_list:
    p.say_hello()
    p.action()
    print(f"Біологічний вид: {p.get_species()}")