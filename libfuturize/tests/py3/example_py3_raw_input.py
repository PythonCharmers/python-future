"""
Example Python 3 code

Does libfuturize --from3 handle this, or does it add an evil eval() to the
input() call?

It should also add 'from __future__ import print_function'
"""
def greet(name):
    print("Hello, {0}!".format(name))

print("What's your name?")
name = input()
greet(name)
