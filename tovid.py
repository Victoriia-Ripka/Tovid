# Tovid language lexer and parser

token_table = {'true': 'keyword', 'false': 'keyword', 'const': 'keyword', 'var': 'keyword', 'func': 'keyword',
               'return': 'keyword', 'if': 'keyword', 'else': 'keyword', 'for': 'keyword', 'range': 'keyword',
               'break': 'keyword', 'import': 'keyword', 'package': 'keyword', 'nil': 'keyword', 'iota': 'keyword',
               'int': 'keyword', 'float': 'keyword', 'complex': 'keyword', 'string': 'keyword', 'boolean': 'keyword',
               'print': 'keyword', 'scanf': 'keyword', ':=': 'assign_op',
               '.': 'punc', ',': 'punc', ':': 'punc', ';': 'punc',
               ' ': 'ws', '\t': 'ws', '\n': 'cr', '\r': 'cr', '\n\r': 'cr', '\r\n': 'cr',
               '*': 'mult_op', '/': 'mult_op', '^': 'pow_op', '+': 'add_op', '-': 'add_op',
               '==': 'rel_op', '>': 'rel_op', '>=': 'rel_op', '<': 'rel_op', '<=': 'rel_op', '!=': 'rel_op',
               '> ': 'rel_op', '>= ': 'rel_op', '< ': 'rel_op', '<= ': 'rel_op', '!= ': 'rel_op',
               '(': 'brack_op', ')': 'brack_op', '{': 'brack_op', '}': 'brack_op',
               '//': 'comment', '/*': 'comment', '*/': 'comment'
               }
token_state_table = {2: 'ident', 4: 'int', 7: 'float', 11: 'complex', 19: 'string', 16: 'rel_op', 17: 'rel_op'}


stf = {(0, 'Letter'): 1, (1, 'Letter'): 1, (1, 'Digit'): 1, (1, 'other'): 2,
       (0, 'Digit'): 3, (3, 'Digit'): 3, (3, 'other'): 4, (3, 'dot'): 5, (3, '+'): 8, (3, 'i'): 21, (5, 'Digit'): 6,
       (5, 'other'): 103, (6, 'Digit'): 6, (6, 'other'): 7, (6, '+'): 8, (6, 'i'): 21, (8, 'Digit'): 8, (8, 'dot'): 9,
       (8, 'i'): 21, (8, 'other'): 101, (9, 'Digit'): 10, (9, 'other'): 103, (10, 'Digit'): 10, (10, 'i'): 21,
       (10, 'other'): 101, (21, 'other'): 11,
       (0, ':'): 12, (12, '='): 13, (12, 'other'): 102,
       (0, 'other'): 101,
       (0, 'cr'): 14,
       (0, 'ws'): 0,
       (0, '='): 15, (0, '!'): 15, (15, '='): 16, (15, 'other'): 101,
       (0, '<'): 22, (0, '>'): 22, (22, '='): 16, (22, 'other'): 17,
       (0, '"'): 18, (18, 'other'): 18, (18, '"'): 19,
       (0, '{'): 20, (0, '}'): 20, (0, '^'): 20, (0, '+'): 20, (0, '-'): 20,
       (0, '('): 20, (0, ')'): 20, (0, ','): 20, (0, ';'): 20,
       (0, '/'): 26, (0, '*'): 23, (26, 'other'): 25, (23, 'other'): 25,
       (26, '/'): 24, (26, '*'): 24, (23, '/'): 24,
       }
init_state = 0
F = {2, 4, 7, 11, 13, 14, 16, 17, 19, 20, 24, 25, 101, 102, 103}
F_star = {2, 4, 7, 11, 17, 25}
F_error = {101, 102, 103}

table_of_symb = {}
table_of_id = {}
table_of_const = {}

table_of_var = {}
table_of_named_const = {}
bool_expr_results = ('true', 'false')

state = init_state

