from utils import log, cut_blank
from enum import Enum



class Type(Enum):  # 枚举类型
    INTEGER = 0
    # PLUS = 1
    OPERATOR = 1  # +-
    MUL_DIV = 2  # */
    GREATER_LESS = 3  # ><==
    EOF = 4
    LPAREN = 5  # ( )
    RPAREN =6



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
        ops = '+-'
        op = self.current_char
        if op is not None and op in ops:
            self.current_char = op
            self.advance()
        return op

    def mul_div(self):
        ops = '*/'
        op = self.current_char
        if op is not None and op in ops:
            self.current_char = op
            self.advance()
        return op
        pass

    def greater_less(self):
        ops = '><=='
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

            operators = '+-'
            if self.current_char in operators:  # 是否是 + 类型
                token = Token(Type.OPERATOR, self.operator())
                return token

            muls = '*/'
            if self.current_char in muls:  # 是否是 */ 类型
                token = Token(Type.MUL_DIV, self.mul_div())
                return token

            greaters = '><=='
            if self.current_char in greaters:  # 是否是 ><== 类型
                token = Token(Type.GREATER_LESS, self.greater_less())
                return token


            if self.current_char == '(':
                self.advance()
                return Token(Type.LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(Type.RPAREN, ')')

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
        """factor : INTEGER | LPAREN expr RPAREN"""
        token = self.current_token
        if token.type == Type.INTEGER:
            self.eat(Type.INTEGER)
            return token.value
        elif token.type == Type.LPAREN:
            self.eat(Type.LPAREN)
            result = self.expr()
            self.eat(Type.RPAREN)
            return result


    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        list = []
        result = self.factor()
        while self.current_token.type is Type.MUL_DIV:
            list.append(result)  # left

            token = self.current_token
            op = token.value
            list.append(op)  # op

            self.eat(Type.MUL_DIV)
            right = self.factor()
            list.append(right)  # right

            result = apply_ops(list)
            list = []  # 清空元素
        log('result', result)
        return result

    def expr(self):
        list = []
        result = self.term()
        log('expr result', result)
        while self.current_token.type in [Type.OPERATOR, Type.MUL_DIV]:
            list.append(result)  # left
            token = self.current_token
            op = token.value  # op
            list.append(op)
            self.eat(Type.OPERATOR)

            right = self.term()  # right
            list.append(right)
            log('list', list)
            result = apply_ops(list)
            list = []  # 清空元素
        return result


"""
语言实现模式:创建您自己的特定于域的通用编程语言(实用程序员)

编写编译器和解释器:一种软件工程方法

Java中的现代编译器实现

现代编译器设计

编译器:原理、技术和工具(第二版)
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