# Tovid language lexer and syntaxer

token_table = {'true': 'keyword', 'false': 'keyword', 'const': 'keyword', 'var': 'keyword', 'func': 'keyword',
               'return': 'keyword', 'if': 'keyword', 'else': 'keyword', 'for': 'keyword', 'range': 'keyword',
               'break': 'keyword', 'import': 'keyword', 'package': 'keyword', 'nil': 'keyword', 'iota': 'keyword',
               'int': 'keyword', 'float': 'keyword', 'complex': 'keyword', 'string': 'keyword', 'boolean': 'keyword',
               'print': 'keyword', 'scanf': 'keyword', ':=': 'assign_op',
               '.': 'punc', ',': 'punc', ':': 'punc', ';': 'punc',
               ' ': 'ws', '\t': 'ws', '\n': 'cr', '\r': 'cr', '\n\r': 'cr', '\r\n': 'cr',
               '*': 'mult_op', '/': 'mult_op', '^': 'pow_op',
               '==': 'rel_op', '>': 'rel_op', '>=': 'rel_op', '<': 'rel_op', '<=': 'rel_op', '!=': 'rel_op',
               '> ': 'rel_op', '>= ': 'rel_op', '< ': 'rel_op', '<= ': 'rel_op', '!= ': 'rel_op',
               '(': 'brack_op', ')': 'brack_op', '{': 'brack_op', '}': 'brack_op',
               '//': 'comment', '/*': 'comment', '*/': 'comment'
               }
token_state_table = {2: 'ident', 4: 'int', 7: 'float', 11: 'complex', 19: 'string', 16: 'rel_op', 17: 'rel_op',
                     28: 'add_op'}


stf = {(0, 'Letter'): 1, (1, 'Letter'): 1, (1, 'Digit'): 1, (1, 'other'): 2,
       (0, 'Digit'): 3, (3, 'Digit'): 3, (3, 'other'): 4, (3, 'dot'): 5, (3, '+'): 8, (3, 'i'): 21, (5, 'Digit'): 6,
       (5, 'other'): 103, (6, 'Digit'): 6, (6, 'other'): 7, (6, '+'): 8, (6, 'i'): 21, (8, 'Digit'): 8, (8, 'dot'): 9,
       (8, 'i'): 21, (8, 'other'): 101, (9, 'Digit'): 10, (9, 'other'): 103, (10, 'Digit'): 10, (10, 'i'): 21,
       (10, 'other'): 101, (21, 'other'): 11,
       (0, ':'): 12, (12, '='): 13, (12, 'other'): 102,
       (0, 'other'): 101,
       (0, 'cr'): 14,
       (0, 'ws'): 0,
       (0, '-'): 27, (0, '+'): 27, (27, 'Digit'): 3, (27, 'other'): 28,
       (0, '='): 15, (0, '!'): 15, (15, '='): 16, (15, 'other'): 101,
       (0, '<'): 22, (0, '>'): 22, (22, '='): 16, (22, 'other'): 17,
       (0, '"'): 18, (18, 'other'): 18, (18, '"'): 19,
       (0, '{'): 20, (0, '}'): 20, (0, '^'): 20,
       (0, '('): 20, (0, ')'): 20, (0, ','): 20, (0, ';'): 20,
       (0, '/'): 26, (0, '*'): 23, (26, 'other'): 25, (23, 'other'): 25,
       (26, '/'): 24, (26, '*'): 24, (23, '/'): 24,
       }
init_state = 0
F = {2, 4, 7, 11, 13, 14, 16, 17, 19, 20, 24, 25, 28, 101, 102, 103}
F_star = {2, 4, 7, 11, 17, 25, 28}
F_error = {101, 102, 103}

table_of_symb = {}
table_of_id = {}
table_of_const = {}
table_of_var = {}
current_func_params = []
func_names = []

state = init_state

f = open('a.tovid', 'r')
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
    if state in F:
        if state == 14:
            num_line += 1
            state = init_state
        elif state == init_state:
            ...
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
            print('{0:<3d} {1:<10s} {2:<10s} '.format(num_line, lexeme, token))
            table_of_symb[len(table_of_symb) + 1] = (num_line, lexeme, token, '')
            lexeme = ''
            state = init_state


def fail():
    global state, num_line, char
    # print(num_line)
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


