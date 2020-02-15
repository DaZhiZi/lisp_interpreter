from utils import log, apply_ops, cut_blank
from enum import Enum
"""
在一本有趣的书————《有用思维的五要素》中，作者Burger和Starbird分享了
他们如何观察Tony Plig，一个国际知名的小号演奏家，为优秀的小号演奏者开了
一个大师班的故事。学生们首先演奏复杂的音乐短句，并且他们演奏的非常好。
但后来他们被要求演奏非常基础、简单的音符。当他们演奏音符时候，与先前的
复杂短句相比，这些音符显得十分幼稚。他们完成演奏后，老师也演奏了相同的音符，
但是当他演奏的时候，却不显得幼稚。差异让人惊讶。Tony解释说，掌握简单的音
符能够让人更好的控制复杂的曲子。这个例子很明确————想要掌握精湛的技术，
必须注重简单、基础的思想。

故事中的启示不仅仅适用于音乐，也适用于软件开发。这个故事提醒我们不要忽视在基础
、简单的想法上埋工夫的重要性。即使有时候干这些事情像是在退步
。虽然熟练使用您使用的工具或者框架非常重要，但是其背后的原理也非常重要。

“如果你只学习方法，那么你只会方法；但如果你学习原理，那么你可以定义你自己的方法。”
话题转回来，我们继续深入研究解释器和编译器。

今天，我将给你展示第一章中计算器的新版本，这个版本更够：

处理字符串中任何位置的空白字符
从输入中处理多位整数
支持减法（之前目前只能加法）  上一个 支持： +-*/  ><==
"""

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


def ops_num(str):
    i = 0
    numbers = '1234567890'
    for s in str:
        if s not in numbers:
            i += 1
    return i
"""
与第一版相比，主要的代码变成了：

方法getNextToken方法稍微重构了一下，增加pos指针的逻辑被抽象到了新的方法advance
增添了两个新方法，skipWhitespace用于忽略空格字符，integer用于处理多位整数
除了 INTEGER -> PLUS -> INTEGER 之外，
我们还增加了 INTEGER -> MINUS -> INREGER 短语。现在还能成功的识别加法或者减法
在第一部分，您学习了两个重要的概念，Token和词法分析器。

今天我想谈谈Lexemes、parsing和parsers。

你已经知道了Token。但是为了让我们完成对Token的讨论，我们需要谈一谈Lexemes。

什么是Lexeme？

Lexeme是一系列形成Token的字符。在下面的图片中，
您可以看到Token和lexemes的一些例子，
希望它能使它们之间的关系变得清晰一点：
现在，还记得我们的老朋友，expr方法吗？

我之前说过，这就是算术表达式实际发生的地方。但在你解析一个表达式之前，
你首先要识别出它们是什么类型的短语，例如，它是加法，还是减法。

这就是expr方法的本质工作：他从getNextToken方法中获取标记流中的结构，
然后解释已经识别的短语，生成算术表达式。

在Token流查找结构的过程，或换句话说，
识别Token流的短语的过程称作解析（Parsing）。
执行该工作的解释器或编译器的一部分乘坐解析器（Parser）。

所以，你现在知道了expr方法是你的解释器的一部分，
它同时解析和解释句子。

expr方法首先尝试解析 INTEGER - > PLUS - > INTEGER或INTEGER - > MINUS - > INTEGER
短语的Token流，并在识别成功后将加法或减法的结果返回给调用者。

然后，又到了练习时间。
"""
class Interpreter(object):
    def __init__(self, text): #  终端输入的字符串, e.g. "3+5"
        self.text = text    # text  可以看成 token 的集合  tokens
        self.pos = 0        # 文本开始的索引  默认为 0
        self.current_token = None  # 当前的 token 默认 None
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
        result = ''
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

        op = self.current_token
        self.eat(Type.OPERATOR)

        right = self.current_token
        self.eat(Type.INTEGER)
        # log('right', right)

        list.append(op.value)  # list [op, left, right]
        list.append(left.value)
        list.append(right.value)

        result = apply_ops(list)
        log('result', result)
        return result

"""
扩展两位数的乘法
扩展两位数的除法
修改代码，支持任意数量的加法或减法。例如“9-5+3 + 11”
检查你的理解：

啥是Lexeme？
Token流中查找结构的进程名称是什么？
解析Token流的部分叫什么？
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
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()