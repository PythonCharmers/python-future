"""
Example Python 2 code with print statement and raw_input().

Check: does libfuturize automatically handle this?
"""

def greet(name):
    print "Hello, {0}!".format(name)

print "What's your name?"
name = raw_input()
greet(name)