print('-' * 30)
print('table_of_symb:{0}'.format(table_of_symb))
print('-' * 30)
print('table_of_id:{0}'.format(table_of_id))
print('-' * 30)
print('table_of_const:{0}'.format(table_of_const))
print('-' * 30)


# -------------------------------------------------------
num_row_s = 1
num_line_s = 1
len_table_of_symb = len(table_of_symb)

params_types = {'nil': 'keyword', 'iota': 'keyword', 'int': 'keyword', 'float': 'keyword', 'complex': 'keyword',
                'string': 'keyword', 'boolean': 'keyword', 'true': 'keyword', 'false': 'keyword'}

allowed_data_types = ['int', 'float', 'complex', 'string', 'boolean']

# доповнювати
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
                fail_parse("змінна без const/var", (num_line_s, lex, tok))
            else:
                parse_statementlist()
        print("Parser: Синтаксичний і семантичний аналiз завершився успiшно")
        return True
    except SystemExit as e:
        print("Parser: Аварiйне завершення програми з кодом {0}".format(e))


# done
def parse_func():
    global num_row_s, num_line_s, table_of_var, func_names
    num_row_s += 1
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    # не потрібно змінити порядок двох наступних рідків?
    func_names.append(lex)
    parse_identlist(lex)
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    parse_token('(', tok, num_row_s)
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    parse_params(lex, tok)
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    parse_token(')', tok, num_row_s)
    parse_token('{', tok, num_row_s)
    parse_statementlist()
    parse_token('}', tok, num_row_s)

    # скоуп закінчився. Очищаємо змінні та параметри функції
    table_of_var.clear()
    current_func_params.clear()


# done
def parse_params(lexeme, token):
    global num_row_s, num_line_s, current_func_params
    if lexeme != ')':
        num_line_s, lex, tok = get_current_lexeme(num_row_s)
        num_line_s1, lex1, tok1 = get_current_lexeme(num_row_s + 1)
        while lex != ')':
            if lex in table_of_id.keys() or tok in params_types.keys():
                current_func_params.append(lex)
                num_row_s += 1
                num_line_s, lex, tok = get_current_lexeme(num_row_s)
            else:
                fail_parse('очікувався параметр', (num_line_s, lex, tok))
            if lex == ',':
                num_line_s1, lex1, tok1 = get_current_lexeme(num_row_s + 1)
                if lex1 in table_of_id.keys() or tok1 in params_types.keys():
                    current_func_params.append(lex)
                    num_row_s += 1
                    num_line_s, lex, tok = get_current_lexeme(num_row_s)
                else:
                    fail_parse('очікувався параметр', (num_line_s, lex1, tok1))
    num_line_s += 1


# done
def parse_token(lexeme, token, id) :
    global num_row_s, num_line_s
    if num_row_s <= len_table_of_symb:
        num_line_s, lex, tok = get_current_lexeme(num_row_s)
        num_row_s += 1
        if (lex, tok) == (lexeme, token):
            print('parseToken: В рядку {0} токен {1}'.format(num_line_s, (lexeme, token)))
            return True
        else:
            fail_parse('невiдповiднiсть токенiв', (num_line_s, lex, tok, lexeme, token))
            return False
    else:
        fail_parse("неочiкуваний кiнець програми", (lexeme, token, num_row_s))


# done
def parse_identlist(lexeme):
    global num_row_s
    if lexeme in table_of_id.keys():
        num_row_s += 1
    else:
        num_line_s, lex, tok = get_current_lexeme(num_row_s)
        fail_parse('очікувався ідентифікатор', (num_line_s, lex, tok))


# done?
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
# fix
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
        elif tok == 'ident':
            parse_declared_ident(lex, tok)
        else:
            # print('тутки з лексемою ', lex, ' та токеном ', tok)
            print("непередбачена логіка у функції parse_statementlist")
            fail_parse('return', (num_line_s, lex, tok))
        num_line_s, lex, tok = get_current_lexeme(num_row_s)


# done
def parse_declared_ident(lexeme, token):
    global num_row_s, num_line_s
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    if lexeme in table_of_var.keys():
        num_row_s += 1
        parse_token(':=', 'assign_op', num_row_s)
        parse_declarpart()
    else:
        fail_parse("не оголошена змінна", (num_line_s, lex, tok, ))


