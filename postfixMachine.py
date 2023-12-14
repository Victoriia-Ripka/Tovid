# -------------------------------------------------------
# code generation
# -------------------------------------------------------

import re
from stack import Stack


class PSM:             # Postfix Stack Machine
    def __init__(self, file_name):
      self.tableOfVar = {}
      self.tableOfLabel = {}
      self.tableOfConst = {}
      self.tableOfNamedConst = {}
      self.postfixCode = []
      self.mapDebug = {}
      self.numLine = 0
      self.file_name = file_name
      self.file = ""
      self.slt = ""
      self.headSection = {"VarDecl": ".vars(", "LblDecl": ".labels(",
                          "ConstDecl": ".constants(", "NamedConstDecl": ".named_constants(", "Code": ".code("}
      self.errMsg = {1: "неочікуваний заголовок",
                     2: "тут очікувався хоч один порожній рядок",
                     3: "тут очікувався заголовок секції",
                     4: "очікувалось два елемента в рядку",
                     8: "неініційована змінна",
                     9: "типи операндів не прийнятні для виконуваної операції",
                     10: "невідомий унарний оператор"
                     }
      self.stack = Stack()
      self.numInstr = 0
      self.maxNumbInstr = 0

    def load_postfix_file(self, file_name):
      try:
        self.file_name = file_name + ".postfix"
        self.file = open(self.file_name, 'r')
        self.parse_postfix_program()
        self.file.close()
      except PSMExcept as e:
        print(f"PSM.loadPostfixFile ERROR: у рядку {self.numLine}, код винятку - {e.msg}, msg = {self.errMsg[e.msg]}")

    def parse_postfix_program(self):
        # print("--------- header ")
        self.parse_header(".target: Postfix Machine")
        # print(f"have header1 {self.numLine}")
        self.parse_header(".version: 0.0.1")
        # print(f"have header2 {self.numLine}")

        self.parse_section("VarDecl")
        # print(f"have var {self.numLine}")

        self.parse_section("ConstDecl")
        # print("have const ")

        self.parse_section("NamedConstDecl")
        # print("have named const ")

        self.parse_section("LblDecl")
        # print("have lbl ")

        self.parse_section("Code")  # mapDebug:: numInstr -> numLine
        # print("have code ")

    def parse_header(self, header):
        if self.file.readline().rstrip() != header:
            raise PSMExcept(1)
        self.numLine += 1

    def parse_section(self, section):
        # print("============Section: "+section)
        headerSect = self.headSection[section]
        s = self.file.readline().partition("#")[0].strip()
        self.numLine += 1
        # один порожній рядок обов'язковий
        if s != "":
            raise PSMExcept(2)
        # інші (можливі) порожні рядки та заголовок секції
        F = True
        while F:
            s = self.file.readline().partition("#")[0].strip()
            # print("s=",s)
            self.numLine += 1
            if s == "":
                pass  # self.numLine += 1
            elif s == headerSect:
                # self.numLine += 1
                F = False
            else:
                raise PSMExcept(3)
        # формування відповідної таблиці (можливі і порожні рядки)
        F = True
        while F:
            s = self.file.readline().partition("#")[0].strip()
            self.numLine += 1
            if s == "":
                pass
            elif s == ")":  # кінець секції
                F = False
            else:
                self.slt = s
                self.proc_section(section)

    def proc_section(self, section):
        list = self.slt.split()
        if len(list) != 2:
            raise PSMExcept(4)
        else:
            item1 = list[0]
            item2 = list[1]
            if section == "VarDecl":
                table = self.tableOfVar
                indx = len(table) + 1
                table[item1] = (indx, item2, 'val_undef')

            if section == "ConstDecl":
                table = self.tableOfConst
                indx = len(table) + 1
                if item2 == "int":
                    val = int(item1)
                elif item2 == "float":
                    val = float(item1)
                elif item2 == "complex":
                    try:
                        val = complex(item1.replace('i', 'j'))
                    except ValueError:
                        val = complex('0+'+item1.replace('i', 'j'))
                # elif item2 == "boolean":
                #     val = item1
                # elif item2 == 'string':
                #     val = str(item1)
                table[item1] = (indx, item2, val)  # temporarily

            if section == "NamedConstDecl":
                table = self.tableOfNamedConst
                indx = len(table) + 1
                table[item1] = (indx, item2, 'to_be_clarified')

            if section == "LblDecl":
                table = self.tableOfLabel
                indx = len(table) + 1
                table[item1] = item2

            if section == "Code":
                indx = len(self.postfixCode)
                self.postfixCode.append((item1, item2))
                instrNum = len(self.postfixCode) - 1
                self.mapDebug[instrNum] = self.numLine

    def postfix_exec(self):
        """Виконує postfixCode"""
        print('\npostfixExec:')
        self.maxNumbInstr = len(self.postfixCode)
        try:
            while self.numInstr < self.maxNumbInstr:
                self.stack.print()
                lex, tok = self.postfixCode[self.numInstr]
                if tok in ('int', 'float', 'complex', 'string', 'l-val', 'r-val', 'label', 'boolean'):
                    self.stack.push((lex, tok))
                    self.numInstr += 1
                elif tok in ('jump', 'jf', 'colon'):
                    self.do_jumps(lex, tok)
                elif tok == 'out_op':
                        id, _ = self.stack.pop()
                        # print('завдання: вивести ', id)
                        self.numInstr += 1
                        if id in self.tableOfVar.keys():
                            print(f'-------------- OUT: {id}={self.tableOfVar[id][2]}')
                        elif id in self.tableOfNamedConst.keys():
                            print(f'-------------- OUT: {id}={self.tableOfNamedConst[id][2]}')
                        else:
                            print(f'-------------- OUT: {id}')
                elif tok == 'in_op':
                        id, _ = self.stack.get_top_element()
                        user_input = '"' + input() + '"'
                        print(f'-------------- IN: {id}={self.tableOfVar[id][2]} -> {id}={user_input}')  # {id}={self.tableOfVar[id][2]} -> {id}={user_input}')
                        self.stack.push((user_input, 'string'))
                        self.do_it(':=', 'assign_op')
                        self.numInstr += 1
                        # if id in self.tableOfVar.keys():
                        #     self.tableOfVar[lexL] = (self.tableOfVar[lexL][0], tokR, get_value(lexR, tokR))
                        # else:
                        #     self.tableOfNamedConst[lexL][0], tokR, get_value(lexR, tokR)
                else:
                    print(f'-=-=-=========({lex},{tok})  numInstr={self.numInstr}')
                    self.do_it(lex, tok)
                    self.numInstr += 1
            self.stack.print()
        except PSMExcept as e:
            # Повідомити про факт виявлення помилки
            print('RunTime: Аварійне завершення програми з кодом {0}'.format(e))

    def do_jumps(self, lex, tok):
        ni = self.numInstr
        if tok == 'jump':
            lexLbl, _ = self.stack.pop()  # зняти з вершини стека мітку
            self.numInstr = int(self.tableOfLabel[lexLbl])  # номер наступної інструкції = значення мітки
        elif tok == 'colon':
            _, _ = self.stack.pop()  # зняти з вершини стека
            self.numInstr = self.numInstr + 1  # непотрібну нам мітку
        elif tok == 'jf':
            lexLbl, _ = self.stack.pop()  # зняти з вершини стека мітку
            valBoolExpr, _ = self.stack.pop()  # зняти з вершини стека значення BoolExpr
            if valBoolExpr == 'false':
                self.numInstr = int(self.tableOfLabel[lexLbl])
            else:
                self.numInstr = self.numInstr + 1
        print(f'+=+=+=========({lex},{tok})  numInstr={ni} nextNumInstr={self.numInstr}')

    def do_it(self, lex, tok):
        # зняти з вершини стека запис (правий операнд)
        # self.stack.print()
        (lexR, tokR) = self.stack.pop()
        if tok == 'unary_op':  # якщо унарний '+' або '-', то лівий операнд знімати вже не треба буде
            self.processing_arith_unary_op(lex, (lexR, tokR))
            return
        # зняти з вершини стека ідентифікатор (лівий операнд)
        (lexL, tokL) = self.stack.pop()

        if (lex, tok) == (':=', 'assign_op'):
            if lexL in self.tableOfVar.keys():
                tokL = self.tableOfVar[lexL][1]
            else:  # elif lexL in self.tableOfNamedConst.keys():
                tokL = self.tableOfNamedConst[lexL][1]
            # print('tokL =', tokL, 'tokR =', tokR)
            if tokL != tokR:
                print(f'(lexR,tokR)={(lexR, tokR)}\n(lexL,tokL)={(lexL, tokL)}')
                raise PSMExcept(7)  # типи змінної відрізняється від типу значення
            else:
                # виконати операцію:
                # оновлюємо запис у таблиці ідентифікаторів
                # ідентифікатор/змінна  =
                #              (index - не змінився,
                #               тип - як у правого операнда (вони однакові),
                #               значення - як у правого операнда)
                if lexL in self.tableOfVar.keys():
                    self.tableOfVar[lexL] = (self.tableOfVar[lexL][0], tokR, get_value(lexR, tokR))
                else:
                    self.tableOfNamedConst[lexL] = (self.tableOfNamedConst[lexL][0], tokR, get_value(lexR, tokR))
        else:
            self.processing_arith_bool_binary_op((lexL, tokL), lex, (lexR, tokR))

    def processing_arith_unary_op(self, arth_bool_op, lex_tok_r):
        (lexR, tokR) = lex_tok_r
        type_r, val_r = self.get_val_type_operand(lexR, tokR)
        self.apply_unary_operator(arth_bool_op, (lexR, type_r, val_r))

    def processing_arith_bool_binary_op(self, lex_tok_l, arth_bool_op, lex_tok_r):
        (lexL, tokL) = lex_tok_l
        (lexR, tokR) = lex_tok_r
        type_l, val_l = self.get_val_type_operand(lexL, tokL)
        type_r, val_r = self.get_val_type_operand(lexR, tokR)
        self.apply_binary_operator((lexL, type_l, val_l), arth_bool_op, (lexR, type_r, val_r))

    def get_val_type_operand(self, lex, tok):
        if tok == "r-val":
            if lex in self.tableOfVar.keys():
                if self.tableOfVar[lex][2] == 'val_undef':
                    raise PSMExcept(8)  # 'неініційована змінна', (lexL,tableOfVar[lexL], (lexL,tokL
                else:
                    type, val = (self.tableOfVar[lex][1], self.tableOfVar[lex][2])
            elif lex in self.tableOfNamedConst.keys():
                type, val = (self.tableOfNamedConst[lex][1], self.tableOfNamedConst[lex][2])
        elif tok == 'int':
            val = int(lex)
            type = tok
        elif tok == 'float':
            val = float(lex)
            type = tok
        elif tok == 'complex':
            val = complex(lex.replace('i', 'j'))
            type = tok
        elif tok == 'boolean':
            val = lex
            type = tok
        return type, val

    def apply_unary_operator(self, unary_op, lex_type_val_r):
        (lexR, typeR, valR) = lex_type_val_r
        if unary_op in ('+', '-'):  # про всяк випадок, якщо в мову будуть додаватися факторіал чи інші унарні оператори
            if typeR == 'string':
                raise PSMExcept(9)
            if unary_op == '-':
                if typeR in ('int', 'float', 'complex'):
                    print(lex_type_val_r)
                    value = -valR  # інверсія
                elif typeR == 'boolean':
                    if valR == 'true':
                        value = 'false'
                    elif valR == 'false':
                        value = 'true'
                else:
                    raise PSMExcept(9)
            elif unary_op == '+':
                value = valR  # нічого не робимо
        else:
            raise PSMExcept(10)
        self.stack.push((str(value), typeR))

    def apply_binary_operator(self, lex_type_val_l, arth_bool_op, lex_type_val_r):
        (lexL, typeL, valL) = lex_type_val_l
        (lexR, typeR, valR) = lex_type_val_r
        resulting_type = typeL
        # if typeL != typeR:
        #     raise PSMExcept(9)  # типи операндів відрізняються
        if arth_bool_op in ('+', '-'):
            if typeL == typeR and typeL == 'int':
                resulting_type = typeL
            elif typeL == 'boolean' or typeR == 'boolean':
                raise PSMExcept(9)
            elif typeL == 'string' or typeR == 'string':
                raise PSMExcept(9)
            elif typeL == 'complex' or typeR == 'complex':
                resulting_type = 'complex'
            else:
                resulting_type = 'float'
            if arth_bool_op == '+':
                # print(valL, type(valL), valR, type(valR))
                value = valL + valR
            elif arth_bool_op == '-':
                value = valL - valR
        elif arth_bool_op in ('*', '/'):
            if typeL in ('boolean', 'string') or typeR in ('boolean', 'string'):
                raise PSMExcept(9)
            if arth_bool_op == '*':
                if typeL == typeR and typeL == 'int':
                    resulting_type = typeL
                elif typeL == 'complex' or typeR == 'complex':
                    resulting_type = 'complex'
                else:
                    resulting_type = 'float'
                value = valL * valR
            elif arth_bool_op == '/':
                if typeL == 'complex' or typeR == 'complex':
                    resulting_type = 'complex'
                else:
                    resulting_type = 'float'
                if valR == 0:
                    raise PSMExcept(10)  # ділення на нуль
                else:
                    value = valL / valR
        elif arth_bool_op == '^':
            if typeL in ('boolean', 'string', 'complex') or typeR in ('boolean', 'string', 'complex'):
                raise PSMExcept(9)
            resulting_type = 'float'
            value = pow(valL, valR)
        # elif arth_bool_op == '/':  # and typeL == 'float':

        # elif arth_bool_op == '/' and typeL == 'int':
        #     value = int(valL / valR)
        elif arth_bool_op in ('<', '<=', '>', '>=', '==', '!='):
            if typeL in ('complex', 'string') or typeR in ('complex', 'string'):
                raise PSMExcept(9)
            if arth_bool_op == '<':
                value = str(valL < valR).lower()
            elif arth_bool_op == '<=':
                value = str(valL <= valR).lower()
            elif arth_bool_op == '>':
                value = str(valL > valR).lower()
            elif arth_bool_op == '>=':
                value = str(valL >= valR).lower()
            elif arth_bool_op == '==':
                value = str(valL == valR).lower()
            elif arth_bool_op == '!=':
                value = str(valL != valR).lower()
        else:
            pass
        # покласти результат на стек
        if arth_bool_op in ('<', '<=', '>', '>=', '==', '!='):
            self.stack.push((str(value), 'boolean'))
        else:
            self.stack.push((str(value), resulting_type))


class PSMExcept(Exception):
    def __init__(self, msg):
        self.msg = msg


def get_value(lex, tok):
    if tok == 'float':
        return float(lex)
    elif tok == 'complex':
        return complex(lex.replace('i', 'j'))
    elif tok == 'int':
        return int(lex)
    elif tok == 'string':
        return str(lex)
    elif tok == 'boolean':
        return lex

# pm1 = PSM('a.tovid')
# pm1.load_postfix_file("a.postfix")  # завантаження .postfix - файла
# pm1.postfix_exec()
