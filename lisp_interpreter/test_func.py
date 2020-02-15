from utils import  log
"""
最近因刚接触python3，以前接触的时python2，虽然知道有些区别，但作为初学者，还是会碰到各种报错。

比如写一个脚本让用户在屏幕上输入用户名，然后输出到屏幕。

如果要是python2的话会这样写：

username = raw_input( 'username: ')

print（'Welcome', username）

当你在执行的时候就会报错：

Traceback (most recent call last):
  File "001.login.py", line 5, in <module>
    username=raw_input('username:')
NameError: name 'raw_input' is not defined

未定义名称“raw_input”

原因是：rwa_input是2.x版本的输入函数，在新版本环境下会报错，该函数未定义。在3.x版本中应该用input()代替raw_input()。

那么将“raw_input”改成“input”就可已解决了。
"""
# age = int(raw_input("input your age :\n"))
# input = input("raw_input: ")
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

number_end('12+9', 3)


# 计划 （'9', 4）