# done
def parse_scanf_print(lexeme, token):
    global num_line_s, num_row_s
    num_row_s += 1
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    parse_token('(', tok, num_row_s)
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    if lex != ')':
        num_line_s, lex, tok = get_current_lexeme(num_row_s)
        _, lex1, tok1 = get_current_lexeme(num_row_s + 1)
        while lex != ')':
            if lexeme == 'scanf':
                # print(lex, num_line_s)
                if lex in table_of_id.keys():
                    num_row_s += 1
                    num_line_s, lex, tok = get_current_lexeme(num_row_s)
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
                if lex in table_of_id.keys() or tok in params_types.keys() :
                    num_row_s += 1
                    num_line_s, lex, tok = get_current_lexeme(num_row_s)
                else:
                    fail_parse('очікувався параметр', (num_line_s, lex, tok))
                if lex == ',' or lex == '+':
                    _, lex1, tok1 = get_current_lexeme(num_row_s + 1)
                    if lex1 in table_of_id.keys() or tok1 in params_types.keys():
                        num_row_s += 1
                        num_line_s, lex, tok = get_current_lexeme(num_row_s)
                    else:
                        fail_parse('очікувався параметр', (num_line_s, lex1, tok1))
    parse_token(')', tok, num_row_s)


# done
def parse_declarlist():
    global num_row_s
    declared_datatype = False
    # datatype = ''
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    keyword = lex
    num_row_s += 1
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    if lex in allowed_data_types:
        datatype = lex
        num_row_s += 1
        num_line_s, lex, tok = get_current_lexeme(num_row_s)
        declared_datatype = True
    elif lex in table_of_id.keys():
        declared_datatype = False
    else:
        fail_parse("не дозволений тип даних", (num_line_s, lex, tok))
    if lex in table_of_id.keys():
        if lex in table_of_var.keys():
            fail_parse('повторне оголошення змінної',(num_line_s, lex, tok))
        current_id = lex
        num_row_s += 1
        num_line_s, lex, tok = get_current_lexeme(num_row_s)
        index = len(table_of_var) + 1 if keyword == 'var' else len(table_of_const) + 1
        if tok == 'assign_op':
            num_row_s += 1
            value_datatype = parse_declarpart()
            if declared_datatype:
                if datatype == value_datatype or value_datatype == 'from_function' or value_datatype == 'from_params':
                    if keyword == 'var':
                        table_of_var[current_id] = (index, datatype, 'assigned')
                    else:
                        table_of_const[current_id] = (datatype, index)
                else:
                    fail_parse('значення змінної не відповідає оголошеному типу', (num_line_s, current_id, 'ident'))
            else:
                if value_datatype == 'from_function' or value_datatype == 'from_params':
                    fail_parse("неможливо визначити тип", (num_line_s, lex, tok))
                else:
                    if keyword == 'var':
                        table_of_var[current_id] = (index, value_datatype, 'assigned')
                    else:
                        table_of_const[current_id] = (value_datatype, index)
        else:
            if not declared_datatype:
                num_row_s -= 1
                num_line_s, lex, tok = get_current_lexeme(num_row_s)
                fail_parse("неможливо визначити тип", (num_line_s, lex, tok))
            else:
                if keyword == 'var':
                    table_of_var[current_id] = (index, datatype, 'assigned')
                else:
                    table_of_const[current_id] = (datatype, index)


    else:
        fail_parse("очікувався ідентифікатор", (num_line_s, lex, tok))