file_name = input('Введіть файл (без .tovid): ')
f = open(f'{file_name}.tovid', 'r')
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

            # на випадок відсутности відступу чи нового рядка в кінці файлу
            if num_char == len_code:
                num_char += 1
                state = next_state(state, 'cr')
                if is_final(state):
                    processing()
        print('\n\033[0m\033[1m\033[4mLexer\033[0m: \033[92mЛексичний аналіз завершено успішно\033[0m')
    except SystemExit as error:
        f_success = (False, 'Lexer')
        print('\n\033[0m\033[1m\033[4mLexer\033[0m: \033[91mАварійне завершення програми з кодом {0}\033[0m'.format(error))


def processing():
    global state, lexeme, char, num_line, num_char, table_of_symb
    if state in F:
        if state == 14:
            num_line += 1
            state = init_state
        elif state in F_star:
            token = get_token(state, lexeme)
            if token != 'keyword':
                index = index_id_const(state, lexeme)
                try:
                    print('{0:<3d} {1:<10s} {2:<10s} {3:<2d} '.format(num_line, lexeme, token, index))
                except TypeError:
                    print('{0:<3d} {1:<10s} {2:<10s} {3:<2d} '.format(num_line, lexeme, token, index[1]))
                table_of_symb[len(table_of_symb)+1] = (num_line, lexeme, token, index)
            else:  # якщо keyword
                # print('{0:<3d} {1:<10s} {2:<10s} '.format(num_line, lexeme, token))
                table_of_symb[len(table_of_symb)+1] = (num_line, lexeme, token, '')
            lexeme = ''
            num_char = put_char_back(num_char)  # зiрочка
            state = init_state
        elif state in F_error:  # (101, 102, 103): # ERROR
            fail()
        else:
            lexeme += char
            token = get_token(state, lexeme)
            # print('{0:<3d} {1:<10s} {2:<10s} '.format(num_line, lexeme, token))
            table_of_symb[len(table_of_symb) + 1] = (num_line, lexeme, token, '')
            lexeme = ''
            state = init_state


def fail():
    global state, num_line, char
    if state == 101:
        print('\033[91mLexer ERROR: у рядку ', num_line, ' неочікуваний символ ' + char, '\033[0m')
        exit(101)
    if state == 102:
        print('\033[91mLexer ERROR: у рядку ', num_line, ' очікувався символ =, а не ' + char, '\033[0m')
        exit(102)
    if state == 103:
        print('\033[91mLexer ERROR: у рядку ', num_line, ' очікувалася цифра, а не ' + char,
              ' неможливо сформувати дробове число\033[0m')
        exit(103)


def is_final(state):
    if state in F:
        return True
    else:
        return False


def next_state(state, class_ch):
    global char
    if state in (3, 6, 8, 10):
        if class_ch == 'Letter':
            if char == 'i':
                return stf[(state, char)]
            else:
                return stf[(state, 'other')]
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


# print('\n', '-' * 30)
# print('table_of_symb:{0}'.format(table_of_symb))
# print('-' * 30)
# print('table_of_id:{0}'.format(table_of_id))
# print('-' * 30)
# print('table_of_const:{0}'.format(table_of_const))
# print('-' * 30, '\n')


# -------------------------------------------------------
# syntax and semantic
# -------------------------------------------------------


num_row_s = 1
num_line_s = 1
len_table_of_symb = len(table_of_symb)

params_types = {'nil': 'keyword', 'iota': 'keyword', 'int': 'keyword', 'float': 'keyword', 'complex': 'keyword',
                'string': 'keyword', 'boolean': 'keyword'}

allowed_data_types = ['int', 'float', 'complex', 'string', 'boolean']

