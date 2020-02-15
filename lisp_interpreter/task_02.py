from utils import log, apply_ops
from enum import Enum


class Type(Enum): # 枚举类型
    INTEGER = 0
    # PLUS = 1
    OPERATOR = 1

    EOF = 2

class Token():
    def __init__(self, token_type=None, value=None):
        self.type = token_type      # token  type
        self.value = value          # token  value

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
    i = index   # 下一个元素 索引
    numbers = '0123456789'
    while(found(numbers, codes[i])):
        i += 1
        if i >= len(codes):
            break
    r = codes[index: i]
    return (r, i-1)


class Interpreter(object):
    def __init__(self, text): #  终端输入的字符串, e.g. "3+5"
        self.text = text    # text  可以看成 token 的集合  tokens
        self.pos = 0        # 文本开始的索引  默认为 0
        self.current_token = None  # 当前的 token 默认 None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        text = self.text
        last_index = len(text) - 1
        if self.pos > last_index: # 是否是最后一个元素
            return Token(Type.EOF, None)

        current_char = text[self.pos] # 当前字符

        if current_char.isdigit(): # 是否是数字类型
            left = self.pos
            # number_end('12+9', 3)
            (r, right) = number_end(text, left)
            current_chars = r
            token = Token(Type.INTEGER, int(current_chars))
            self.pos = right + 1
            # self.pos += 1  # 类似计时器 类似指针 space单位间隔 为 1
            log('self.pos', self.pos)
            return token

        ops = '+-*/' +  '><=='
        if current_char in ops: # 是否是 + 类型
            op = current_char
            log('op', op)
            if op == '=':
                op = '=='
                self.pos += 2
            else:
                self.pos += 1
            token = Token(Type.OPERATOR, op)
            log('self.pos', self.pos)
            return token

        self.error() # 错误

    """
    expr 方法本身使用方法eat来验证传递给其的参数与当前Token是否一致。

    匹配传递的令牌类型后，eat方法获取下一个Token并将其赋值给currentToken，
    从而有效的“吃掉”当前匹配的Token并且推进了Token流中的虚拟指针（pos）。
    如果不对应，eat方法会抛出异常。
    """
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()


    def expr(self):
        list = []
        self.current_token = self.get_next_token()
        left = self.current_token
        self.eat(Type.INTEGER)
        log('left', left)


        op = self.current_token
        self.eat(Type.OPERATOR)

        right = self.current_token
        self.eat(Type.INTEGER)
        log('right', right)

        list.append(op.value)  # list [op, left, right]
        list.append(left.value)
        list.append(right.value)

        result = apply_ops(list)
        return result


"""
修改代码来允许输入多位整数，例如“12+3”
添加一个跳过空格的办法，让您的计算器可以处理带有空格的字符串输入，比如“ 12 + 3”
支持“-”运算符，比如“7-5”这样的减法。 8*8
支持比较运算： 8>24  False  24>8 True  24==24 True
"""
def main():
    while True:
        try:

            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()