# тут якось потрібно слідкувати щоб була послідовність між змінними і знаками (а + м) * 12 > 3
# fix
def parse_declarpart():
    global num_row_s, num_line_s
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    declarpart_line = num_line_s
    boolean_expr = False
    arithm_operators_used = False
    while num_line_s == declarpart_line and tok != 'punc':
        # print('ІТЕРАЦІЯ')
        num_line_s, lex, tok = get_current_lexeme(num_row_s)
        # print(num_line_s, lex, tok, num_row_s)
        if tok == 'add_op':
            # print(num_line_s, lex, tok, num_row_s)
            arithm_operators_used = True
            num_row_s += 1
            num_line_s, lex, tok = get_current_lexeme(num_row_s)

        elif tok in params_types.keys():
            value_datatype = tok
            num_row_s += 1
            num_line_s, lex, tok = get_current_lexeme(num_row_s)
        # в цьому іфі повинні парситися виклики функцій sum(c1, c2) або присвоєння змінної
        elif lex in table_of_id:
            # all_var_const_funcnames = []
            # all_var_const_funcnames.extend(table_of_var.keys())
            # all_var_const_funcnames.extend(table_of_const.keys())
            # all_var_const_funcnames.extend(func_names)
            # print('*' * 30)
            # print(all_var_const_funcnames)
            # print('*' * 30)
            try:
                if lex in table_of_var.keys():
                    value_datatype = table_of_var.get(lex)[1]
                elif lex in table_of_const.keys():
                    value_datatype = table_of_const.get(lex)[0]
                elif lex in func_names:
                    value_datatype = 'from_function'
            except TypeError:
                if lex in current_func_params:
                    value_datatype = 'from_params'
                else:
                    fail_parse('не оголошена змінна', (num_line_s, lex, tok))
            except KeyError:
                if lex in current_func_params:
                    value_datatype = 'from_params'
                else:
                    fail_parse('не оголошена змінна', (num_line_s, lex, tok))
            if lex in func_names:
                value_datatype = 'from_function'
                num_row_s += 1
                num_line_s, lex, tok = get_current_lexeme(num_row_s)
                parse_token('(', 'brack_op', '')
                parse_params(lex, tok)
                num_line_s, lex, tok = get_current_lexeme(num_row_s)
                # num_row_s += 1
                # num_line_s, lex, tok = get_current_lexeme(num_row_s)
            num_row_s += 1
            num_line_s, lex, tok = get_current_lexeme(num_row_s)
        elif lex == '^':
            arithm_operators_used = True
            num_row_s += 1
            num_line_s, lex, tok = get_current_lexeme(num_row_s)
            # print(lex)
            if lex == '(':
                parse_declarpart_parentheses()
            elif lex in table_of_var.keys() or tok == "int" or tok == "float":
                num_row_s += 1
                num_line_s, lex, tok = get_current_lexeme(num_row_s)
                # ХЗ ЩО ТУТ РОБИТИ
                # Діма: та нічого не треба робити, якщо айді або число,
                #       то значить все коректно, ми ж лише синтаксис перевіряємо
        elif tok == 'mult_op':
            arithm_operators_used = True
            zero_devision_check = True if lex == '/' else False
            num_row_s += 1
            num_line_s, lex, tok = get_current_lexeme(num_row_s)
            if tok == 'int':
                if not int(lex):
                    fail_parse('ділення на нуль', (num_line_s, lex, tok))
            elif tok == 'float':
                if not float(lex):
                    fail_parse('ділення на нуль', (num_line_s, lex, tok))
        elif tok == 'rel_op':
            boolean_expr = True
            num_row_s += 1
            num_line_s, lex, tok = get_current_lexeme(num_row_s)
        elif lex == 'true' or lex == 'false':
            boolean_expr = True
            num_row_s += 1
            num_line_s, lex, tok = get_current_lexeme(num_row_s)
        elif lex == '(':
            parse_declarpart_parentheses()
        else:
            fail_parse('неправильна задекларована змінна', (num_line_s, lex, tok))
    if boolean_expr:
        value_datatype = 'boolean'
    elif arithm_operators_used:
        value_datatype = 'float'
    return value_datatype


