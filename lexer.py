# Tovid language lexer

token_table = {'true': 'keyword', 'false': 'keyword', 'const': 'keyword', 'var': 'keyword', 'func': 'keyword',
               'return': 'keyword', 'if': 'keyword', 'else': 'keyword', 'for': 'keyword', 'range': 'keyword',
               'break': 'keyword', 'import': 'keyword', 'package': 'keyword', 'nil': 'keyword', 'iota': 'keyword',
               'int': 'keyword', 'float': 'keyword', 'complex': 'keyword', 'string': 'keyword', 'boolean': 'keyword',
               ':=': 'assign_op', '.': 'punc', ',': 'punc', ':': 'punc', ';': 'punc',
               ' ': 'ws', '\t': 'ws', '\n': 'cr', '\r': 'cr', '\n\r': 'cr', '\r\n': 'cr',
               '-': 'add_op', '+': 'add_op', '*': 'mult_op', '/': 'mult_op', '^': 'pow_op',
               '(': 'brack_op', ')': 'brack_op', '{': 'brack_op', '}': 'brack_op'
               }
token_state_table = {2: 'ident', 4: 'int', 7: 'float', 11: 'complex', 19: 'string', 16: 'rel_op', 17: 'rel_op'}


stf = {(0, 'Letter'): 1, (1, 'Letter'): 1, (1, 'Digit'): 1, (1, 'other'): 2,
       (0, 'Digit'): 3, (3, 'Digit'): 3, (3, 'other'): 4, (3, 'dot'): 5, (3, '+'): 8, (5, 'Digit'): 6,
       (5, 'other'): 103, (6, 'Digit'): 6, (6, 'other'): 7, (6, '+'): 8, (8, 'Digit'): 8, (8, 'dot'): 9,
       (8, 'Letter'): 21, (8, 'other'): 101, (9, 'Digit'): 10, (9, 'other'): 103, (10, 'Digit'): 10, (10, 'Letter'): 21,
       (10, 'other'): 101, (21, 'other'): 11,
       (0, ':'): 12, (12, '='): 13, (12, 'other'): 102,
       (0, 'other'): 101,
       (0, 'cr'): 14,
       (0, 'ws'): 0,
       (0, '='): 15, (0, '!'): 15, (15, '='): 16, (15, 'other'): 101,
       (0, '<'): 22, (0, '>'): 22, (22, '='): 16, (22, 'other'): 17,
       (0, '"'): 18, (18, 'other'): 18, (18, '"'): 19,
       (0, '{'): 20, (0, '}'): 20, (0, '^'): 20, (0, '/'): 20, (0, '*'): 20, (0, '-'): 20, (0, '+'): 20,
       (0, '('): 20, (0, ')'): 20, (0, ','): 20, (0, ';'): 20
       }
init_state = 0
F = {2, 4, 7, 11, 13, 14, 16, 17, 19, 20, 101, 102, 103}
F_star = {2, 4, 7, 11, 17}
F_error = {101, 102, 103}

table_of_symb = {}
table_of_id = {}
table_of_const = {}

state = init_state

f = open('file.tovid', 'r')
source_code = f.read()
f.close()

f_success = (True, 'Lexer')

len_code = len(source_code)-1
num_line = 1
num_char = -1
char = ''
lexeme = ''


def lex():
    global state, num_line, char, lexeme, num_char, f_success
    try:
        while num_char < len_code:
            char = next_char()
            class_ch = class_of_char(char)
            state = next_state(state, class_ch)
            if is_final(state):
                processing()
            elif state == init_state:
                lexeme = ''
            else:
                lexeme += char
        print('Lexer: Лексичний аналіз завершено успішно')
    except SystemExit as error:
        f_success = (False, 'Lexer')
        print('Lexer: Аварійне завершення програми з кодом {0}'.format(error))


def processing():
    global state, lexeme, char, num_line, num_char, table_of_symb
    if state == 14:
        num_line += 1
        state = init_state
    if state in F_star:
        token = get_token(state, lexeme)
        if token != 'keyword':
            index = index_id_const(state, lexeme)
            try:
                print('{0:<3d} {1:<10s} {2:<10s} {3:<2d} '.format(num_line, lexeme, token, index))
            except TypeError:
                print('{0:<3d} {1:<10s} {2:<10s} {3:<2d} '.format(num_line, lexeme, token, index[1]))
            table_of_symb[len(table_of_symb)+1] = (num_line, lexeme, token, index)
        else:  # якщо keyword
            print('{0:<3d} {1:<10s} {2:<10s} '.format(num_line, lexeme, token))
            table_of_symb[len(table_of_symb)+1] = (num_line, lexeme, token, '')
        lexeme = ''
        num_char = put_char_back(num_char)  # зiрочка
        state = init_state
    if state in (13, 16, 17, 19, 20):
        lexeme += char
        token = get_token(state, lexeme)
        print('{0:<3d} {1:<10s} {2:<10s} '.format(num_line, lexeme, token))
        table_of_symb[len(table_of_symb)+1] = (num_line, lexeme, token, '')
        lexeme = ''
        state = init_state
    if state in F_error:  # (101, 102, 103): # ERROR
        fail()


def fail():
    global state, num_line, char
    print(num_line)
    if state == 101:
        print('Lexer: у рядку ', num_line, ' неочікуваний символ ' + char)
        exit(101)
    if state == 102:
        print('Lexer: у рядку ', num_line, ' очікувався символ =, а не ' + char)
        exit(102)
    if state == 103:
        print('Lexer: у рядку ', num_line, ' очікувалася цифра, а не ' + char, ' неможливо сформувати дробове число')
        exit(103)


def is_final(state):
    if state in F:
        return True
    else:
        return False


def next_state(state, class_ch):
    global char
    # if state in (8, 10):
    #     if class_ch == 'Letter' and char != 'i':
    #         return stf[(state, 'other')]
    try:
        return stf[(state, class_ch)]
    except KeyError:
        return stf[(state, 'other')]


def next_char():
    global num_char
    num_char += 1
    return source_code[num_char]


def put_char_back(num_char):
    return num_char-1


def class_of_char(char):
    if char == '.':
        result = "dot"
    elif char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
        result = "Letter"
    elif char in "0123456789":
        result = "Digit"
    elif char in " \t":
        result = "ws"
    elif char == "\n":
        result = "cr"
    elif char in "+-*/^(){}<>=\"\\,:;!":
        result = char
    else:
        result = "Символ не належить алфавіту"

    return result


def get_token(state, lexeme):
    try:
        return token_table[lexeme]
    except KeyError:
        return token_state_table[state]


def index_id_const(state, lexeme):
    indx = 0
    if state == 2:
        indx = table_of_id.get(lexeme)
        if not indx:
            indx = len(table_of_id)+1
            table_of_id[lexeme] = indx
    if state in (4, 7, 11):
        indx = table_of_const.get(lexeme)
        if not indx:
            indx = len(table_of_const)+1
            table_of_const[lexeme] = (token_state_table[state], indx)
    return indx


lex()


print('-' * 30)
print('table_of_symb:{0}'.format(table_of_symb))
print('table_of_id:{0}'.format(table_of_id))
print('table_of_const:{0}'.format(table_of_const))
