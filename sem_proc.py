def lex():
    global state, numLine, char, lexeme, numChar, FSuccess
    try:
        while numChar < lenCode:
            char = nextChar() # прочитати наступний символ
            classCh = classOfChar(char) # до якого класу належить
            state = nextState(state,classCh) # обчислити наступний стан
            if (is_final(state)): # якщо стан заключний
                processing() # виконати семантичнi процедури
            elif state == initState: # якщо стан НЕ закл., а стартовий, то
                lexeme='' # збиратимемо нову лексему
            else: # якщо стан НЕ закл. i не стартовий, то
                lexeme+=char # додати символ до лексеми
                print('Lexer: Лексичний аналiз завершено успiшно')
    except SystemExit as e:
        FSuccess = (False,'Lexer') # Встановити ознаку неуспiшностi
        # Повiдомити про неуспiх
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


def processing():
    global state,lexeme,char,numLine,numChar, tableOfSymb
    if state==14: 
        numLine+=1
        state=initState
    if state in (2,6,9): 
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
        state = initState
    if state in (12,14):
        lexeme+=char
        token=getToken(state,lexeme)
        print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine,lexeme,token))
        tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,'')
        lexeme=''
        state=initState
    if state in Ferror: #(101,102): # ERROR
        fail()