def parse_program():
    global num_row_s, num_line_s
    try:
        while num_row_s < len_table_of_symb:
            num_line_s, lex, tok = get_current_lexeme(num_row_s)
            if lex == 'func':
                parse_func()
            elif lex == 'import':
                parse_import()
            elif lex == '//' or lex == '/*':
                parse_comment(num_line_s)
            elif lex == 'package':
                parse_package()
            elif lex == 'if':
                parse_if()
            elif lex == 'for':
                parse_for()
            elif lex == 'scanf' or lex == 'print':
                parse_scanf_print(lex, tok)
            elif lex == 'var' or lex == 'const':
                parse_declarlist()
            elif lex in table_of_id.keys():
                if lex in table_of_var.keys() or lex in table_of_named_const.keys():
                    parse_declared_var(lex, tok)  # переприсвоєння (якщо const то видасть помилку всередині)
                else:
                    fail_parse('оголошення змінної чи константи без var/const', (num_line_s, lex, tok))
            else:
                parse_statementlist()
        print("\n\033[0m\033[1m\033[4mParser\033[0m: \033[92mСинтаксичний і семантичний аналiз завершився успiшно\033[0m")
        return True
    except SystemExit as e:
        print("\n\033[0m\033[1m\033[4mParser\033[0m: \033[91mАварiйне завершення програми з кодом {0}\033[0m".format(e))


def parse_func():
    global num_row_s, num_line_s, table_of_var
    num_row_s += 1
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    parse_identlist(lex)
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    parse_token('(', tok, num_row_s)
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    parse_token(')', tok, num_row_s)
    parse_token('{', tok, num_row_s)
    parse_statementlist()
    parse_token('}', tok, num_row_s)
    # скоуп закінчився. Очищаємо змінні та параметри функції
    # table_of_var.clear()
    # current_func_params.clear()
    # Уже ні :)))


# def parse_params(lexeme, token):
#     global num_row_s, num_line_s, current_func_params
#     if lexeme != ')':
#         num_line_s, lex, tok = get_current_lexeme(num_row_s)
#         num_line_s1, lex1, tok1 = get_current_lexeme(num_row_s + 1)
#         while lex != ')':
#             if lex in table_of_id.keys() or tok in params_types.keys():
#                 current_func_params.append(lex)
#                 num_row_s += 1
#                 num_line_s, lex, tok = get_current_lexeme(num_row_s)
#             else:
#                 fail_parse('очікувався параметр', (num_line_s, lex, tok))
#             if lex == ',':
#                 num_line_s1, lex1, tok1 = get_current_lexeme(num_row_s + 1)
#                 if lex1 in table_of_id.keys() or tok1 in params_types.keys():
#                     current_func_params.append(lex)
#                     num_row_s += 1
#                     num_line_s, lex, tok = get_current_lexeme(num_row_s)
#                 else:
#                     fail_parse('очікувався параметр', (num_line_s, lex1, tok1))
#     num_line_s += 1


def parse_token(lexeme, token, id) :
    global num_row_s, num_line_s
    if num_row_s <= len_table_of_symb:
        num_line_s, lex, tok = get_current_lexeme(num_row_s)
        num_row_s += 1
        if (lex, tok) == (lexeme, token):
            # print('parseToken: В рядку {0} токен {1}'.format(num_line_s, (lexeme, token)))
            return True
        else:
            fail_parse('невiдповiднiсть токенiв', (num_line_s, lex, tok, lexeme, token))
            return False
    else:
        fail_parse("неочiкуваний кiнець програми", (lexeme, token, num_row_s))


def parse_identlist(lexeme):
    global num_row_s
    if lexeme in table_of_id.keys():
        num_row_s += 1
    else:
        num_line_s, lex, tok = get_current_lexeme(num_row_s)
        fail_parse('очікувався ідентифікатор', (num_line_s, lex, tok))


def parse_comment(comment_line):
    global num_row_s, num_line_s
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    if lex == '//':
        while num_line_s == comment_line:
            num_row_s += 1
            num_line_s, lex, tok = get_current_lexeme(num_row_s)
        num_row_s -= 1
    elif lex == '/*':
        while lex != '*/':
            num_row_s += 1
            num_line_s, lex, tok = get_current_lexeme(num_row_s)
    num_row_s += 1


