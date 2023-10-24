def class_of_char(char):
    if char is '.':
        result = "dot"
    elif char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
        result = "Letter"
    elif char in "0123456789":
        result = "Digit"
    elif char in " \t":
        result = "ws"
    elif char is "\n":
        result = "cr"
    elif char in "+-*/^(){}<>=\"":
        result = char
    else:
        result = "Символ не належить алфавіту"
    return result


stf = {(0, 'Letter'): 1, (1, 'Letter'): 1, (1, 'Digit'): 1, (1, 'other'): 2,
       (0, 'Digit'): 3, (3, 'Digit'): 3, (3, 'other'): 4, (3, 'dot'): 5, (5, 'Digit'): 6, (5, 'other'): 103, (6, 'Digit'): 6, (6, 'other'): 7, (6, '+'): 8, (8, 'Digit'): 8, (8, 'dot'): 9, (8, 'i'): 11, (9, 'Digit'): 10, (9, 'other'): 103, (10, 'Digit'): 10, (10, 'i'): 11,
       (0, ': '): 12, (12, '='): 13, (12, 'other'): 102,
       (0, 'other'): 101,
       (0, 'cr'): 14,
       (0, '='): 15, (15, '='): 16,
       (0, '<'): 17, (0, '>'): 17,
       (0, '\"'): 18, (18, 'other'): 18, (18, '\"'): 19,
       (0, '{'): 20, (0, '}'): 20, (0, '^'): 20, (0, '/'): 20, (0, '*'): 20, (0, '-'): 20, (0, '+'): 20, (0, '('): 20, (0, ')'): 20
       }
init_state = 0
F = {2, 4, 7, 11, 13, 14, 16, 17, 19, 20, 101, 102, 103}
F_star = {2, 4, 7, 11}
F_error = {101, 102, 103}


token_table = {'true': 'keyword', 'false': 'keyword', 'const': 'keyword', 'var': 'keyword', 'func': 'keyword',
               'return': 'keyword', 'if': 'keyword', 'else': 'keyword', 'for': 'keyword', 'range': 'keyword',
               'break': 'keyword', 'import': 'keyword', 'package': 'keyword',
               ':=': 'assign_op', '.': 'punc', ',': 'punc', ':': 'punc',
               ' ': 'ws', '\t': 'ws', '\n': 'cr', '\r': 'cr', '\n\r': 'cr', '\r\n': 'cr',
               '-': 'add_op', '+': 'add_op', '*': 'mult_op', '/': 'mult_op', '^': 'pow_op',
               '(': 'brack_op', ')': 'brack_op', '{': 'brack_op', '}': 'brack_op'
               }
token_state_table = {2: 'ident', 4: 'int', 7: 'float', 11: 'complex', 19: 'string', 16: 'rel_op', 17: 'rel_op'}


# table_of_symb = { 'n_rec': (num_line, lexeme, token, idx_id_const) }


def lex():
    global state, numLine, char, lexeme, numChar, FSuccess
    try:
        while numChar < lenCode:
            char = nextChar() # прочитати наступний символ
            classCh = class_of_char(char) # до якого класу належить
            state = nextState(state,classCh) # обчислити наступний стан
            if (state in F): # якщо стан заключний
                processing() # виконати семантичнi процедури
            elif state == init_state: # якщо стан НЕ закл., а стартовий, то
                lexeme='' # збиратимемо нову лексему
            else: # якщо стан НЕ закл. i не стартовий, то
                lexeme+=char # додати символ до лексеми
                print('Lexer: Лексичний аналiз завершено успiшно')
    except SystemExit as e:
        FSuccess = (False,'Lexer')
        print('Lexer: Аварiйне завершення програми з кодом {0}'.format(e))


def nextChar():
    global numChar
    numChar+=1
    return sourceCode[numChar]


def putCharBack(numChar):
    return numChar - 1


def nextState(state,classCh):
    try:
        return stf[(state,classCh)]
    except KeyError:
        return stf[(state,'other')]

# не впевнена чи добре в іфах є кінцеві стани
def processing():
    global state,lexeme,char,numLine,numChar, tableOfSymb
    if state==14: 
        numLine+=1
        state=init_state
    if state==2: 
        token=getToken(state,lexeme)
        if token != 'keyword': 
            index=indexIdConst(state,lexeme)
            print('{0:<3d} {1:<10s} {2:<10s} {3:<2d} '.format(numLine,\
            lexeme,token,index))
            tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,index)
        else: # якщо keyword
            print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine,lexeme,token))
            tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,'')
            lexeme=''
            numChar=putCharBack(numChar) # зiрочка
            state = init_state
    if state in (4, 7, 11, 13, 16, 17, 19, 20):
        lexeme+=char
        token=getToken(state,lexeme)
        print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine,lexeme,token))
        tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,'')
        lexeme=''
        state=init_state
    if state in F_error: #(101, 102, 103): # ERROR
        fail()

