from utils import log, cut_blank
from enum import Enum

"""

在之前的文章里，你已经学习了如何解析和解释任意个整数的加减计算表达式，
比如“7 - 3 + 2 - 1”。你也学到了有关语法图和如何使用它们来描述编程语言的语法。

今天，你将要学到如何去解析解释任意个整数的乘除计算表达式，
比如“7 * 4 / 2 * 3”。本章将划分的是整数除法，所以“9 / 4”，结果会是“2”。

我也会谈一谈另一个广泛使用的，用于指定编程语言的语法的表示法————
上下文无关语法（context-free grammars），简称语法（grammars）或者 BNF（Backus-Naur Form）。出于本文的目的，我不会使用纯的BNF表示法，而是像修改过的EBNF表示法。

用这种语法的几个原因：

grammar以简洁的方式指定编程语言语法。与语法图不同，语法非常的紧凑。
您将在以后的文章中看到我越来越多的使用这种语法。
grammar可以作为很好的文档。
即使你从头开始写编译器，grammar也是一个很好的开始。通常，
您可以通过遵循一组简单的规则将语法转换为代码。
有一种工具，称作解析器生成器，它们接受语法作为输入，
然后根据语法自动生成解析器。本文将在最后讨论这些工具。
现在，让我们开始讨论语法的机械方面吧？

这是一个描述算术表达式的语法，如“7 * 4 / 2 * 3”（它只是语法可以被生成的种多表达式之一）
"""


class Type(Enum):  # 枚举类型
    INTEGER = 0
    # PLUS = 1
    OPERATOR = 1
    EOF = 2


class Token():
    def __init__(self, token_type=None, value=None):
        self.type = token_type  # token  type
        self.value = value  # token  value

    def __repr__(self):
        s = 'type: {}, len: {}, value: {}'.format(self.type, len(str(self.value)), self.value)
        s = '"{}"'.format(self.value)
        return s


def found(string, element):
    r = False
    e = element
    s = string
    if s.find(e) != -1:
        r = True
    return r


# 查找数字结尾的函数
# 返回数字和最后一个数字的索引
# index 是第一个数字的索引
def number_end(codes, index):
    r = ''
    i = index  # 下一个元素 索引
    numbers = '0123456789'
    while (found(numbers, codes[i])):
        i += 1
        if i >= len(codes):
            break
    r = codes[index: i]
    return (r, i - 1)


def ops_num(str):
    i = 0
    numbers = '1234567890'
    for s in str:
        if s not in numbers:
            i += 1
    return i


def apply_subtracting(list):  # 加减乘除
    op = list[1]
    a = list[0]
    b = list[2]
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    if op == '/':
        return a / b


def apply_compare(list):  # 大于小于等于
    op = list[1]
    a = list[0]
    b = list[2]
    if op == '>':
        return a > b
    if op == '<':
        return a < b
    if op == '==':
        return a == b


def apply_ops(list):  # list 为  [left, op , right]
    op = list[1]  # 第二个元素
    if op in '+-*/':
        return apply_subtracting(list)
    else:
        return apply_compare(list)

class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "3 * 5", "12 / 3 * 4", etc
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        """Advance the 'pos' pointer and set the 'current_char' variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):  # 处理数字  多个字符
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def operator(self):
        ops = '+-*/' + '><=='
        op = self.current_char
        if op is not None and op in ops:
            if op == '=':
                op = '=='
                self.pos += 1
            self.current_char = op
            self.advance()
        return op

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                token = Token(Type.INTEGER, self.integer())
                return token

            ops = '+-*/' + '><=='
            if self.current_char in ops:  # 是否是 + 类型
                token = Token(Type.OPERATOR, self.operator())
                return token

            self.error()

        return Token(Type.EOF, None)


class Interpreter(object):
    def __init__(self, lexer):  # 终端输入的字符串, e.g. "3+5"
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')


    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()


    def factor(self):
        """Return an INTEGER token value.

        factor : INTEGER
        """
        token = self.current_token
        self.eat(Type.INTEGER)
        return token.value


    def expr(self):
        list = []
        result = self.factor()
        while self.current_token.type is Type.OPERATOR:
            list.append(result)  # left
            token = self.current_token
            op = token.value  # op
            list.append(op)
            self.eat(Type.OPERATOR)
            right = self.factor()  # right
            list.append(right)
            log('list', list)
            result = apply_ops(list)
            list = []  # 清空元素
        return result


"""
什么是上下文无关语法？
语法有多少规则？
什么是终结符？（找到图中所有的）
什么是非终结符？（同上）
什么是规则的头？
什么是规则的正文？
什么是语法的起始符号
"""


def main():
    while True:
        try:

            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        # 先删掉空格
        # t = cut_blank(text)
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()