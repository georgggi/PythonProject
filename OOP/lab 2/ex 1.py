class BankAccount:
    def __init__(self, owner, balance=0):
        if balance < 0:
            raise ValueError('Начальный баланс не может быть отрицательным')
        self.__owner = owner
        self.__balance = balance
        self.__log = []

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            print('Ошибка: сумма пополнения должна быть положительной')
            return False
        self.__balance += amount
        self.__log.append(f'+{amount} сом (пополнение)')
        return True

    def withdraw(self, amount):
        if amount <= 0:
            print('Ошибка: сумма снятия должна быть положительной')
            return False
        if amount > self.__balance:
            print(f'Ошибка: недостаточно средств (баланс {self.__balance} сом)')
            return False
        self.__balance -= amount
        self.__log.append(f'-{amount} сом (снятие)')
        return True

    def get_statement(self):
        lines = [f'Выписка по счёту. Владелец: {self.__owner}']
        for i, op in enumerate(self.__log, 1):
            lines.append(f'  {i}. {op}')
        lines.append(f'Текущий баланс: {self.__balance} сом')
        return '\n'.join(lines)

acc1 = BankAccount('Айдар', 5000)
acc1.deposit(2000)
acc1.withdraw(1500)
acc1.withdraw(10000)
acc1.deposit(-50)
acc1.deposit(500)
print(acc1.get_statement())
print()

acc2 = BankAccount('Айгуль', 300)
acc2.deposit(1200)
acc2.withdraw(400)
acc2.withdraw(2000)
acc2.deposit(100)
print(acc2.get_statement())