# Tovid language lexer and parser
from postfixMachine import PSM

token_table = {'true': 'boolean', 'false': 'boolean', 'const': 'keyword', 'var': 'keyword', 'func': 'keyword',
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
# united_table_var_named_const = {}
table_of_labels = {}
bool_expr_results = ('true', 'false')

state = init_state

file_name = input('Введіть файл (без .tovid): ')
f = open(f'{file_name}.tovid', 'r')
source_code = f.read()
f.close()

f_success = (False, 'Lexer')

len_code = len(source_code)-1
num_line = 1
num_char = -1
current_lex_id = 1
current_line = 1
char = ''
lexeme = ''

params_types = {'nil': 'keyword', 'int': 'keyword', 'float': 'keyword', 'complex': 'keyword',
                'string': 'keyword', 'boolean': 'keyword'}

allowed_data_types = ['int', 'float', 'complex', 'string', 'boolean']

pm = PSM(file_name)
postfix_code = []


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
        f_success = (True, 'Lexer')
        return f_success
    except SystemExit as error:
        f_success = (False, 'Lexer')
        print('\n\033[0m\033[1m\033[4mLexer\033[0m: \033[91mАварійне завершення програми з кодом {0}\033[0m'.format(error))
        return f_success


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
                print('{0:<3d} {1:<10s} {2:<10s} '.format(num_line, lexeme, token))
                table_of_symb[len(table_of_symb)+1] = (num_line, lexeme, token, '')
            lexeme = ''
            num_char = put_char_back(num_char)  # зiрочка
            state = init_state
        elif state in F_error:  # (101, 102, 103): # ERROR
            fail()
        else:
            lexeme += char
            token = get_token(state, lexeme)
            if token == 'string':
                lexeme = lexeme.replace('"', '')
            print('{0:<3d} {1:<10s} {2:<10s} '.format(num_line, lexeme, token))
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


# lex()
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
len_table_of_symb = len(table_of_symb)


def parse_program():
    global current_lex_id, current_line, f_success
    try:
        while current_lex_id < len_table_of_symb:
            current_line, lex, tok = get_current_lexeme(current_lex_id)
            if lex == 'func':
                parse_func()
            elif lex == 'import':
                parse_import()
            elif lex == '//' or lex == '/*':
                parse_comment(current_line)
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
                    fail_parse('оголошення змінної чи константи без var/const', (current_line, lex, tok))
            else:
                parse_statementlist()
        print("\n\033[0m\033[1m\033[4mParser\033[0m: \033[92mСинтаксичний і семантичний аналiз завершився успiшно\033[0m")
        f_success = (True, 'Parser')
        return f_success
    except SystemExit as e:
        print("\n\033[0m\033[1m\033[4mParser\033[0m: \033[91mАварiйне завершення програми з кодом {0}\033[0m".format(e))
        # f_success = (False, 'Parser')
        # return f_success


def parse_func():
    global current_lex_id, current_line, table_of_var
    current_lex_id += 1
    current_line, lex, tok = get_current_lexeme(current_lex_id)
    parse_identlist(lex)
    current_line, lex, tok = get_current_lexeme(current_lex_id)
    parse_token('(', tok, current_lex_id)
    current_line, lex, tok = get_current_lexeme(current_lex_id)
    parse_token(')', tok, current_lex_id)
    parse_token('{', tok, current_lex_id)
    parse_statementlist()
    parse_token('}', tok, current_lex_id)
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
    global current_lex_id, current_line
    if current_lex_id <= len_table_of_symb:
        current_line, lex, tok = get_current_lexeme(current_lex_id)
        current_lex_id += 1
        if (lex, tok) == (lexeme, token):
            # print('parseToken: В рядку {0} токен {1}'.format(num_line_s, (lexeme, token)))
            return True
        else:
            fail_parse('невiдповiднiсть токенiв', (current_line, lex, tok, lexeme, token))
            return False
    else:
        fail_parse("неочiкуваний кiнець програми", (lexeme, token, current_lex_id))


def parse_identlist(lexeme):
    global current_lex_id
    if lexeme in table_of_id.keys():
        current_lex_id += 1
    else:
        num_line_s, lex, tok = get_current_lexeme(current_lex_id)
        fail_parse('очікувався ідентифікатор', (num_line_s, lex, tok))


def parse_comment(comment_line):
    global current_lex_id, current_line
    current_line, lex, tok = get_current_lexeme(current_lex_id)
    if lex == '//':
        while current_line == comment_line:
            current_lex_id += 1
            current_line, lex, tok = get_current_lexeme(current_lex_id)
        current_lex_id -= 1
    elif lex == '/*':
        while lex != '*/':
            current_lex_id += 1
            current_line, lex, tok = get_current_lexeme(current_lex_id)
    current_lex_id += 1


# зарарз працює як тіло функції/іф/фор.
# пофіксити, щоб можна було без вкладеності парсити теж (не чекати на '}')
def parse_statementlist():
    global current_lex_id, current_line

    current_line, lex, tok = get_current_lexeme(current_lex_id)
    while lex != '}':
        if lex == '//' or lex == '/*':
            parse_comment(current_line)
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
            if lex in table_of_var.keys() or lex in table_of_named_const.keys():  # declared_var сама заборонить переприсвоєння константи
                parse_declared_var(lex, tok)
            else:
                fail_parse('оголошення змінної чи константи без var/const', (current_line, lex, tok))
        else:
            # print("непередбачена логіка у функції parse_statementlist()")
            fail_parse('return', (current_line, lex, tok))
        current_line, lex, tok = get_current_lexeme(current_lex_id)


def parse_declared_var(lexeme, token):
    global current_lex_id, current_line
    current_line, lex, tok = get_current_lexeme(current_lex_id)
    ident_line = current_line
    postfix_code_gen('lval', (lex, tok))
    if lexeme in table_of_var.keys():
        current_lex_id += 1
        parse_token(':=', 'assign_op', current_lex_id)
        new_type = parse_expression()
        postfix_code_gen(':=', (':=', 'assign_op'))
        index, old_type, _ = table_of_var[lexeme]
        if new_type == old_type:
            table_of_var[lexeme] = (index, old_type, 'assigned')
            # united_table_var_named_const[lexeme] = (index, old_type, 'variable', 'assigned')
        else:
            fail_parse('значення змінної не відповідає оголошеному типу', (ident_line, lexeme, token))
    elif lexeme in table_of_named_const.keys():
        fail_parse('переприсвоєння значення константі', (current_line, lex, tok))
    else:
        fail_parse("не оголошена змінна", (current_line, lex, tok,))


def parse_scanf_print(lexeme, token):
    global current_line, current_lex_id, table_of_var
    current_lex_id += 1
    current_line, lex, tok = get_current_lexeme(current_lex_id)
    parse_token('(', tok, current_lex_id)
    current_line, lex, tok = get_current_lexeme(current_lex_id)
    if lex != ')':
        current_line, lex, tok = get_current_lexeme(current_lex_id)
        _, lex1, tok1 = get_current_lexeme(current_lex_id + 1)
        if lexeme == 'scanf':
            if lex in table_of_var.keys():  # зчитувати для переприсвоєння можна лише змінну
                postfix_code_gen('lval', (lex, 'lval'))
                postfix_code_gen('in_op', ('IN', 'in_op'))
                current_lex_id += 1
                current_line, lex, tok = get_current_lexeme(current_lex_id)
                # table_of_var[lex] = (index, old_type, 'assigned')  # буде виконано на PSM
                # в таблиці змінних зробити присвоєння до змінної таке, що було отримано зі скану
            else:
                fail_parse('очікувався параметр', (current_line, lex, tok))
            while lex == ',':
                _, lex1, tok1 = get_current_lexeme(current_lex_id + 1)
                if lex1 in table_of_var.keys():
                    postfix_code_gen('lval', (lex1, 'lval'))
                    postfix_code_gen('in_op', ('IN', 'in_op'))
                    current_lex_id += 2
                    current_line, lex, tok = get_current_lexeme(current_lex_id)
                else:
                    fail_parse('очікувався параметр', (current_line, lex1, tok1))
        elif lexeme == 'print':  # else:
            if lex in table_of_var.keys() or lex in table_of_named_const.keys() or tok in allowed_data_types:
                if lex in table_of_var.keys():
                    if table_of_var[lex][2] == 'undefined':
                        fail_parse('використання undefined змінної', (current_line, lex, tok))
                if tok in allowed_data_types and lex not in table_of_var.keys() and lex not in table_of_named_const.keys():
                    postfix_code_gen(tok, (lex, tok))
                else:
                    postfix_code_gen('rval', (lex, 'rval'))
                postfix_code_gen('out_op', ('OUT', 'out_op'))
                current_lex_id += 1
                current_line, lex, tok = get_current_lexeme(current_lex_id)
            else:
                fail_parse('очікувався параметр', (current_line, lex, tok))
            while lex in (',', '+'):
                _, lex1, tok1 = get_current_lexeme(current_lex_id + 1)
                if lex1 in table_of_var.keys() or lex1 in table_of_named_const.keys() or tok1 in allowed_data_types:
                    if lex1 in table_of_var.keys():
                        if table_of_var[lex1][2] == 'undefined':
                            fail_parse('використання undefined змінної', (current_line, lex1, tok1))
                else:
                    fail_parse('очікувався параметр', (current_line, lex1, tok1))
                if tok1 in allowed_data_types and lex1 not in table_of_var.keys() and lex1 not in table_of_named_const.keys():
                    postfix_code_gen(tok1, (lex1, tok1))
                else:
                    postfix_code_gen('rval', (lex1, 'rval'))
                postfix_code_gen('out_op', ('OUT', 'out_op'))
                current_lex_id += 2
                current_line, lex, tok = get_current_lexeme(current_lex_id)
    parse_token(')', tok, current_lex_id)


def parse_declarlist():
    global current_lex_id
    datatype_is_declared = False
    num_line_s, lex, tok = get_current_lexeme(current_lex_id)
    keyword = lex
    current_lex_id += 1
    num_line_s, lex, tok = get_current_lexeme(current_lex_id)
    lType = ''
    rType = ''
    if lex in allowed_data_types:
        declared_datatype = lex
        current_lex_id += 1
        num_line_s, lex, tok = get_current_lexeme(current_lex_id)
        datatype_is_declared = True
        lType = declared_datatype
        # postfix_code_gen('lval', (lex, tok))
    elif lex in table_of_id.keys():
        datatype_is_declared = False
    else:
        fail_parse("не дозволений тип даних", (num_line_s, lex, tok))
    if lex in table_of_id.keys():
        if lex in table_of_var.keys() or lex in table_of_named_const.keys():
            fail_parse('повторне оголошення змінної або константи',(num_line_s, lex, tok))
        current_id = lex
        current_token = tok
        current_lex_id += 1
        num_line_s, lex, tok = get_current_lexeme(current_lex_id)
        index = len(table_of_var) + 1 if keyword == 'var' else len(table_of_named_const) + 1
        if tok == 'assign_op':
            postfix_code_gen('lval', (current_id, current_token))
            current_lex_id += 1
            value_datatype = parse_expression()
            postfix_code_gen(':=', (':=', 'assign_op'))
            if datatype_is_declared:
                if declared_datatype == value_datatype:
                    if keyword == 'var' or keyword == 'for':
                        table_of_var[current_id] = (index, declared_datatype, 'assigned')
                        # united_table_var_named_const[current_id] = (index, declared_datatype, 'variable', 'assigned')
                    else:
                        table_of_named_const[current_id] = (index, declared_datatype)
                        # united_table_var_named_const[current_id] = (index, declared_datatype, 'const', 'assigned')
                else:
                    fail_parse('значення змінної не відповідає оголошеному типу', (num_line_s, current_id, 'ident'))
            else:
                if keyword == 'var' or keyword == 'for':
                    table_of_var[current_id] = (index, value_datatype, 'assigned')
                else:
                    table_of_named_const[current_id] = (index, value_datatype)
        else:
            if keyword == 'const':
                current_lex_id -= 1
                num_line_s, lex, tok = get_current_lexeme(current_lex_id)
                fail_parse('не присвоєно значення константі', (num_line_s, lex, tok))
            if not datatype_is_declared:
                current_lex_id -= 1
                num_line_s, lex, tok = get_current_lexeme(current_lex_id)
                fail_parse("неможливо визначити тип", (num_line_s, lex, tok))
            else:
                if keyword == 'var' or keyword == 'for':
                    table_of_var[current_id] = (index, declared_datatype, 'undefined')
                    # united_table_var_named_const[current_id] = (index, declared_datatype, 'variable', 'undefined')
                else:
                    table_of_named_const[current_id] = (index, declared_datatype)
                    # united_table_var_named_const[current_id] = (index, declared_datatype, 'const', 'assigned')
    else:
        fail_parse("очікувався ідентифікатор", (num_line_s, lex, tok))


# тут якось потрібно слідкувати щоб була послідовність між змінними і знаками (а + м) * 12 > 3
def parse_expression():
    global current_lex_id, current_line
    current_line, lex, tok = get_current_lexeme(current_lex_id)

    if lex in bool_expr_results:
        left_type = 'boolean'
        current_lex_id += 1
        postfix_code.append((lex, tok))
        finish = True
    else:
        left_type = parse_arithm_expression()
        try:
            current_line, lex, tok = get_current_lexeme(current_lex_id)
        except KeyError:
            finish = True
        else:
            finish = False
    result_type = left_type

    while not finish:
        try:
            current_line, lex, tok = get_current_lexeme(current_lex_id)
        except KeyError:
            finish = True
        else:
            if tok == 'rel_op':
                rel_op = lex
                current_lex_id += 1
                right_type = parse_arithm_expression()
                if not (left_type == 'string' or right_type == 'string' or left_type == 'complex' or right_type == 'complex'):
                    result_type = 'boolean'
                else:
                    fail_parse('неможливо виконати порівняння', (current_line, left_type, right_type))
                postfix_code_gen(rel_op, (rel_op, 'rel_op'))
            else:
                finish = True
    return result_type


def parse_arithm_expression():
    global current_lex_id, current_line
    current_line, lex, tok = get_current_lexeme(current_lex_id)
    unary_sign_present = False
    if tok == 'add_op':
        unary_sign_present = True
        unary_sign = lex
        current_lex_id += 1

    left_type = parse_term()
    result_type = left_type
    if unary_sign_present:
        postfix_code_gen(unary_sign, (unary_sign, 'unary_op'))
    finish = False

    while not finish:
        try:
            current_line, lex, tok = get_current_lexeme(current_lex_id)
        except KeyError:
            finish = True
        else:
            if tok == 'add_op':
                add_op = lex
                current_lex_id += 1
                right_type = parse_term()
                if left_type == right_type and left_type == 'int':
                    result_type = left_type
                elif left_type == 'boolean' or right_type == 'boolean':
                    fail_parse('невідповідність типів', (current_line, left_type, right_type))
                elif left_type == 'string' or right_type == 'string':
                    fail_parse('арифметична дія над стрічкою', (current_line, lex, tok))
                elif left_type == 'complex' or right_type == 'complex':
                    result_type = 'complex'
                else:
                    result_type = 'float'
                postfix_code_gen(add_op, (add_op, 'add_op'))
            else:
                finish = True
    return result_type


def parse_term():
    global current_lex_id, current_line
    current_line, lex, tok = get_current_lexeme(current_lex_id)
    left_type = parse_chunk()
    result_type = left_type
    finish = False

    while not finish:
        try:
            current_line, lex, tok = get_current_lexeme(current_lex_id)
        except KeyError:
            finish = True
        else:
            if tok == 'mult_op':
                operator = lex
                current_lex_id += 1
                current_line, lex, tok = get_current_lexeme(current_lex_id)
                right_type = parse_chunk()
                if left_type == 'boolean' or right_type == 'boolean':
                    fail_parse('невідповідність типів', (current_line, left_type, right_type))
                elif left_type == 'string' or right_type == 'string':
                    fail_parse('арифметична дія над стрічкою', (current_line, lex, tok))
                postfix_code_gen(operator, (operator, 'mult_op'))

                if operator == '/':
                    result_type = 'float'
                    if right_type == 'int':
                        lex = int(lex)
                    elif right_type == 'float':
                        lex = float(lex)
                    if not lex:
                        fail_parse('ділення на нуль', (current_line, lex, tok))
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
    global current_lex_id, current_line
    current_line, lex, tok = get_current_lexeme(current_lex_id)
    left_type = parse_factor()
    result_type = left_type
    finish = False

    while not finish:
        try:
            current_line, lex, tok = get_current_lexeme(current_lex_id)
        except KeyError:
            finish = True
        else:
            if tok == 'pow_op':
                current_lex_id += 1
                right_type = parse_chunk()
                if left_type == 'boolean' or right_type == 'boolean':
                    fail_parse('невідповідність типів', (current_line, left_type, right_type))
                elif left_type == 'string' or right_type == 'string':
                    fail_parse('арифметична дія над стрічкою', (current_line, lex, tok))
                result_type = 'float'
                postfix_code_gen('^', ('^', 'pow_op'))
            else:
                finish = True
    return result_type


def parse_factor():
    global current_lex_id, current_line
    current_line, lex, tok = get_current_lexeme(current_lex_id)
    factor_type = ''
    if lex in table_of_var.keys():
        if table_of_var[lex][2] == 'undefined':
            fail_parse('використання undefined змінної', (current_line, lex, tok))
        factor_type = table_of_var[lex][1]
        postfix_code_gen('rval', (lex, 'rval'))
    elif lex in table_of_named_const.keys():
        factor_type = table_of_named_const[lex][1]
        postfix_code_gen('rval', (lex, 'rval'))
    elif lex in table_of_const.keys():
        factor_type = table_of_const[lex][0]
        postfix_code_gen('const', (lex, tok))
    elif tok == 'string':
        factor_type = 'string'
        postfix_code_gen('string', (lex, tok))
        # все одно вилетить на функції parse_chunk()
    elif lex in bool_expr_results:
        factor_type = 'boolean'
        postfix_code_gen('boolean', (lex, tok))
        # все одно вилетить на функції parse_chunk()
    elif lex == '(':
        current_lex_id += 1
        current_line, lex, tok = get_current_lexeme(current_lex_id)
        factor_type = parse_expression()
        parse_token(')', 'brack_op', '')
        current_lex_id -= 1
    current_lex_id += 1
    return factor_type


def parse_return():
    global current_lex_id, current_line
    current_lex_id += 1
    current_line, lex, tok = get_current_lexeme(current_lex_id)
    if lex in table_of_id.keys() or tok in allowed_data_types or lex == 'iota' or lex == 'nil' or lex == 'true' or lex == 'false':
        current_lex_id += 1
        current_line, lex, tok = get_current_lexeme(current_lex_id)
    else:
        fail_parse("return", (current_line, tok, lex))


def parse_package():
    global current_lex_id, current_line
    current_lex_id += 1
    current_line, lex, tok = get_current_lexeme(current_lex_id)
    parse_identlist(lex)


def parse_import():
    global current_lex_id, current_line
    current_lex_id += 1
    current_line, lex, tok = get_current_lexeme(current_lex_id)
    if tok == 'string':
        parse_token(lex, tok, current_line)
    else:
        fail_parse('очікувався рядок', (current_line, lex, tok))


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
    global current_lex_id, current_line
    current_line, lex, tok = get_current_lexeme(current_lex_id)
    if lex == 'if' and tok == 'keyword':
        current_lex_id += 1
        if parse_expression() != 'boolean':
            fail_parse('очікувався булевий вираз', current_line)
        parse_token('{', 'brack_op','')
        current_line, lex, tok = get_current_lexeme(current_lex_id)
        m1 = create_label()
        postfix_code.append(m1)  # Трансляцiя
        postfix_code.append(('JF', 'jf'))
        parse_statementlist()
        current_line, lex, tok = get_current_lexeme(current_lex_id)
        parse_token('}','brack_op','')
        current_line, lex, tok = get_current_lexeme(current_lex_id)
        if lex == 'else' and tok == 'keyword':
            parse_token('else', 'keyword','')
            parse_token('{', 'brack_op','')
            m2 = create_label()
            postfix_code.append(m2)  # Трансляцiя
            postfix_code.append(('JMP', 'jump'))
            set_value_label(m1)  # в табл. мiток
            postfix_code.append(m1)
            postfix_code.append((':', 'colon'))
            parse_statementlist()
            parse_token('}', 'brack_op','')
            set_value_label(m2)  # в табл. мiток
            postfix_code.append(m2)  # Трансляцiя
            postfix_code.append((':', 'colon'))

        else:
            set_value_label(m1)  # в табл. мiток
            postfix_code.append(m1)
            postfix_code.append((':', 'colon'))

    else:
        fail_parse('невiдповiднiсть токенiв', (current_line, lex, tok))


# def parse_for():
#     global current_lex_id, current_line
#     current_line, lex, tok = get_current_lexeme(current_lex_id)
#     back = 0
#     i = 0
#     while lex != '{':
#         current_line, lex, tok = get_current_lexeme(current_lex_id)
#         current_lex_id += 1
#         back+=1
#         if lex == ';':
#             i+=1
#     current_lex_id -= back
#     if i == 2:
#         parse_declarlist()
#         parse_token(';', 'punc', '')
#         if parse_expression() != 'boolean':
#             fail_parse('очікувався булевий вираз', current_line)
#         parse_token(';', 'punc', '')
#         parse_arithm_expression()
#         current_line, lex, tok = get_current_lexeme(current_lex_id)
#         while lex != '{':
#             current_lex_id += 1
#             current_line, lex, tok = get_current_lexeme(current_lex_id)
#     else:
#         current_lex_id += 1
#         if parse_expression() != 'boolean':
#             fail_parse('очікувався булевий вираз', current_line)
#     parse_token('{', 'brack_op', '')
#     parse_statementlist()
#     parse_token('}', 'brack_op', '')


def parse_for():
    global current_lex_id, current_line
    current_line, lex, tok = get_current_lexeme(current_lex_id)
    back = 0
    i = 0
    znak = ''
    znak_2 = ''
    start_znach = 0
    last_znach = 0
    variable_name = ''
    to_do = 0
    step = 0

    while lex != '{':
        if i == 0 and lex == ':=':
            current_line, lex, tok = get_current_lexeme(current_lex_id-2)
            variable_name = lex
            current_line, lex, tok = get_current_lexeme(current_lex_id)
            start_znach = int(lex)
        if i == 1 and tok == 'rel_op':
            current_line, lex, tok = get_current_lexeme(current_lex_id-1)
            znak = lex
            current_line, lex, tok = get_current_lexeme(current_lex_id-2)
            if lex == variable_name:
                current_line, lex, tok = get_current_lexeme(current_lex_id)
                to_do = int(lex)

        if i == 2 and lex==':=':
            current_line, lex, tok = get_current_lexeme(current_lex_id+1)
            znak_2 = lex
            current_line, lex, tok = get_current_lexeme(current_lex_id+2)
            step = int(lex)

        current_line, lex, tok = get_current_lexeme(current_lex_id)
        current_lex_id += 1
        back += 1
        if lex == ';':
            i += 1

    current_lex_id -= back
    if znak_2 == '+':
        last_znach = start_znach + to_do * step
    if znak_2 == '-':
        last_znach = start_znach - (start_znach - to_do) * step

    if i == 2:
        m1 = create_label()
        m2 = create_label()
        m3 = create_label()

        postfix_code.append(m1)  # Трансляцiя
        postfix_code.append(('JMP', 'jump'))  # 1
        set_value_label(m1)  # в табл. мiток
        postfix_code.append(m1)  # Трансляцiя
        postfix_code.append((':', 'colon'))  # 1
        parse_declarlist()
        parse_token(';', 'punc', '')
        if parse_expression() != 'boolean':
            fail_parse('очікувався булевий вираз', current_line)
        postfix_code.append(m3)  # Трансляцiя
        postfix_code.append(('JF', 'jf'))  # 3
        parse_arithm_expression()
        postfix_code.append(m2)  # Трансляцiя
        postfix_code.append(('JMP', 'jump'))  # 2
        set_value_label(m2)  # в табл. мiток
        postfix_code.append(m2)  # Трансляцiя
        postfix_code.append((':', 'colon'))  # 2
        current_line, lex, tok = get_current_lexeme(current_lex_id)
        if znak == '<' or znak == '<=':
            k = 0
            while lex != '{':
                k += 1
                current_line, lex, tok = get_current_lexeme(current_lex_id)
                current_lex_id += 1

            for i in range(start_znach,last_znach):
                if i == start_znach:
                    current_lex_id -= k
                else:
                    current_lex_id -= k - 1
                current_line, lex, tok = get_current_lexeme(current_lex_id)
                parse_declared_var(lex, tok)

        else:
            k = 0
            while lex != '{':
                k += 1
                current_line, lex, tok = get_current_lexeme(current_lex_id)
                current_lex_id+=1

            for i in range(last_znach, start_znach):
                if i == last_znach:
                    current_lex_id -= k
                else:
                    current_lex_id -= k-1
                current_line, lex, tok = get_current_lexeme(current_lex_id)
                parse_declared_var(lex, tok)

        postfix_code.append(m3)  # Трансляцiя
        postfix_code.append(('JMP', 'jump'))  # 3

        parse_token('{', 'brack_op', '')

        if znak == '<' or znak == '<=':
            for i in range(start_znach,last_znach):
                parse_statementlist()
                print('1----z')

        else:
            for i in range(last_znach,start_znach):
                parse_statementlist()
                print('2----z')

        parse_token('}', 'brack_op', '')
        postfix_code.append(m1)  # Трансляцiя
        postfix_code.append(('JMP', 'jump'))  # 1
        set_value_label(m3)  # в табл. мiток
        postfix_code.append(m3)  # Трансляцiя
        postfix_code.append((':', 'colon'))  # 3


def get_current_lexeme(num_row):
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
    elif str == 'повторне оголошення змінної або константи':
        (num_line, lexeme, token) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} повторне оголошення змінної або константи ({1}, {2})'
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
        exit(21)
    elif str == '':
        (num_line, lexeme, token) = tuple
        print('\033[91mParser ERROR: \n\t В рядку {0} неочiкуваний елемент ({1}, {2})'.format(num_line, lexeme, token))
        exit(22)


