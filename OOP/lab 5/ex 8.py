class Stack:
    def __init__(self, items=()):
        self._items = list(items)

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise ValueError("Нельзя извлечь элемент из пустого стека")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise ValueError("Стек пуст")
        return self._items[-1]

    def __len__(self):
        return len(self._items)

    def __contains__(self, item):
        return item in self._items

    def __str__(self):
        if not self._items:
            return "Стек: <пуст>"
        return "Стек: " + " → ".join(str(x) for x in reversed(self._items))

    def __repr__(self):
        return f"Stack({self._items!r})"

    def __iter__(self):
        return iter(reversed(self._items))

    def __add__(self, other):
        if not isinstance(other, Stack):
            return NotImplemented
        return Stack(self._items + other._items)

    def __eq__(self, other):
        if not isinstance(other, Stack):
            return NotImplemented
        return self._items == other._items

    __hash__ = None

    def __bool__(self):
        return bool(self._items)

    def __getitem__(self, index):
        return self._items[::-1][index]

def check_brackets(text):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = Stack()
    for pos, ch in enumerate(text):
        if ch in "([{":
            stack.push((ch, pos))
        elif ch in pairs:
            if not stack:
                return False, f"лишняя закрывающая «{ch}» в позиции {pos}"
            opener, open_pos = stack.pop()
            if opener != pairs[ch]:
                return False, (f"«{opener}» (позиция {open_pos}) закрыта "
                               f"неподходящей «{ch}» (позиция {pos})")
    if stack:
        opener, open_pos = stack.peek()
        return False, f"не закрыта «{opener}» в позиции {open_pos}"
    return True, "скобки расставлены правильно"

if __name__ == "__main__":
    s = Stack()
    print("Пустой стек:", s, "| bool:", bool(s), "| len:", len(s))
    for x in (10, 20, 30, 40):
        s.push(x)
    print("После push(10..40):", s)
    print("repr:", repr(s))
    print("len =", len(s), "| peek() =", s.peek(), "(элемент остался)")
    print("pop() =", s.pop(), "->", s)
    print("bool(s) =", bool(s))
    print("\nПоиск и индексы:")
    print("20 in s:", 20 in s, "| 99 in s:", 99 in s)
    print("s[0] =", s[0], "(вершина) | s[1] =", s[1], "| s[-1] =", s[-1], "(основание)")
    print("Итерация от вершины:", [x for x in s])
    print("\nКонкатенация и сравнение:")
    t = Stack(["a", "b"])
    u = s + Stack([1, 2])
    print("s     :", s)
    print("s + [1,2]:", u)
    print("исходный s не изменился:", s, "| len(u) =", len(u))
    print("Stack([1, 2]) == Stack([1, 2]):", Stack([1, 2]) == Stack([1, 2]),
          "| Stack([1, 2]) == Stack([2, 1]):", Stack([1, 2]) == Stack([2, 1]))
    print("\nИзвлечение всех элементов:")
    tmp = Stack(s)
    while tmp:
        print("  pop ->", tmp.pop())
    print("Итог:", tmp, "| bool =", bool(tmp))
    print("\nПроверка скобок:")
    tests = ["(a + b) * [c - {d / e}]", "((a + b)", "{[(])}", "", ")(", "f(x[1]) + g{y}",
             "((()))]"]
    for expr in tests:
        ok, msg = check_brackets(expr)
        print(f"  {expr!r:<28} {'ВЕРНО' if ok else 'ОШИБКА':<7} {msg}")

    print("\nОбработка ошибок:")
    for action in (lambda: Stack().pop(), lambda: Stack().peek(), lambda: s[10],
                   lambda: s + [1, 2]):
        try:
            action()
        except (ValueError, IndexError, TypeError) as e:
            print(f"  {type(e).__name__}: {e}")