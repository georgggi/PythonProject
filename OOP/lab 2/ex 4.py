class EWallet:
    def __init__(self, owner, balance, currency, max_transfer):
        self.__owner = owner
        self.__balance = balance
        self.__currency = currency
        self.__max_transfer = max_transfer

    @property
    def balance(self):
        return self.__balance

    @property
    def can_transfer(self):
        return self.__balance > 0

    def transfer(self, recipient, amount):
        if not isinstance(recipient, EWallet):
            print('Ошибка: получатель должен быть кошельком')
            return False
        if amount <= 0:
            print('Ошибка: сумма должна быть положительной')
            return False
        if amount > self.__max_transfer:
            print(f'Отказ: превышен лимит перевода ({self.__max_transfer} {self.__currency})')
            return False
        if amount > self.__balance:
            print(f'Отказ: недостаточно средств ({self.balance} {self.__currency})')
            return False
        self.__balance -= amount
        recipient.__balance += amount
        print(f'{self.__owner} → {recipient.__owner}: {amount} {self.__currency}')
        return True

    def __str__(self):
        return f'{self.__owner}: {self.balance} {self.__currency}'

w1 = EWallet('Айдар', 10000, 'KGS', 5000)
w2 = EWallet('Бекзат', 2000, 'KGS', 3000)
w3 = EWallet('Чолпон', 0, 'KGS', 1000)

print('До переводов:')
for w in (w1, w2, w3):
    print(' ', w, '| переводы доступны:', w.can_transfer)

print('\nПереводы:')
w3.transfer(w1, 100)
w1.transfer(w2, 3000)
w1.transfer(w3, 6000)
w2.transfer(w3, 4500)
w2.transfer(w3, 2500)
w3.transfer(w1, 500)

print('\nПосле переводов:')
for w in (w1, w2, w3):
    print(' ', w)