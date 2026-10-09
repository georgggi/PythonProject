class SecurePassword:
    def __init__(self):
        self.__password = None

    @staticmethod
    def __errors(pwd):
        errors = []
        if len(pwd) < 8:
            errors.append('длина меньше 8 символов')
        if not any(ch.isdigit() for ch in pwd):
            errors.append('нет ни одной цифры')
        if not any(ch.isupper() for ch in pwd):
            errors.append('нет заглавной буквы')
        if ' ' in pwd:
            errors.append('есть пробелы')
        return errors

    @property
    def password(self):
        return '*' * len(self.__password) if self.__password else '(не задан)'

    @password.setter
    def password(self, value):
        errors = self.__errors(value)
        if errors:
            for e in errors:
                print(f'  ✗ {e}')
            return
        self.__password = value
        print('  ✓ пароль установлен')

    def check(self, pwd):
        return self.password is not None and pwd == self.password

    def strength(self, pwd):
        ok = 4 - len(self.__errors(pwd))
        if ok == 4:
            return 'Сильный'
        if ok == 3:
            return 'Средний'
        return 'Слабый'

sp = SecurePassword()
for test in ['abc', 'abcdefgh', 'Abcdefg1', 'My Pass 12', 'Str0ngPass']:
    print(f'Пароль «{test}» — {sp.strength(test)}')
    sp.password = test

print('\nХранимый пароль:', sp.password)
print('check("Str0ngPass"):', sp.check('Str0ngPass'))
print('check("wrong"):', sp.check('wrong'))