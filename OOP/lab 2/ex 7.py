class Safe:
    MAX_ATTEMPTS = 3

    def __init__(self, pin, master_pin):
        self.__pin = pin
        self.__master_pin = master_pin
        self.__content = []
        self.__attempts = 0
        self.__locked = False

    def __check_pin(self, pin):
        if self.__locked:
            print('Сейф заблокирован!')
            return False
        if pin == self.__pin:
            self.__attempts = 0
            return True
        self.__attempts += 1
        left = Safe.MAX_ATTEMPTS - self.__attempts
        if left <= 0:
            self.__locked = True
            print('Неверный PIN. Сейф заблокирован!')
        else:
            print(f'Неверный PIN. Осталось попыток: {left}')
        return False

    def open(self, pin):
        if self.__check_pin(pin):
            print('Сейф открыт. Содержимое:', self.__content or 'пусто')
            return list(self.__content)
        return None

    def put(self, item, pin):
        if self.__check_pin(pin):
            self.__content.append(item)
            print(f'«{item}» положен в сейф')
            return True
        return False

    def reset(self, master_pin):
        if master_pin == self.__master_pin:
            self.__locked = False
            self.__attempts = 0
            print('Сейф разблокирован мастер-кодом')
            return True
        print('Неверный мастер-код')
        return False

s = Safe('1234', '9999')
s.put('паспорт', '1234')
s.put('деньги', '1234')
s.open('1234')
print('\n-- Подбор PIN --')
s.open('0000')
s.open('1111')
s.open('2222')
s.open('1234')
print('\n-- Разблокировка --')
s.reset('0000')
s.reset('9999')
s.open('1234')