def parse_declarpart_parentheses():
    global num_row_s, num_line_s
    num_row_s += 1

    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    declarpart_line = num_line_s
    while lex != ')':
        if declarpart_line != num_line_s:
            fail_parse('не закрита кругла дужка', (declarpart_line, lex, tok))
        # print(num_line_s, lex, tok, num_row_s)
        # if tok == 'add_op':
        #     num_row_s += 1
        #     num_line_s, lex, tok = get_current_lexeme(num_row_s)
        # if tok in params_types.keys():
        #     num_row_s += 1
        #     num_line_s, lex, tok = get_current_lexeme(num_row_s)
        # # if tok == 'string':
        # #     num_row_s += 1
        # #     num_line_s, lex, tok = get_current_lexeme(num_row_s)
        # if lex in table_of_id:
        #     num_row_s += 1
        #     num_line_s, lex, tok = get_current_lexeme(num_row_s)
        # elif lex == '(':
        #     parse_declarpart_parentheses()
        # else:
        #     fail_parse('неправильна задекларована змінна', (num_line_s, lex, tok))
        if tok == 'add_op':
            num_row_s += 1
            num_line_s, lex, tok = get_current_lexeme(num_row_s)
        elif tok in params_types.keys():
            num_row_s += 1
            num_line_s, lex, tok = get_current_lexeme(num_row_s)
        # в цьому іфі повинні парситися виклики функцій sum(c1, c2) або присвоєння змінної
        elif lex in table_of_id:
            num_row_s += 1
            num_line_s, lex, tok = get_current_lexeme(num_row_s)
            if lex == '(':
                num_row_s += 1
                num_line_s, lex, tok = get_current_lexeme(num_row_s)
                parse_params(lex, tok)
                num_line_s, lex, tok = get_current_lexeme(num_row_s)
                num_row_s += 1
                num_line_s, lex, tok = get_current_lexeme(num_row_s)
        elif lex == '^':
            num_row_s += 1
            num_line_s, lex, tok = get_current_lexeme(num_row_s)
            # print(lex)
            if lex == '(':
                parse_declarpart_parentheses()
            elif lex in table_of_var.keys() or tok == "int" or tok == "float":
                num_row_s += 1
                num_line_s, lex, tok = get_current_lexeme(num_row_s)
                # тут натикаємось на закриту дужку
        elif tok == 'mult_op':
            # print('ми тут')
            num_row_s += 1
            num_line_s, lex, tok = get_current_lexeme(num_row_s)
        elif tok == 'rel_op':
            num_row_s += 1
            num_line_s, lex, tok = get_current_lexeme(num_row_s)
        elif lex == '(':
            parse_declarpart_parentheses()
        else:
            fail_parse('неправильна задекларована змінна', (num_line_s, lex, tok))
    num_row_s += 1
    num_line_s, lex, tok = get_current_lexeme(num_row_s)


# done
def parse_return():
    global num_row_s, num_line_s
    num_row_s += 1
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    if lex in table_of_id.keys() or tok in allowed_data_types or lex == 'iota' or lex == 'nil' or lex == 'true' or lex == 'false':
        num_row_s += 1
        num_line_s, lex, tok = get_current_lexeme(num_row_s)
    else:
        fail_parse("return", (num_line_s, tok, lex))


# done
def parse_package():
    global num_row_s, num_line_s
    num_row_s += 1
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    parse_identlist(lex)


# done
def parse_import():
    global num_row_s, num_line_s
    num_row_s += 1
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    if tok == 'string':
        parse_token(lex, tok, num_line_s)
    else:
        fail_parse('очікувався рядок', (num_line_s, lex, tok))


# fix
def parse_bool_expr():
    global num_row_s, num_line_s
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    while(tok != 'rel_op'):
        # print(lex, tok, 'line 350')
        num_row_s += 1
        num_line_s, lex, tok = get_current_lexeme(num_row_s)
    if tok in 'rel_op':
        # print(lex, tok, 'line 400')
        num_row_s += 1
    else:
        fail_parse('невiдповiднiсть токенiв', (num_line_s, lex, tok))
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    while(tok != 'brack_op' and tok != 'punc'):
        # print(lex, tok, 'line 350')
        num_row_s += 1
        num_line_s, lex, tok = get_current_lexeme(num_row_s)
    num_line_s, lex, tok = get_current_lexeme(num_row_s)


# fix
def parse_if():
    global num_row_s, num_line_s
    num_line_s, lex, tok = get_current_lexeme(num_row_s)
    if lex == 'if' and tok == 'keyword':
        num_row_s += 1
        parse_bool_expr()
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


# fix
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
        parse_bool_expr()
        parse_token(';', 'punc', '')
        num_line_s, lex, tok = get_current_lexeme(num_row_s)
        while (lex != '{'):
            num_row_s += 1
            num_line_s, lex, tok = get_current_lexeme(num_row_s)
        #parse_statementlist()
    else:
        parse_bool_expr()
    parse_token('{', 'brack_op', '')
    parse_statementlist()
    parse_token('}', 'brack_op', '')


# done
def get_current_lexeme (num_row) :
    num_line, lexeme, token, _ = table_of_symb[num_row]
    return num_line, lexeme, token