# зарарз працює як тіло функції/іф/фор.
# пофіксити, щоб можна було без вкладеності парсити теж (не чекати на '}')
def parse_statementlist():
    global num_row_s, num_line_s

    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    while lex != '}':
        if lex == '//' or lex == '/*':
            parse_comment(num_line_s)
        elif lex == 'if':
            parse_if()
        elif lex == 'for':
            parse_for()
        elif lex == 'var' or lex == 'const':
            parse_declarlist()
        elif lex == 'scanf' or lex == 'print':
            parse_scanf_print(lex, tok)
        elif lex == 'return':
            parse_return()
        elif lex in table_of_id.keys():
            if lex in table_of_var.keys() or lex in table_of_named_const.keys():
                parse_declared_var(lex, tok)
            else:
                fail_parse('оголошення змінної чи константи без var/const', (num_line_s, lex, tok))
        else:
            # print("непередбачена логіка у функції parse_statementlist()")
            fail_parse('return', (num_line_s, lex, tok))
        num_line_s, lex, tok = get_current_lexeme(num_row_s)


def parse_declared_var(lexeme, token):
    global num_row_s, num_line_s
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    ident_line = num_line_s

    if lexeme in table_of_var.keys():
        num_row_s += 1
        parse_token(':=', 'assign_op', num_row_s)
        new_type = parse_expression()
        index, old_type, _ = table_of_var[lexeme]
        if new_type == old_type:
            table_of_var[lexeme] = (index, old_type, 'assigned')
        else:
            fail_parse('значення змінної не відповідає оголошеному типу', (ident_line, lexeme, token))
    elif lexeme in table_of_named_const.keys():
        fail_parse('переприсвоєння значення константі', (num_line_s, lex, tok))
    else:
        fail_parse("не оголошена змінна", (num_line_s, lex, tok, ))


def parse_scanf_print(lexeme, token):
    global num_line_s, num_row_s, table_of_var
    num_row_s += 1
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    parse_token('(', tok, num_row_s)
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    if lex != ')':
        num_line_s, lex, tok = get_current_lexeme(num_row_s)
        _, lex1, tok1 = get_current_lexeme(num_row_s + 1)
        while lex != ')':
            if lexeme == 'scanf':
                if lex in table_of_id.keys():
                    num_row_s += 1
                    num_line_s, lex, tok = get_current_lexeme(num_row_s)
                    # table_of_var[lex] = (index, old_type, 'assigned')
                    # в таблиці змінних зробити присвоєння до змінної таке, що було отримано зц скану
                else:
                    fail_parse('очікувався параметр', (num_line_s, lex, tok))
                if lex == ',':
                    _, lex1, tok1 = get_current_lexeme(num_row_s + 1)
                    if lex1 in table_of_id.keys():
                        num_row_s += 1
                        num_line_s, lex, tok = get_current_lexeme(num_row_s)
                    else:
                        fail_parse('очікувався параметр', (num_line_s, lex1, tok1))
            else:  # elif lexeme == print
                if lex in table_of_var.keys() or lex in table_of_named_const.keys() or tok in params_types.keys():
                    if lex in table_of_var.keys():
                        if table_of_var[lex][2] == 'undefined':
                            fail_parse('використання undefined змінної', (num_line_s, lex, tok))
                    num_row_s += 1
                    num_line_s, lex, tok = get_current_lexeme(num_row_s)
                else:
                    fail_parse('очікувався параметр', (num_line_s, lex, tok))
                if lex == ',' or lex == '+':
                    _, lex1, tok1 = get_current_lexeme(num_row_s + 1)
                    if lex1 in table_of_var.keys() or lex1 in table_of_named_const.keys() or tok1 in params_types.keys():
                        if lex in table_of_var.keys():
                            if table_of_var[lex1][2] == 'undefined':
                                fail_parse('використання undefined змінної', (num_line_s, lex1, tok1))
                        num_row_s += 1
                        num_line_s, lex, tok = get_current_lexeme(num_row_s)
                    else:
                        fail_parse('очікувався параметр', (num_line_s, lex1, tok1))
    parse_token(')', tok, num_row_s)