# parse_program()
# print('\033[0m')
# print('-' * 30)
# print('table_of_var: {0}'.format(table_of_var))
# print('-' * 30)
# print('table_of_named_const: {0}'.format(table_of_named_const))
# print('-' * 30)


# -------------------------------------------------------
# code generation
# -------------------------------------------------------


def serv():
    print(f"pm1.tableOfVar:\n {pm.tableOfVar}\n")
    print(f"pm1.tableOfLabel:\n {pm.tableOfLabel}\n")
    print(f"pm1.tableOfConst:\n {pm.tableOfConst}\n")
    print(f"pm1.tableOfNamedConst:\n {pm.tableOfNamedConst}\n")
    print(f"pm1.postfixCode:\n {pm.postfixCode}\n")
    # print(postfix_code)


# Виклик функцiї savepostfix_code() приводить до побудови постфiкс-коду
#  i виведення на консоль iнформацiї
def save_postfix_code():
    global file_name
    try:
        with open(f"{file_name}.postfix", 'w') as file:
            section = '.target: Postfix Machine\n'
            file.write(section)
            section = '.version: 0.0.1\n\n'
            file.write(section)

            section = '.vars(\n'
            identifiers = [i for i in table_of_var.keys()]
            datatypes = [j[1] for j in table_of_var.values()]
            vars_for_postfix = []
            for i in range(len(identifiers)):
                vars_for_postfix.append((identifiers[i], datatypes[i]))
            # print('\n', vars_for_postfix, '\n')
            try:
                column_width = max(len(word) for row in vars_for_postfix for word in row)  # padding
            except ValueError:
                column_width = 5
            for row in vars_for_postfix:
                section += '\t' + ''.join(word.ljust(column_width) for word in row) + '\n'
            section += ')\n\n'
            file.write(section)

            section = '.constants(\n'
            identifiers = [i for i in table_of_const.keys()]
            datatypes = [j[0] for j in table_of_const.values()]
            consts_for_postfix = []
            for i in range(len(identifiers)):
                consts_for_postfix.append((identifiers[i], datatypes[i]))
            # print('\n', consts_for_postfix, '\n')
            try:
                column_width = max(len(word) for row in consts_for_postfix for word in row)  # padding
            except ValueError:
                column_width = 5
            for row in consts_for_postfix:
                section += '\t' + ''.join(word.ljust(column_width) for word in row) + '\n'
            section += ')\n\n'
            file.write(section)

            section = '.named_constants(\n'
            identifiers = [i for i in table_of_named_const.keys()]
            datatypes = [j[1] for j in table_of_named_const.values()]
            named_consts_for_postfix = []
            for i in range(len(identifiers)):
                named_consts_for_postfix.append((identifiers[i], datatypes[i]))
            # print('\n', named_consts_for_postfix, '\n')
            try:
                column_width = max(len(word) for row in named_consts_for_postfix for word in row) + 1  # padding
            except ValueError:
                column_width = 5
            for row in named_consts_for_postfix:
                section += '\t' + ''.join(word.ljust(column_width) for word in row) + '\n'
            section += ')\n\n'
            file.write(section)

            section = '.labels(\n'
            labels = []
            # element_index = [j[0] for j in table_of_const.values()]
            for pair_num in range(len(postfix_code)):
                if postfix_code[pair_num][1] != 'label':
                    pair_num += 1
                else:  # коли все-ж попадаємо на label
                    if postfix_code[pair_num+1][1] == 'colon':
                        labels.append((postfix_code[pair_num][0], pair_num))
                    else:
                        pair_num += 1

            # consts_for_postfix = []
            # for i in range(len(identifiers)):
            #     consts_for_postfix.append((identifiers[i], datatypes[i]))
            # print('\n', labels, '\n')
            try:
                column_width = max(len(str(word)) for row in labels for word in row) + 3  # padding
            except ValueError:
                column_width = 5
            for row in labels:
                section += '\t' + ''.join(str(word).ljust(column_width) for word in row) + '\n'
            section += ')\n\n'
            file.write(section)

            section = '.code(\n'
            # labels = []
            # element_index = [j[0] for j in table_of_const.values()]
            # for pair_num in range(len(postfix_code)):
            #     if postfix_code[pair_num][1] != 'label':
            #         pair_num += 1
            #     else:  # коли все-ж попадаємо на label
            #         if postfix_code[pair_num + 1][1] == 'colon':
            #             labels.append((postfix_code[pair_num][0], pair_num))
            #         else:
            #             pair_num += 1

            # consts_for_postfix = []
            # for i in range(len(identifiers)):
            #     consts_for_postfix.append((identifiers[i], datatypes[i]))
            # print('\n', postfix_code, '\n')

            try:
                column_width = max(len(word) for row in postfix_code for word in row)  # padding
            except ValueError:
                column_width = 5
            for row in postfix_code:
                section += '\t' + ''.join(word.ljust(column_width) for word in row) + '\n'
            section += ')\n\n'
            file.write(section)


            # file.write('\n\n')
            # file.write(str(postfix_code))  # тимчасово записую туди сам список
        print(f"\nPostfix code збережено до файлу {file_name}.postfix")
    except Exception as e:
        print(f"Помилка при збережені файлу: {e}")


