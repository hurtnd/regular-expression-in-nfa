from string import ascii_lowercase

SIGMA = ascii_lowercase  # Алфавит из маленьких английских букв
CONCATENATION = '+'
UNION = '|'
KLEENE_STAR = '*'
EMPTY_LANGUAGE = '#'
EMPTY_WORD = 'E'


class State:
    label = None
    edge1 = None
    edge2 = None


class NFA:
    """
    Класс недетерминированного конечного автомата
    """
    initial = None
    accept = None

    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept


def thompson_construction(postfix):
    """
    Функция принимает обратную польскую запись регулярного выражения и
    возвращает соответствующий недетерминированный конечный автомат
    """
    stack = []
    for c in postfix:
        if c == KLEENE_STAR:
            nfa1 = stack.pop()
            initial = State()  # Начальное состояние
            accept = State()  # Конечное состояние
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept
            stack.append(NFA(initial, accept))
        elif c == CONCATENATION:
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            nfa1.accept.edge1 = nfa2.initial
            stack.append(NFA(nfa1.initial, nfa2.accept))
        elif c == UNION:
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            initial = State()
            accept = State()
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial
            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept
            stack.append(NFA(initial, accept))
        else:
            initial = State()
            accept = State()
            initial.label = c
            initial.edge1 = accept
            stack.append(NFA(initial, accept))
    return stack.pop()


def search_states(state):
    """
    Функция рекурсивно находит множество состояний,
    в которые можно перейти из заданного состояния
    """
    states = set()
    states.add(state)
    if state.label is None:
        if state.edge1 is not None:
            states |= search_states(state.edge1)
        if state.edge2 is not None:
            states |= search_states(state.edge2)
    return states


def infix_to_postfix(infix):
    """
    Функция принимает регулярное выражение и
    делает из него обратную польскую запись
    """
    # Словарь, содержащий приоритеты операторов
    precedence = {UNION: 1, CONCATENATION: 2, KLEENE_STAR: 3}

    postfix = ''  # Переменная для хранения постфиксной записи
    stack = []  # Стек для хранения операторов

    for i, char in enumerate(infix):
        # Если символ - буква алфавита,
        # он добавляется к выходной строке в постфиксной форме
        if char.isalpha():
            postfix += char
        # Если символ - открывающая скобка, он добавляется в стек
        elif char == '(':
            stack.append(char)
        # Если символ - закрывающая скобка,
        # извлекаются все операторы из стека и
        # добавляются в выходную строку до тех пор,
        # пока не встретится открывающая скобка
        elif char == ')':
            while stack and stack[-1] != '(':
                postfix += stack.pop()
            stack.pop()
        else:
            # Заменяем две и более подряд идущих звёзд на одну
            if char == KLEENE_STAR and i > 0 and infix[i-1] == KLEENE_STAR:
                continue
            # Извлекаются все операторы из стека с большим или
            # равным приоритетом и добавляются в выходную строку.
            # Затем оператор добавляется в стек.
            while stack and stack[-1] != \
                    '(' and precedence[char] <= precedence.get(stack[-1], 0):
                postfix += stack.pop()
            stack.append(char)

    # Извлекаются все операторы из стека и добавляются в выходную строку
    while stack:
        postfix += stack.pop()

    return postfix  # Возвращает постфиксную запись


def match(infix, word):
    """
    Функция принимает обратную польскую запись и слово.
    Возвращает True если слово принадлежит регулярному выражению и
    False в противном случае
    """
    # Преобразуем регулярное выражение из инфиксной формы в постфиксную
    postfix = infix_to_postfix(infix)
    # Вызываем функцию, которая по заданному регулярному выражению строит НКА
    nfa = thompson_construction(postfix)
    current = set()
    incoming = set()
    # Вызов функции, которая возвращает множество состояний НКА,
    # в которых автомат может находиться после перехода из начального состояния
    current |= search_states(nfa.initial)
    for s in word:
        for c in current:
            if c.label == s:
                # Вызов функции, которая возвращает множество состояний НКА,
                # в которые автомат может перейти по первому ребру
                incoming |= search_states(c.edge1)
        current = incoming
        incoming = set()  # Чистим
    return nfa.accept in current


def is_correct_regex(regex_str):
    """
    Функция принимает регулярное выражение и проверят,
    что оно правильно задано
    """
    if len(regex_str) > 1:
        # Проверяем, что рег. выражение начинается и заканчивается со скобки
        if regex_str[0] == '(' and regex_str[-1] == ')':
            # Создаем строку, которая содержит среднюю часть рег. выражения,
            # т.е. все символы между первой и последней скобками.
            middle = regex_str[1:-1]
            # Проходимся по всем символам в средней части регулярного выражения
            for i in range(0, len(middle)):
                if middle[i] == CONCATENATION or middle[i] == UNION:
                    # Содержит левую часть текущего подвыражения
                    left = middle[0:i]
                    # Содержит правую часть текущего подвыражения
                    right = middle[i + 1:]
                    if is_correct_regex(left) and is_correct_regex(right):
                        return True
            return False
        # Проверяем, что рег. выражение заканчивается символом звездочки Клини
        elif regex_str[-1] == KLEENE_STAR:
            return is_correct_regex(regex_str[:-1])
        else:
            # Проверяем, что регулярное выражение не состоит из двух
            # и более букв алфавита SIGMA подряд
            if len(regex_str) > 1 and all(c in SIGMA for c in regex_str):
                return False
            for c in regex_str:
                if c not in SIGMA:
                    return False
            return True
    elif len(regex_str) == 1:
        if regex_str == EMPTY_LANGUAGE or regex_str == EMPTY_WORD \
                                       or regex_str in SIGMA:
            return True
    else:
        return False