def parse_declarlist():
    global num_row_s
    datatype_is_declared = False
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    keyword = lex
    num_row_s += 1
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    if lex in allowed_data_types:
        declared_datatype = lex
        num_row_s += 1
        num_line_s, lex, tok = get_current_lexeme(num_row_s)
        datatype_is_declared = True
    elif lex in table_of_id.keys():
        datatype_is_declared = False
    else:
        fail_parse("не дозволений тип даних", (num_line_s, lex, tok))
    if lex in table_of_id.keys():
        if lex in table_of_var.keys() or lex in table_of_named_const.keys():
            fail_parse('повторне оголошення змінної',(num_line_s, lex, tok))
        current_id = lex
        num_row_s += 1
        num_line_s, lex, tok = get_current_lexeme(num_row_s)
        index = len(table_of_var) + 1 if keyword == 'var' else len(table_of_named_const) + 1
        if tok == 'assign_op':
            num_row_s += 1
            value_datatype = parse_expression()
            if datatype_is_declared:
                if declared_datatype == value_datatype:
                    if keyword == 'var':
                        table_of_var[current_id] = (index, declared_datatype, 'assigned')
                    else:
                        table_of_named_const[current_id] = (index, declared_datatype)
                else:
                    fail_parse('значення змінної не відповідає оголошеному типу', (num_line_s, current_id, 'ident'))
            else:
                if keyword == 'var':
                    table_of_var[current_id] = (index, value_datatype, 'assigned')
                else:
                    table_of_named_const[current_id] = (index, value_datatype)
        else:
            if keyword == 'const':
                num_row_s -= 1
                num_line_s, lex, tok = get_current_lexeme(num_row_s)
                fail_parse('не присвоєно значення константі', (num_line_s, lex, tok))
            if not datatype_is_declared:
                num_row_s -= 1
                num_line_s, lex, tok = get_current_lexeme(num_row_s)
                fail_parse("неможливо визначити тип", (num_line_s, lex, tok))
            else:
                if keyword == 'var':
                    table_of_var[current_id] = (index, declared_datatype, 'undefined')
                else:
                    table_of_named_const[current_id] = (index, declared_datatype)
    else:
        fail_parse("очікувався ідентифікатор", (num_line_s, lex, tok))


# тут якось потрібно слідкувати щоб була послідовність між змінними і знаками (а + м) * 12 > 3
def parse_expression():
    global num_row_s, num_line_s
    num_line_s, lex, tok = get_current_lexeme(num_row_s)

    if lex in bool_expr_results:
        left_type = 'boolean'
        num_row_s += 1
        finish = True
    else:
        left_type = parse_arithm_expression()
        try:
            num_line_s, lex, tok = get_current_lexeme(num_row_s)
        except KeyError:
            finish = True
        else:
            finish = False
    result_type = left_type

    while not finish:
        try:
            num_line_s, lex, tok = get_current_lexeme(num_row_s)
        except KeyError:
            finish = True
        else:
            if tok == 'rel_op':
                num_row_s += 1
                right_type = parse_arithm_expression()
                if not (left_type == 'string' or right_type == 'string' or left_type == 'complex' or right_type == 'complex'):
                    result_type = 'boolean'
                else:
                    fail_parse('неможливо виконати порівняння', (num_line_s, left_type, right_type))
            else:
                finish = True
    return result_type