def postfix_code_gen(case, to_tran):
    if case == 'lval':
        lex, tok = to_tran
        postfix_code.append((lex, 'l-val'))
    elif case == 'rval':
        lex, tok = to_tran
        postfix_code.append((lex, 'r-val'))
    else:
        lex, tok = to_tran
        postfix_code.append((lex, tok))


def compile_to_postfix():
    global len_table_of_symb, f_success, table_of_symb
    f_success = lex()
    if f_success == (True, 'Lexer'):
        f_success = (False, 'Parser')
        len_table_of_symb = len(table_of_symb)
        f_success = parse_program()
        if f_success == (True, 'Parser'):
            try:
                save_postfix_code()
            except SystemExit as error:
                f_success = (False, 'Compiler')
                print('\n\033[0m\033[1m\033[4mCompiler\033[0m: \033[91mАварійне завершення програми з кодом {0}\033[0m'.
                format(error))
            else:
                print('\n\033[0m\033[1m\033[4mCompiler\033[0m: \033[92mКомпіляція у постфікс завершена успішно\033[0m')
                f_success = (True, 'Compiler')
            # return f_success
    return f_success


def code_execution():
    global f_success
    f_success = compile_to_postfix()
    if f_success == (True, 'Compiler'):
        try:
            pm.load_postfix_file(file_name)
            pm.postfix_exec()
        except SystemExit as error:
            f_success = (False, 'Executor')
            print('\033[0m\033[1m\033[4mExecutor\033[0m: \033[91mАварійне завершення програми з кодом {0}\033[0m'.
                  format(error))
        else:
            serv()
            print('\033[0m\033[1m\033[4mExecutor\033[0m: \033[92mВиконання коду завершено успішно\033[0m')
            f_success = (True, 'Executor')
    return f_success


