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
            initial, accept = State(), State()
            initial.edge1, initial.edge2 = nfa1.initial, accept
            nfa1.accept.edge1, nfa1.accept.edge2 = nfa1.initial, accept
            stack.append(NFA(initial, accept))
        elif c == CONCATENATION:
            nfa2, nfa1 = stack.pop(), stack.pop()
            nfa1.accept.edge1 = nfa2.initial
            stack.append(NFA(nfa1.initial, nfa2.accept))
        elif c == UNION:
            nfa2, nfa1 = stack.pop(), stack.pop()
            initial = State()
            initial.edge1, initial.edge2 = nfa1.initial, nfa2.initial
            accept = State()
            nfa1.accept.edge1, nfa2.accept.edge1 = accept, accept
            stack.append(NFA(initial, accept))
        else:
            accept, initial = State(), State()
            initial.label, initial.edge1 = c, accept
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
    precedence = {'|': 1, '+': 2, '*': 3}
    postfix = ''
    stack = []
    for char in infix:
        if char.isalpha():
            postfix += char
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                postfix += stack.pop()
            stack.pop()
        else:
            while stack and stack[-1] != '(' and precedence[char] <= precedence.get(stack[-1], 0):
                postfix += stack.pop()
            stack.append(char)
    while stack:
        postfix += stack.pop()
    return postfix


def match(infix, word):
    """
    Функция принимает обратную польскую запись и слово. 
    Возвращает True если слово принадлежит регулярному выражению и 
    False в противном случае
    """
    postfix = infix_to_postfix(infix)
    nfa = thompson_construction(postfix)
    current = set()
    incoming = set()
    current |= search_states(nfa.initial)
    for s in word:
        for c in current:
            if c.label == s:
                incoming |= search_states(c.edge1)
        current = incoming
        incoming = set()
    return nfa.accept in current


def is_correct_regex(regex_str):
    """
    Функция принимает регулярное выражение и проверят,
    что оно правильно задано
    """
    if len(regex_str) > 1:
        if regex_str[0] == '(' and regex_str[-1] == ')':
            middle = regex_str[1:-1]
            for i in range(0, len(middle)):
                if middle[i] == CONCATENATION or middle[i] == UNION:
                    left = middle[0:i]
                    right = middle[i + 1:]
                    if is_correct_regex(left) and is_correct_regex(right):
                        return True
            return False
        elif regex_str[-1] == KLEENE_STAR:
            return is_correct_regex(regex_str[:-1])
        else:
            # Проверяем, что регулярное выражение не состоит из двух и более букв алфавита SIGMA
            if len(regex_str) > 1 and all(c in SIGMA for c in regex_str):
                return False
            for c in regex_str:
                if c not in SIGMA:
                    return False
            return True
    elif len(regex_str) == 1:
        if regex_str == EMPTY_LANGUAGE or regex_str == EMPTY_WORD or regex_str in SIGMA:
            return True
    else:
        return False