def parse_arithm_expression():
    global num_row_s, num_line_s
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    if tok == 'add_op':
        num_row_s += 1

    left_type = parse_term()
    result_type = left_type
    finish = False

    while not finish:
        try:
            num_line_s, lex, tok = get_current_lexeme(num_row_s)
        except KeyError:
            finish = True
        else:
            if tok == 'add_op':
                num_row_s += 1
                right_type = parse_term()
                if left_type == right_type and left_type == 'int':
                    result_type = left_type
                elif left_type == 'boolean' or right_type == 'boolean':
                    fail_parse('невідповідність типів', (num_line_s, left_type, right_type))
                elif left_type == 'string' or right_type == 'string':
                    fail_parse('арифметична дія над стрічкою', (num_line_s, lex, tok))
                elif left_type == 'complex' or right_type == 'complex':
                    result_type = 'complex'
                else:
                    result_type = 'float'
            else:
                finish = True
    return result_type


def parse_term():
    global num_row_s, num_line_s
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    left_type = parse_chunk()
    result_type = left_type
    finish = False

    while not finish:
        try:
            num_line_s, lex, tok = get_current_lexeme(num_row_s)
        except KeyError:
            finish = True
        else:
            if tok == 'mult_op':
                operator = lex
                num_row_s += 1
                num_line_s, lex, tok = get_current_lexeme(num_row_s)
                right_type = parse_chunk()
                if left_type == 'boolean' or right_type == 'boolean':
                    fail_parse('невідповідність типів', (num_line_s, left_type, right_type))
                elif left_type == 'string' or right_type == 'string':
                    fail_parse('арифметична дія над стрічкою', (num_line_s, lex, tok))

                if operator == '/':
                    result_type = 'float'
                else:  # elif operator == '*':
                    if left_type == right_type and left_type == 'int':
                        result_type = left_type
                    elif left_type == 'complex' or right_type == 'complex':
                        result_type = 'complex'
                    else:
                        result_type = 'float'
            else:
                finish = True
    return result_type


def parse_chunk():
    global num_row_s, num_line_s
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    left_type = parse_factor()
    result_type = left_type
    finish = False

    while not finish:
        try:
            num_line_s, lex, tok = get_current_lexeme(num_row_s)
        except KeyError:
            finish = True
        else:
            if tok == 'pow_op':
                num_row_s += 1
                right_type = parse_factor()
                if left_type == 'boolean' or right_type == 'boolean':
                    fail_parse('невідповідність типів', (num_line_s, left_type, right_type))
                elif left_type == 'string' or right_type == 'string':
                    fail_parse('арифметична дія над стрічкою', (num_line_s, lex, tok))
                result_type = 'float'
            else:
                finish = True
    return result_type


def parse_factor():
    global num_row_s, num_line_s
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    factor_type = ''
    if lex in table_of_var.keys():
        if table_of_var[lex][2] == 'undefined':
            fail_parse('використання undefined змінної', (num_line_s, lex, tok))
        factor_type = table_of_var[lex][1]
    elif lex in table_of_named_const.keys():
        factor_type = table_of_named_const[lex][1]
    elif lex in table_of_const.keys():
        factor_type = table_of_const[lex][0]
    elif tok == 'string':
        factor_type = 'string'
    elif lex in bool_expr_results:
        factor_type = 'boolean'
    elif lex == '(':
        num_row_s += 1
        num_line_s, lex, tok = get_current_lexeme(num_row_s)
        factor_type = parse_expression()
        parse_token(')', 'brack_op', '')
        num_row_s -= 1
    num_row_s += 1
    return factor_type


def parse_return():
    global num_row_s, num_line_s
    num_row_s += 1
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    if lex in table_of_id.keys() or tok in allowed_data_types or lex == 'iota' or lex == 'nil' or lex == 'true' or lex == 'false':
        num_row_s += 1
        num_line_s, lex, tok = get_current_lexeme(num_row_s)
    else:
        fail_parse("return", (num_line_s, tok, lex))


def parse_package():
    global num_row_s, num_line_s
    num_row_s += 1
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    parse_identlist(lex)


def parse_import():
    global num_row_s, num_line_s
    num_row_s += 1
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    if tok == 'string':
        parse_token(lex, tok, num_line_s)
    else:
        fail_parse('очікувався рядок', (num_line_s, lex, tok))