def set_value_label(label):
    global table_of_labels
    lex, tok = label
    table_of_labels[lex] = len(postfix_code)
    return True


def create_label():
    global table_of_labels
    number = len(table_of_labels)+1
    lexeme = "m" + str(number)
    value = table_of_labels.get(lexeme)
    if not value:
        table_of_labels[lexeme] = 'val_undef'
        tok = 'label'  # # #
    else:
        tok = 'Конфлiкт мiток'
        print(tok)
        exit(1003)
    return (lexeme, tok)


code_execution()  # compile_to_postfix() відбувається всередині


code = ""
code += '\tldstr ""\n'  # початковий вертикальний порожній рядок
code += '\tcall void [mscorlib]System.Console::WriteLine(string)\n'

def convert_to_CIL():
    global code
    label_name = ''
    prev = ''
    last_string = ''
    last_lval = ''
    for instr in postfix_code:
        val, tok = instr[0], instr[1]

        if tok == 'l-val':
            if val in table_of_var.keys():
                prev = table_of_var[val][1]
            elif val in table_of_named_const.keys():
                prev = table_of_named_const[val][1]
            code += f'\tldloca {val}\n'
            last_lval = val

        elif tok == 'r-val':
            if val in table_of_var.keys():
                var_named_const_type = table_of_var[val][1]
            elif val in table_of_named_const.keys():
                var_named_const_type = table_of_named_const[val][1]

            if var_named_const_type == 'string':
                last_string = val

            if var_named_const_type == 'float' and prev in ('int', 'intnum'):
                code += '\tconv.r4\n'
            elif var_named_const_type == 'int' and prev in ('float', 'floatnum'):
                code += '\tconv.i4\n'
            # elif var_named_const_type == 'boolean' and prev not in ('bool', 'boolean'):
            #     code += '\tldc.i4 1\n'
                # code += '\tceq\n'

            # if var_named_const_type == 'string':
            #     if prev not in ('string', 'stringval'):
            #         code += '\tcall instance string [mscorlib]System.Object::ToString()\n'

            # if var_named_const_type == 'string':
            #     code += f'\tldloc {val}\n'
            # elif var_named_const_type == 'boolean':
            #     print(val)
            #     code += f'\tldc.i4 {1 if val == "true" else 0}\n'
            # else:
            #     code += f'\tldloc {val}\n'
            code += f'\tldloc {val}\n'

            if var_named_const_type in ('int', 'intnum') and prev in ('float', 'floatnum'):
                code += '\tconv.r4\n'
            elif var_named_const_type in ('float', 'floatnum') and prev in ('int', 'intnum'):
                code += '\tconv.r4\n'

            prev = var_named_const_type

        elif tok in ('int', 'intnum'):
            code += f'\tldc.i4 {val}\n'
            if prev in ('float', 'floatnum'):
                code += '\tconv.r4\n'
                prev = 'float'
            else:
                prev = 'int'

        elif tok in ('float', 'floatnum'):
            if prev in ('int', 'intnum'):
                code += '\tconv.r4\n'

            code += f'\tldc.r4 {val}\n'

            prev = 'float'

        elif tok in ('string', 'stringval'):
            if prev in ('int', 'intnum', 'float', 'floatnum'):
                code += '\tbox [mscorlib]System.Int32\n'

            code += f'\tldstr "{val}"\n'

            prev = 'string'

        elif tok in ('boolval', 'boolean') and val == 'true':
            code += f'\tldc.i4 1\n'
            prev = 'boolean'

        elif tok in ('boolval', 'boolean') and val == 'false':
            code += f'\tldc.i4 0\n'
            prev = 'boolean'

        elif tok == 'assign_op':
            if prev in ('float', 'floatnum'):
                code += f'\tstind.r4\n'
            elif prev in ('int', 'intnum'):
                code += f'\tstind.i4\n'
            elif prev in ('boolean', 'boolval'):
                code += f'\tstind.i4\n'
            elif prev in ('string', 'stringval'):
                code += f'\tstind.ref\n'
            prev = ''

        elif tok == 'add_op' and val == '+':
            code += f'\tadd\n'
            # prev = ''

        elif tok == 'add_op' and val == '-':
            code += f'\tsub\n'
            # prev = ''

        elif tok == 'mult_op' and val == '*':
            code += f'\tmul\n'
            # prev = ''

        elif tok == 'mult_op' and val == '/':
            code += f'\tdiv\n'
            # prev = ''

        elif tok == 'pow_op' and val == '^':
            code += f'\tcall float64 [mscorlib]System.Math::Pow(float64, float64)\n'
            # code += f'\tcall float64 [mscorlib]System.Math::Pow(float64, float64)\n'
            prev = 'float'

        elif tok == 'unary_op' and val == '-':
            code += f'\tneg\n'

        elif tok == 'unary_op' and val == '+':
            pass

        elif tok == 'rel_op' and val == '==':
            code += f'\tceq\n'
            prev = 'boolean'

        elif tok == 'rel_op' and val == '!=':
            code += f'\tceq\n'
            code += f'\tldc.i4 0\n'
            code += f'\tceq\n'
            prev = 'boolean'

        elif tok == 'rel_op' and val == '>':
            code += f'\tcgt\n'  # \tbrfalse '
            prev = 'boolean'

        elif tok == 'rel_op' and val == '>=':
            code += f'\tclt\n'
            code += f'\tldc.i4 0\n'
            code += f'\tceq\n'
            prev = 'boolean'

        elif tok == 'rel_op' and val == '<':
            code += f'\tclt\n'  # \tbrfalse '
            prev = 'boolean'

        elif tok == 'rel_op' and val == '<=':
            code += f'\tcgt\n'
            code += f'\tldc.i4 0\n'
            code += f'\tceq\n'
            prev = 'boolean'

        elif tok == 'label':
            # if prev == 'boolean':
            #
            label_name = val
            # code += f'{label_name + ":"}\n'
            prev = 'label'
            continue

        elif tok == 'jf' and val == 'JF':
            if prev == 'label':
                code += f'\tbrfalse {label_name}\n'
            # code += f'{label_name}\n'
            label_name = ''

        elif tok == 'jump' and val == 'JMP':
            if prev == 'label':
                code += f'\tbr {label_name}\n'
            # code += f'\tbr {label_name}\n'
            label_name = ''

        elif tok == 'colon' and val == ':' and prev == 'label':
            code += f'{label_name + ":"}\n'
            label_name = ''
            prev = ''

        elif tok == 'out_op':
            if prev in ('int', 'float', 'intnum', 'floatnum'):
                var_named_const_type = prev + '32'
                code += f'\tcall void [mscorlib]System.Console::WriteLine({var_named_const_type})\n'
            elif prev in ('string', 'stringval'):
                code += f'\tcall void [mscorlib]System.Console::WriteLine(string)\n'
            elif prev in ('boolean', 'boolval'):
                code += '\tcall void [mscorlib]System.Console::WriteLine(bool)\n'
            prev = ''

        elif tok == 'in_op':
            code += f'\tcall string [mscorlib]System.Console::ReadLine()\n'
            code += f'\tstind.ref\n'
            # if prev in ('int', 'float', 'intnum', 'floatnum'):
            #     code += f'\tcall {prev}32 [mscorlib]System.{prev.capitalize() + "32" if prev not in ("boolean", "boolval") else "Boolean"}::Parse(string)\n'
            # if prev in ('float', 'floatnum'):
            #     code += f'\tstind.r4\n'
            # elif prev in ('string', 'stringval'):
            #     code += f'\tstind.ref\n'
            # elif prev in ('boolean', 'boolval'):
            #     code += f'\tstind.i4\n'
            # else:
            #     code += f'\tstind.i4\n'
            prev = ''
    code += '\nldstr ""'
    code += 'call void [mscorlib]System.Console::WriteLine(string)'