# можна доповнювати
def fail_parse(str, tuple):
    if str == 'неочiкуваний кiнець програми':
        (lexeme, token, num_row) = tuple
        print('Parser ERROR: \n\t Неочiкуваний кiнець програми - в таблицi символiв (розбору) немає запису з номером {1}.\n\t Очiкувалось - {0}'.format((lexeme, token), num_row))
        exit(1001)
    elif str == 'невiдповiднiсть токенiв':
        (num_line, lexeme, token, lex, tok) = tuple
        print('Parser ERROR: \n\t В рядку {0} неочiкуваний елемент ({1}, {2}). \n\t Очiкувався - ({3},{4})'.format(num_line, lexeme, token, lex, tok))
        exit(1)
    elif str == 'очікувався ідентифікатор':
        (num_line, lexeme, token) = tuple
        print('Parser ERROR: \n\t В рядку {0} неочiкуваний елемент ({1}, {2}). \n\t Очікувався ідентифікатор'.format(
            num_line, lexeme, token))
        exit(2)
    elif str == 'очікувався рядок':
        (num_line, lexeme, token) = tuple
        print('Parser ERROR: \n\t В рядку {0} неочiкуваний елемент ({1}, {2}). \n\t Очікувався рядок'.format(
            num_line, lexeme, token))
        exit(3)
    elif str == 'очікувався параметр':
        (num_line, lexeme, token) = tuple
        print('Parser ERROR: \n\t В рядку {0} неочiкуваний елемент ({1}, {2}). \n\t Очікувався ідентифікатор як параметр функції'.format(
            num_line, lexeme, token))
        exit(4)
    elif str == 'змінна без const/var':
        (num_line) = tuple
        print('Parser ERROR: \n\t В рядку {0} очікується var/const'.format(num_line))
        exit(5)
    elif str == 'return':
        (num_line, lexeme, token) = tuple
        print('Parser ERROR: \n\t В рядку {0} очікується нормальне повернення return'.format(num_line))
        exit(6)
    elif str == 'не дозволений тип даних':
        (num_line, lexeme, token) = tuple
        print('Parser ERROR: \n\t В рядку {0} неочiкуваний елемент ({1}, {2})'.format(num_line, lexeme, token))
        exit(7)
    elif str == 'присвоювання':
        (num_line, lexeme, token) = tuple
        print('Parser ERROR: \n\t В рядку {0} неочiкуваний елемент ({1}, {2}). Очікується присвоювання (:=)'.format(num_line, lexeme, token))
        exit(8)
    elif str == 'не оголошена змінна':
        (num_line, lexeme, token) = tuple
        print('Parser ERROR: \n\t В рядку {0} не оголошена змінна ({1}, {2})'.format(num_line, lexeme, token))
        exit(9)
    elif str == 'не закрита кругла дужка':
        (num_line, lexeme, token) = tuple
        print('Parser ERROR: \n\t В рядку {0} не закрита кругла дужка'.format(num_line))
        exit(10)
    elif str == 'неможливо визначити тип':
        (num_line, lexeme, token) = tuple
        print('Parser ERROR: \n\t В рядку {0} неможливо визначити тип змінної ({1}, {2}) '
              'без присвоєння значення'.format(num_line, lexeme, token))
        exit(11)
    elif str == 'значення змінної не відповідає оголошеному типу':
        (num_line, lexeme, token) = tuple
        print('Parser ERROR: \n\t В рядку {0} значення змінної ({1}, {2}) '
              'не відповідає оголошеному типу '.format(num_line, lexeme, token))
        exit(12)
    elif str == 'ділення на нуль':
        (num_line, lexeme, token) = tuple
        print('Parser ERROR: \n\t В рядку {0} відбувається ділення на нуль ({1}, {2})'
              .format(num_line, lexeme, token))
        exit(13)
    elif str == 'повторне оголошення змінної':
        (num_line, lexeme, token) = tuple
        print('Parser ERROR: \n\t В рядку {0} повторне оголошення змінної ({1}, {2})'
              .format(num_line, lexeme, token))
        exit(13)
    elif str == '':
        (num_line, lexeme, token) = tuple
        print('Parser ERROR: \n\t В рядку {0} неочiкуваний елемент ({1}, {2})'.format(num_line, lexeme, token))
        exit(15)


parse_program()