# def parse_bool_expr():
#     global num_row_s, num_line_s
#     num_line_s, lex, tok = get_current_lexeme(num_row_s)
#     while(tok != 'rel_op'):
#         num_row_s += 1
#         num_line_s, lex, tok = get_current_lexeme(num_row_s)
#     if tok in 'rel_op':
#         num_row_s += 1
#     else:
#         fail_parse('невiдповiднiсть токенiв', (num_line_s, lex, tok))
#     num_line_s, lex, tok = get_current_lexeme(num_row_s)
#     while tok != 'brack_op' and tok != 'punc':
#         num_row_s += 1
#         num_line_s, lex, tok = get_current_lexeme(num_row_s)
#     num_line_s, lex, tok = get_current_lexeme(num_row_s)


def parse_if():
    global num_row_s, num_line_s
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    if lex == 'if' and tok == 'keyword':
        num_row_s += 1
        if parse_expression() != 'boolean':
            fail_parse('очікувався булевий вираз', num_line_s)
        parse_token('{', 'brack_op','')
        num_line_s, lex, tok = get_current_lexeme(num_row_s)
        parse_statementlist()
        num_line_s, lex, tok = get_current_lexeme(num_row_s)
        parse_token('}','brack_op','')
        num_line_s, lex, tok = get_current_lexeme(num_row_s)
        if lex == 'else' and tok == 'keyword':
            parse_token('else', 'keyword','')
            parse_token('{', 'brack_op','')
            parse_statementlist()
            parse_token('}', 'brack_op','')
    else:
        fail_parse('невiдповiднiсть токенiв', (num_line_s, lex, tok))


def parse_for():
    global num_row_s, num_line_s
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    back = 0
    i = 0
    while lex != '{':
        num_line_s, lex, tok = get_current_lexeme(num_row_s)
        num_row_s += 1
        back+=1
        if lex == ';':
            i+=1
    num_row_s -= back
    if i == 2:
        parse_declarlist()
        parse_token(';', 'punc', '')
        if parse_expression() != 'boolean':
            fail_parse('очікувався булевий вираз', num_line_s)
        parse_token(';', 'punc', '')
        parse_arithm_expression()
        num_line_s, lex, tok = get_current_lexeme(num_row_s)
        while lex != '{':
            num_row_s += 1
            num_line_s, lex, tok = get_current_lexeme(num_row_s)
    else:
        num_row_s += 1
        if parse_expression() != 'boolean':
            fail_parse('очікувався булевий вираз', num_line_s)
    parse_token('{', 'brack_op', '')
    parse_statementlist()
    parse_token('}', 'brack_op', '')


def get_current_lexeme (num_row) :
    num_line, lexeme, token, _ = table_of_symb[num_row]
    return num_line, lexeme, token