def save_CIL(file_name):
    fname = file_name + ".il"
    f = open(fname, 'w')
    header = """// Referenced Assemblies.
.assembly extern mscorlib
{
  .publickeytoken = (B7 7A 5C 56 19 34 E0 89 ) 
  .ver 4:0:0:0
}

// Our assembly.
.assembly """ + file_name + """
{
  .hash algorithm 0x00008004
  .ver 0:0:0:0
}

.module """ + file_name + """.exe

// Definition of Program class.
.class private auto ansi beforefieldinit Program
  extends [mscorlib]System.Object
{

    .method private hidebysig static void Main(string[] args) cil managed
    {
"""
    # f.write(header)

    #   cntVars = len(table_of_var)
    local_vars_named_consts = "\t.locals (\n"
    j = 0

    # only_one_table = True if not table_of_named_const else False
    for table in (table_of_var, table_of_named_const):
        comma = ","
        i = 0
        for x in table:
            try:
                _, type, _ = table[x]
            except ValueError:
                _, type = table[x]
            if type == 'int':
                type_il = 'int32'
            elif type == 'float':
                type_il = 'float32'
            elif type == 'string':
                type_il = type
            elif type == 'boolean':
                type_il = 'bool'

            if i == len(table) - 1 and table == table_of_named_const:  # or only_one_table:
                comma = "\n    )"
            local_vars_named_consts += "       [{0}]  {1} {2}".format(j, type_il, x) + comma + "\n"
            i = i + 1
            j = j + 1



    # print((x,a))
    entrypoint = """
    .entrypoint
    .maxstack  8\n"""
    #   code = ""
    #   # for instr in postfixCodeCLR:
    #   for instr in postfix_code:
    #     code += instr + "\n"

    #   # виведення значень змінних
    values_var_named_const = ""
    for table in (table_of_var, table_of_named_const):
        for x in table:
            values_var_named_const += "\t" + 'ldstr "' + x + ' = "\n'
            values_var_named_const += "\t" + "call void [mscorlib]System.Console::Write(string) \n"
            try:
                _, type, _ = table[x]
            except ValueError:
                _, type = table[x]
            if type == 'boolean':
                type = 'bool'
            elif type == 'string':
                pass
            else:
                type = type + '32'
            # ld_type = "ldstr  " if type == 'string' else "ldloc  "
            # values_var_named_const += "\t" + ld_type + x + "\n"
            values_var_named_const += "\t" + "ldloc  " + x + "\n"
            values_var_named_const += "\t" + "call void [mscorlib]System.Console::WriteLine(" + type + ") \n"
    # finishing_text = '\tldstr "Press any key to continue..."\n\tcall void [mscorlib]System.Console::WriteLine(string)\n'
    finishing_text = '\nldstr ""\ncall void [mscorlib]System.Console::WriteLine(string)'

    f.write(header + entrypoint + local_vars_named_consts + code + values_var_named_const + finishing_text + "\tret    \n}\n}")
    f.close()
    print(f"\nIL-код успішно збережено у файлі {fname}")


if f_success == (True, 'Executor'):
    try:
        convert_to_CIL()
        save_CIL(file_name)
    except SystemExit as error:
        print('\033[0m\033[1m\033[4mCIL-converter\033[0m: \033[91mАварійне завершення програми з кодом {0}\033[0m'.
              format(error))
        f_success = (False, 'Converter')
    else:
        print('\033[0m\033[1m\033[4mCIL-converter\033[0m: \033[92mКонвертація postfix в il завершено успішно\033[0m')
        f_success = (True, 'Converter')
