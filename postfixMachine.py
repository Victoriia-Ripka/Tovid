# -------------------------------------------------------
# code generation
# -------------------------------------------------------

import re
from stack import Stack


class PSM():             # Postfix Stack Machine
  def __init__(self, file_name):
    self.tableOfId = {}
    self.tableOfLabel = {}
    self.tableOfConst = {}
    self.postfixCode = []
    self.mapDebug = {}
    self.numLine = 0
    self.file_name = file_name
    self.file = ""
    self.slt = ""
    self.headSection = {"VarDecl": ".vars(", "LblDecl": ".labels(", "ConstDecl": ".constants(", "Code": ".code("}
    self.errMsg = {1: "неочікуваний заголовок",
                   2: "тут очікувався хоч один порожній рядок",
                   3: "тут очікувався заголовок секції",
                   4: "очікувалось два елемента в рядку",
                   8: "неініційована змінна"
                   }
    self.stack = Stack()
    self.numInstr = 0
    self.maxNumbInstr = 0

  def load_postfix_file(self, file_name):
    try:
      self.fileName = file_name + ".tovid"
      self.file = open(self.file_name, 'r')
      self.parse_postfix_program()
      self.file.close()
    except PSMExcept as e:
      print(f"PSM.loadPostfixFile ERROR: у рядку {self.numLine}, код винятку - {e.msg}, msg = {self.errMsg[e.msg]}")

  def parse_postfix_program(self):
      # print("--------- header ")
      self.parse_header(".target: Postfix Machine")
      # print(f"have header1 {self.numLine}")
      self.parse_header(".version: 0.2")
      # print(f"have header2 {self.numLine}")

      self.parse_section("VarDecl")
      # print(f"have var {self.numLine}")

      self.parse_section("LblDecl")
      # print("have lbl ")

      self.parse_section("ConstDecl")
      # print("have const ")

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
              table = self.tableOfId
              indx = len(table) + 1
              table[item1] = (indx, item2, 'val_undef')

          if section == "LblDecl":
              table = self.tableOfLabel
              indx = len(table) + 1
              table[item1] = item2

          if section == "ConstDecl":
              table = self.tableOfConst
              indx = len(table) + 1
              if item2 == "int":
                  val = int(item1)
              elif item2 == "float":
                  val = float(item1)
              elif item2 == "bool":
                  val = item1
              table[item1] = (indx, item2, val)

          if section == "Code":
              indx = len(self.postfixCode)
              self.postfixCode.append((item1, item2))
              instrNum = len(self.postfixCode) - 1
              self.mapDebug[instrNum] = self.numLine

  def postfix_exec(self):
      "Виконує postfixCode"
      print('postfixExec:')
      self.maxNumbInstr = len(self.postfixCode)
      try:
          while self.numInstr < self.maxNumbInstr:
              self.stack.print()
              lex, tok = self.postfixCode[self.numInstr]
              if tok in ('int', 'float', 'l-val', 'r-val', 'label', 'bool'):
                  self.stack.push((lex, tok))
                  self.numInstr = self.numInstr + 1
              elif tok in ('jump', 'jf', 'colon'):
                  self.do_jumps(lex, tok)
              elif tok == 'out_op':
                  id, _ = self.stack.pop()
                  self.numInstr = self.numInstr + 1
                  print(f'-------------- OUT: {id}={self.tableOfId[id][2]}')
              else:
                  print(f'-=-=-=========({lex},{tok})  numInstr={self.numInstr}')
                  self.do_it(lex, tok)
                  self.numInstr = self.numInstr + 1
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
      # зняти з вершини стека ідентифікатор (правий операнд)
      # self.stack.print()
      (lexR, tokR) = self.stack.pop()
      # зняти з вершини стека запис (лівий операнд)
      (lexL, tokL) = self.stack.pop()

      if (lex, tok) == (':=', 'assign_op'):
          tokL = self.tableOfId[lexL][1]
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
              self.tableOfId[lexL] = (self.tableOfId[lexL][0], tokR, get_value(lexR, tokR))
      else:
          self.processing_arth_bool_op((lexL, tokL), lex, (lexR, tokR))

  def processing_arth_bool_op(self, lex_tok_l, arth_bool_op, lex_tok_r):
      (lexL, tokL) = lex_tok_l
      (lexR, tokR) = lex_tok_r
      type_l, val_l = self.get_val_type_operand(lexL, tokL)
      type_r, val_r = self.get_val_type_operand(lexR, tokR)
      self.apply_operator((lexL, type_l, val_l), arth_bool_op, (lexR, type_r, val_r))

  def get_val_type_operand(self, lex, tok):
      if tok == "r-val":
          if self.tableOfId[lex][2] == 'val_undef':
              raise PMExcept(8)  # 'неініційована змінна', (lexL,tableOfId[lexL], (lexL,tokL
          else:
              type, val = (self.tableOfId[lex][1], self.tableOfId[lex][2])
      elif tok == 'int':
          val = int(lex)
          type = tok
      elif tok == 'float':
          val = float(lex)
          type = tok
      elif tok == 'bool':
          val = lex
          type = tok
      return (type, val)

  def apply_operator(self, lex_type_val_l, arth_bool_op, lex_type_val_r):
      (lexL, typeL, valL) = lex_type_val_l
      (lexR, typeR, valR) = lex_type_val_r
      if typeL != typeR:
          raise PMExcept(9)  # типи операндів відрізняються
      elif arth_bool_op == '+':
          value = valL + valR
      elif arth_bool_op == '-':
          value = valL - valR
      elif arth_bool_op == '*':
          value = valL * valR
      elif arth_bool_op == '/' and valR == 0:
          raise PMExcept(10)  # ділення на нуль
      elif arth_bool_op == '/' and typeL == 'float':
          value = valL / valR
      elif arth_bool_op == '/' and typeL == 'int':
          value = int(valL / valR)
      elif arth_bool_op == '<':
          value = str(valL < valR).lower()
      elif arth_bool_op == '<=':
          value = str(valL <= valR).lower()
      elif arth_bool_op == '>':
          value = str(valL > valR).lower()
      elif arth_bool_op == '>=':
          value = str(valL >= valR).lower()
      elif arth_bool_op == '=':
          value = str(valL == valR).lower()
      elif arth_bool_op == '<>':
          value = str(valL != valR).lower()
      else:
          pass
      # покласти результат на стек
      if arth_bool_op in ('<', '<=', '>', '>=', '=', '<>'):
          self.stack.push((str(value), 'bool'))
      else:
          self.stack.push((str(value), typeL))


class PSMExcept(Exception):

  def __init__(self, msg):
    self.msg = msg


def get_value(lex, tok):
      if tok == 'float':
          return float(lex)
      elif tok == 'int':
          return int(lex)
      elif tok == 'bool':
          return lex


postfix_code = []


def postfix_code_gen(case, to_tran):
    global postfix_code
    if case == 'lval':
        lex, tok = to_tran
        postfix_code.append((lex, 'l-val'))
    elif case == 'rval':
        lex, tok = to_tran
        postfix_code.append((lex, 'r-val'))
    else:
        lex, tok = to_tran
        postfix_code.append((lex, tok))


# pm1.loadPostfixFile("")  # завантаження .postfix - файла
# pm1.postfix_exec()