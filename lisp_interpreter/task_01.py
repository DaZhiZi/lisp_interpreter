from utils import log

INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'

"""
为啥你会去学编译器和解释器呢？我给你三个理由

要写一个解释器/编译器，那么你必须一起使用许多的技术。
写一个编译器或解释器将帮助你提升这些技能并且变成一个更牛逼的软件开发者。
同样的，这些你将学到的技能是在写任何程序时候都是很有用的，而不仅仅局限于解释器或编译器。
你真的想知道计算机时如何工作的。解释器和编译器通常看起来和魔术一样。
而且你不会对这些魔术感到满意。您想要揭开解释器和编译器的神秘面纱，
理解它们如何工作，以及控制事务的过程。
你想要编写属于你自己的编程语言或DSL（领域特殊语言）。
如果你设计了一个语言，那么你也得去给它写一个解释器或编译器。
最近掀起了一股创造编程语言之风。你也可以看到一个个新语言涌现：Elixir、Go、Rust等等。
Ok，那么啥是解释器，啥是编译器呢？？？

解释器或编译器的目标是把更高级的源代码翻译成另外一种形式。很模糊吧？带着疑问，
之后的系列你将会学会源代码到底翻译成什么的细节。

此刻，你可能也想知道解释器和编译器的区别是什么。这一系列的目的只是为了简单起见
，我们认为，如果翻译器将源代码翻译成机器语言，那他就是编译器。
如果一个翻译器处理并且运行了源代码，而且没有翻译它到机器语言，那他就是解释器。
"""
"""
我希望目前为止你真的想学习、构建一个解释器和编译器。你对本系列的解释器有什么期待呢？

答案是这样的。你和我将给Pascal语言的大子集写一个简单的解释器。本系列的最后，
你将有一个高效的Pascal解释器和一个像Python的pdb一样的代码级别的调试器。

你可能会问，为啥是Pascal呢？一方面，Pascal不是仅仅为了写这篇文章而虚构出的语言：
真的存在这个语言，它还有许多重要的语言结构。并且有一些古老但是有用的计算机科学书籍，
用着Pascal语言写着Example（我知道这不是一个令人信服的理由，来让人选择给它写一个解释器，
但是学习一个非流行语言至少会很好）

接下来是一段Pascal中的阶乘函数的例子。你将用自己的解释器来运行它，并且在此过程中，
你将写一个交互式的源代码调试器来调试它。
 
"""
"""
program factorial;

function factorial(n: integer): longint;
begin
    if n = 0 then
        factorial := 1
    else
        factorial := n * factorial(n - 1);
end;

var
    n: integer;

begin
    for n := 0 to 16 do
        writeln(n, '! = ', factorial(n));
end.
"""

"""
OK，让我们开始！

你将通过编写一个简单的算数表达式解释器（计算器），
开始首次涉足解释器和编译器。今天的目标非常简约：让你的计算器能够处理两位整数相加，
比如 3+5。这是你的计算器的源代码，不对，是解释器：
"""

class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF
        self.type = type
        # token value: 0, 1, 2. 3, 4, 5, 6, 7, 8, 9, '+', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        text = self.text

        # is self.pos index past the end of the self.text ?
        # if so, then return EOF token because there is no more
        # input left to convert into tokens
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        # get a character at the position self.pos and decide
        # what token to create based on the single character
        current_char = text[self.pos]

        # if the character is a digit then convert it to
        # integer, create an INTEGER token, increment self.pos
        # index to point to the next character after the digit,
        # and return the INTEGER token
        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        self.error()

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # we expect the current token to be a single-digit integer
        left = self.current_token
        self.eat(INTEGER)

        # we expect the current token to be a '+' token
        op = self.current_token
        self.eat(PLUS)

        # we expect the current token to be a single-digit integer
        right = self.current_token
        self.eat(INTEGER)
        # after the above call the self.current_token is set to
        # EOF token

        # at this point INTEGER PLUS INTEGER sequence of tokens
        # has been successfully found and the method can just
        # return the result of adding two integers, thus
        # effectively interpreting client input
        result = left.value + right.value
        return result


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