def fail_parse(str, tuple):
    if str == 'неочiкуваний кiнець програми':
        (lexeme, token, num_row) = tuple
        print('\033[91mParser ERROR: \n\t Неочiкуваний кiнець програми - в таблицi символiв (розбору) немає запису з номером {1}.\n\t Очiкувалось - {0}\033[0m'.format((lexeme, token), num_row))
        exit(1001)
    elif str == 'невiдповiднiсть токенiв':
        (num_line, lexeme, token, lex, tok) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} неочiкуваний елемент ({1}, {2}). \n\t Очiкувався - ({3},{4})'.format(num_line, lexeme, token, lex, tok))
        exit(1)
    elif str == 'очікувався ідентифікатор':
        (num_line, lexeme, token) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} неочiкуваний елемент ({1}, {2}). \n\t Очікувався ідентифікатор'.format(
            num_line, lexeme, token))
        exit(2)
    elif str == 'очікувався рядок':
        (num_line, lexeme, token) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} неочiкуваний елемент ({1}, {2}). \n\t Очікувався рядок'.format(
            num_line, lexeme, token))
        exit(3)
    elif str == 'очікувався параметр':
        (num_line, lexeme, token) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} неочiкуваний елемент ({1}, {2}). \n\t '
              'Очікувався ідентифікатор як параметр функції'.format(num_line, lexeme, token))
        exit(4)
    elif str == 'оголошення змінної чи константи без var/const':
        (num_line) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} очікується var/const'.format(num_line))
        exit(5)
    elif str == 'return':
        (num_line, lexeme, token) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} неочікуваний елемент ({1}, {2})'.format(num_line, lexeme, token))
        exit(6)
    elif str == 'не дозволений тип даних':
        (num_line, lexeme, token) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} неочiкуваний елемент ({1}, {2})'.format(num_line, lexeme, token))
        exit(7)
    elif str == 'присвоювання':
        (num_line, lexeme, token) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} неочiкуваний елемент ({1}, {2}). Очікується присвоювання (:=)'.format(num_line, lexeme, token))
        exit(8)
    elif str == 'не оголошена змінна':
        (num_line, lexeme, token) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} не оголошена змінна ({1}, {2})'.format(num_line, lexeme, token))
        exit(9)
    elif str == 'не закрита кругла дужка':
        (num_line, lexeme, token) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} не закрита кругла дужка'.format(num_line))
        exit(10)
    elif str == 'неможливо визначити тип':
        (num_line, lexeme, token) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} неможливо визначити тип змінної ({1}, {2}) '
              'без присвоєння значення'.format(num_line, lexeme, token))
        exit(11)
    elif str == 'значення змінної не відповідає оголошеному типу':
        (num_line, lexeme, token) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} значення змінної ({1}, {2}) '
              'не відповідає оголошеному типу '.format(num_line, lexeme, token))
        exit(12)
    elif str == 'ділення на нуль':
        (num_line, lexeme, token) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} відбувається ділення на нуль ({1}, {2})'
              .format(num_line, lexeme, token))
        exit(13)
    elif str == 'повторне оголошення змінної':
        (num_line, lexeme, token) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} повторне оголошення змінної ({1}, {2})'
              .format(num_line, lexeme, token))
        exit(14)
    elif str == 'не присвоєно значення константі':
        (num_line, lexeme, token) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} не присвоєно значення константі ({1}, {2})'
              .format(num_line, lexeme, token))
        exit(15)
    elif str == 'використання undefined змінної':
        (num_line, lexeme, token) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} використана змінна ({1}, {2}) до присвоєння значення'
              .format(num_line, lexeme, token))
        exit(16)
    elif str == 'невідповідність типів':
        (num_line, left_type, right_type) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} невідповідність типів {1} і {2}'
              .format(num_line, left_type, right_type))
        exit(17)
    elif str == 'арифметична дія над стрічкою':
        (num_line, lexeme, token) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} арифметична дія над стрічкою ({1}, {2})'
              .format(num_line, lexeme, token))
        exit(18)
    elif str == 'неможливо виконати порівняння':
        (num_line, lexeme, token) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} неможливо виконати порівняння типів {1} і {2}'
              .format(num_line, lexeme, token))
        exit(19)
    elif str == 'переприсвоєння значення константі':
        (num_line, lexeme, token) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} переприсвоюється значення констаниті ({1}, {2}), що неможливо'
              .format(num_line, lexeme, token))
        exit(20)
    elif str == 'очікувався булевий вираз':
        (num_line) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} очікувався булевий вираз'.format(num_line))
        exit(22)
    elif str == '':
        (num_line, lexeme, token) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} неочiкуваний елемент ({1}, {2})'.format(num_line, lexeme, token))
        exit(22)


parse_program()


print('\033[0m')
print('-' * 30)
print('table_of_var: {0}'.format(table_of_var))
print('-' * 30)
print('table_of_named_const: {0}'.format(table_of_named_const))
print('-' * 30)

# -------------------------------------------------------
# code generation
# -------------------------------------------------------

