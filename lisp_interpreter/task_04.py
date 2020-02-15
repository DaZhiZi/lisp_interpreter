from utils import log,  cut_blank
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
今早起来的时候，我陷入了沉思：“为什么我们学习新知识如此的困难？”

我认为它不仅仅是因为它难。我认为其中的一个原因是因为我们花了大量的时间
和精力通过阅读和观看来获取知识，而没有足够的时间通过练习来将这些知识转化成技能。
比如学习游泳，你可以花很多时间阅读上百本有关游泳的书，和阅历丰富的游泳运动员和教练谈几个小时，观看所有能找到的训练视频，但是当你第一次跳进水里时候，你仍然会像石头一样沉入水底。

底线是：你认为自己对这门学科了解多少并不重要————否则你必须把这些知识付诸实践，
从而把它变成一种技能。为了帮助你锻炼，我把一些练习题放到了第一章和第二章。
是的，你会在今天和以后的文章看到更多更多的练习题，我保证:)

好的，让我们开始今天的素材，不然呢？

目前为止，您已经学会了如何解释两个整数的加减法。比如“7+3”、“12 - 9”。
而今天我们讨论的是如何解析（识别）任意数量的加减法运算，比如“7-3+2-1”.

从图像上看，本文中的算术表达式可以用以下的语法图表示：

什么是语法图呢？语法图是编程语言的语法规则的图形表示。

基本上，语法图可以直观的表示编程语言中允许那些语句，不允许哪些语句。

语法图非常易读：只需要按照箭头所指读下去就行。

一些路径表示选择，一些路径表示循环。

您可以按照如下方式阅读上面的语法图：一个项可选地后面跟着加法或者减法标志，
然后跟着一个项，然后又可选地跟着一个加法或者减法，以此类推。

你粗浅的理解了图片的内容。你可能想知道什么是项（term）呢？ 在本文中，项只是一个整数。

语法图主要有两个用途：

它们以图形方式表示编程语言规范（语法）。
它们可以帮助您编写解析器————您可以无脑的把图片内容“复制”到代码上。
您已经学到了识别Token流中短语的过程叫做解析。
执行该部分的解释器或编译器的部分叫做解析器。解析也称作语法分析，
您猜对了，解析器也恰当地称作语法分析器。

根据上面的语法图，以下所有的算术表达式都是合法的：

3
3 + 4
7 - 3 + 2 - 1
但是表达式“3 +” 不是合法的表达式，因为根据上面的语法图，
加号后面必须有一项，否则就是语法错误。

从我们前面的文章（第一二章）可知，expr方法是我们解析器和解释器都存在的地方。

同样的，解析器只识别结构，确保它遵循规范，而解释器实际上在解析器成功识别后才会计算表达式。

下面的代码片段显示了相应的解析器代码。

语法图中的矩形框成为解析整数的term方法，expr方法仅仅遵循刚才的语法图
def term(self):
    token = self.current_token
    self.eat(INTEGER)
    return token.value

def expr(self):
    # set current token to the first token taken from the input
    self.current_token = self.get_next_token()
    
    result = self.term()
    while self.current_token.type in (PLUS, MINUS):
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            result = result + self.term()
        elif token.type == MINUS:
            self.eat(MINUS)
            result = result - self.term()

    return result
"""
def apply_subtracting(list): # 加减乘除
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

def apply_compare(list): # 大于小于等于
    op = list[1]
    a = list[0]
    b = list[2]
    if op == '>':
        return a > b
    if op == '<':
        return a < b
    if op == '==':
        return a == b


def apply_ops(list): # list 为  [left, op , right]
    op = list[1] # 第二个元素
    if op in '+-*/':
        return apply_subtracting(list)
    else:
        return apply_compare(list)


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


    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    """
    你可以看到expr首先调用了term方法。然后expr方法有一个while循环来计算任意次。
    在循环内部，解析器根据Token来做出选择。花一些时间给自己证明上面的代码确实遵循刚
    才的语法图吧。

    解析器本身不解释任何东西：如果它识别表达式成功，那么它什么也不做，
    如果识别失败，就会抛出语法错误。

    让我们修改一下expr方法并添加解释器代码：
 
    """
    def term(self):
        token = self.current_token
        self.eat(Type.INTEGER)
        return token.value


    def expr(self):
        self.current_token = self.get_next_token()
        list = []
        result = self.term()
        while self.current_token.type is Type.OPERATOR:
            list.append(result) # left
            token = self.current_token
            op = token.value # op
            list.append(op)
            self.eat(Type.OPERATOR)
            right = self.term()  # right
            list.append(right)
            log('list', list)
            result = apply_ops(list)
            list = []   # 清空元素
        return result

"""
 画一个语法图，仅包含乘法和除法表达式，比如“7 * 4 / 2 * 3”
支持仅包含乘法和除法的算术表达式，比如“7 * 4 / 2 * 3”
用其他语言写一个解释器，支持“7 - 3 + 2 - 1”这类的表达式。不要看本文章的例子。考虑一下它需要的东西：词法分析器（它接受把输入转化成Token流）、一个解析器（它从词法分析器提供的Token流中提取，并尝试理解其中的结构），解析器在成功解析后有解释器来解释算术表达式及其结果。将这些碎片串在一起。花一些时间将您获得的知识翻译成算术表达式的解释器吧！
检查你的理解：

什么是语法图？
什么是语法分析？
什么是语法分析器？
敬请关注下一章
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