"""
为了使您的计算器正常工作，您还必须遵守以下规则：

仅仅输入个位数相加
目前唯一支持的操作只有加法
输入中不允许有空格
为了保持计算器简单，这些限制是有必要的。不要担心，代码很快就会变得很复杂。

现在，我们深入了解你的解释器的工作原理，以及它如何鉴别算术表达式。

当你在控制行里输入表达式“3+5”时候，你的解释器获取了一个字符串“3+5”，
为了让解释器真正理解如何处理该字符串，首先需要将输入“3+5”分解成为称
作Token的组件。一个Token是一个带有类型和值的对象。比如，对于字符“3”，
它的类型会是INTEGER，对应的值将是整数3。

将输入字符串分解为标记的过程称为词法分析（lexical analysis）。
所以，你的解释器第一步就是读取输入的字符并且将他们转换成一串Token。
执行此操作的解释器部分称为词法分析器（lexical analyzer），
或者简称 Lexer。你可能还会遇到同一组件的其他说法，比如Scanner或者Tokenizer。
但他们都是一个意思：用于将字符输入转换成Token流，作为解释器或者编译器的一部分。

Interpreter类的方法getNextToken是你的词法分析器。每次调用它时候，
都会从传给解释器的字符串中创建下一个Token。我们细看一下方法
本身是如何将字符转换成Token的。输入存储在变量text中，
pos是一个字符串的索引（把字符串视为字符数组）。

最初pos指向字符“3”。该方法首先检查其是否是数字，如果是，
则返回值为3的INTEGER的Token实例并pos递增。

    text
    
    0   1   2
    3   +   5       Token(Type.interger, 3)
    
    position = 0
"""

"""
然后pos现在指向了“+”，下一次调用这个方法
，他检测了字符是否为数字，然后检测字符是否是加号，他的确是。 
最后返回了一个新的“+”值的PLUS类型的Token，然后pos递增。
 
    text
    
    0   1   2
    3   +   5       Token(Type.plus, 3)
    
    position = 1
    
"""

"""
同理（译者不想翻译这段了）

    text
    
    0   1   2
    3   +   5       Token(Type.interger, 3)
    
    position = 2
"""

"""
因为pos现在已经指过了“3+5”，之后每次调用getNextToken时会返回EOF
    
    text
    
    0   1   2   3
    3   +   5   空    Token(Type.efo, None)
    
    position = 2

"""

"""

既然你的解释器可以访问由输入字符组成的Token流，那么解释器还需要对它做一点事情：需要在lexergetNextToken的Token流中找到结构。

至少您希望解释器找到如下结构

INTEGER -> PLUS -> INTEGER

也就是说，他试图找到一些列Token：整数后面跟一个加号，紧接着一个整数

赋值查找和解释该结构的方法应该是expr。这个方法验证了Token序列确实是想象中的序列，
即INTEGER -> PLUS -> INTEGER。 在成功确认结构后，它通过将+左右两边的Token相加得到结果。
从而成功的传递给解释器结果。

expr 方法本身使用方法eat来验证传递给其的参数与当前Token是否一致。

匹配传递的令牌类型后，eat方法获取下一个Token并将其赋值给currentToken，
从而有效的“吃掉”当前匹配的Token并且推进了Token流中的虚拟指针（pos）。如果不对应，eat方法会抛出异常。

让我们回顾一下您的解释器为计算一个算术表达式所作的事情：

解释器接受一个输入的字符串，比如“3+5”
解释器调用了expr方法在词法分析器getNextToken来找到Token流中的结构。
他试图找到INTEGER、PLUS、INTEGER的形式。确认结构后，
它相加两个INTEGER的Token的值来解释输入，因为这时解释器清楚它需要做的就是将3和5相加。
祝贺自己。你刚刚学会了如何构建您的第一个解释器！

现在是练习的时候了。
你不会认为读这篇文章就够了吧？对吧？

接下来是一些练习

修改代码来允许输入多位整数，例如“12+3”
添加一个跳过空格的办法，让您的计算器可以处理带有空格的字符串输入，比如“ 12 + 3”
支持“-”运算符，比如“7-5”这样的减法。
检查你的理解：

什么是解释器？

什么是编译器？

解释器和编译器的区别？

Token是什么？ 
type  value:
    type:
        plus
        int
        eof
    value:
        +
        1234567890
        None

将输入分解为Token的过程叫什么？
str:
    tokens:
        token:

词法分析所称的解释器部分叫啥？

解释器或者编译器的那一部分的其他常用名字是什么？
"""