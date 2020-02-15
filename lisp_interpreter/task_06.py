from utils import log, cut_blank
from enum import Enum

"""
你如何解决一个复杂度与理解、创造一个解释器或编译器一样的事情呢？ 
一开始它看起来非常像一堆乱七八糟的纱线，你需要解开才能得到完美的球。

解决方法就是一次解开一根线，一次一个结。 有时候，
你可能觉得自己不会马上理解某些事情，但你必须坚持下去。 
如果你足够坚持，你最终会清醒，我保证（诶呀，
以前如果我每次不明白的话就放25美分，那么我很久以前就是个富人了）

在理解如果写一个解释器和编译器的过程中，
我可能会给你最好的建议之一就是阅读文章中的源代码，
甚至编写相同的代码。来使你感觉这些东西和代码对你来说十分自然，
然后学习新的主题。不要匆忙，只是放慢速度，花时间深入理解基本思想。
 这种看似缓慢的方法将在未来取得成效，相信我。

你最追将获得最完美的纱线球。 而且，你知道什么吗？
即使它并不是那么完美，但它仍然比啥也不做、不主动学习，
或者快速阅读然后忘了它的方案更好。

记住，保持一次解开一个结，一次一根线。并通过编写代码来练习你所学到东西
 今天，您将使用您从系列之前的文章中学到的所有知识，
 并学习如何解析和解释任何数量的加减乘除的算术表达式。
 您将编写一个能够解释“14 + 2 * 3 - 6 / 2”的表达式解释器。

在深入研究并编写一些代码之前，我们先讨论一下运算符的关联性和优先级。

按照约定，7 + 3 + 1 与 （7 + 3） + 1 相同，
7 - 3 - 1 相当于（7 - 3）- 1，这里没有变化。
我们都在某一时刻学会了这一点，并从那时起就把它视为理所当然。
如果我们将7 - 3 - 1 视作 7 - （3 - 1），那么结果就是5而不是3。

在通常的算术和大多数编程语言中，加减乘除法是左结合的：

7 + 3 + 1 相当于 (7 + 3) + 1
7 - 3 - 1 相当于 (7 - 3) - 1
8 * 4 * 2 相当于 (8 * 4) * 2
8 / 4 / 2 相当于 (8 / 4) / 2


那么操作符左结合意味着什么呢？

当表达式7 + 3 + 1 中，3的两边都有加号时，我们需要一个约定来决定哪个运算符适用于3。
左边还是右边？+运算符关联到左边，因为两边都有左关联的加号运算符，
所以我们说加法运算符是左关联的。 这就是为什么7 + 3 + 1相当于（7 + 3）+ 1的结合性约定。

好吧，那么像7 + 5 * 2这样的表达式，我们5的两边有着不同类型的运算符？
 表达式是否相当于7 + （5 * 2）或者（7 + 5）* 2 我们如何解决这种歧义呢？

在这种情况下，结合性约定对我们没有帮助，因为他仅仅适用于一种运算符，
可以是（+，-）或（*，/）。 我们在同一个表达式中有着不同类型的运算符时，
我们需要另一个约定来解决歧义。 我们需要定义运算符的相对优先级。

所以：我们说如果操作符在*或+之前取其操作数，那么它就具有更高优先级。
在我们所知和使用中，乘法和除法比加减法有更高的优先级。 
所以表达式7 + 5 * 2相当于7 + （5 * 2），7 - 8 / 4 相当于 7 - （8 / 4）。

在我们有一个具有相同优先级的运算符表达式的情况下，我们只关心从左往右执行

7 + 3 - 1 相当于 (7 + 3) - 1
8 / 4 * 2 相当于 (8 / 4) * 2
我希望你不要因为谈论操作符的关联性和优先级而让你想到生死。 
关于这些约定的好处是我们可以从表中构造算术表达式的语法，
该表显示了算术运算符的关联性和优先级。 然后，我们可以按照第四章概的指南将语法翻译成代码，
除了关联性之外，我们的解释器还能够处理运算符的优先级

这是我们的优先级表：



从表中可以看出，运算符 + 和 - 具有相同的优先级，并且他们都是左关联的。 您还可以看到 * 和 / 也是左关联的，它们具有相同的优先级，但具有比加减法更高的优先级。

以下是我们如何从优先级表构造语法的规则：

对于每个优先级定义一个非终止符，非终止符的产生式主体应该包含来自该级别的运算符和非终止符的下一个更高级别的优先级。
为基本的表达式单元创建一个额外的非终止符因子，在我们的例子中是整数。一般的规则是，如果您有N级优先级，那么总共需要N + 1个非终止符；每个级别一个非终止加一个基本表达式单元的非终止符。
继续！

让我们遵循规则并构建我们的语法。

通过规则1，我们将定义两个非终止符：一个非终止符称作expr给第二级和一个称作term的非终止符为第一级。并且通过遵循规则2，我们将为算术表达式的基本单位————整数，定义一个非终止符因子。

我们新语法的开始符号是expr，expr的产生式会包含一个表示使用第二级运算符的主体。在我们的例子中，这个主体的运算符是+和-，并包下一个更高优先级的term非终止符，level 1

 
"""


class Type(Enum):  # 枚举类型
    INTEGER = 0
    # PLUS = 1
    OPERATOR = 1  # +-
    MUL_DIV = 2  # */
    GREATER_LESS = 3  # ><==
    EOF = 4


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
                token = Token(Type.Type.GREATER_LESS, self.greater_less())
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


    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        list = []
        result = self.factor()
        while self.current_token.type is Type.MUL_DIV:
            list.append(result)  # left

            token = self.current_token
            op = token.value
            list.append(op)      # op

            self.eat(Type.MUL_DIV)
            right = self.factor()
            list.append(right)  # right

            result = apply_ops(list)
            list = []           # 清空元素
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