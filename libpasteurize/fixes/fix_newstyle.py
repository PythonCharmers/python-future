u"""
Fixer for "class Foo: ..." -> "class Foo(object): ..."
"""

from lib2to3 import fixer_base
from lib2to3.fixer_util import Node, Leaf, token, syms, LParen, RParen, Name
# from lib2to3.fixer_util import Name, syms, Node, Leaf, Newline, find_root
from lib2to3.pygram import token

def insert_object(node, idx):
    node.insert_child(idx, RParen())
    node.insert_child(idx, Name(u"object"))
    node.insert_child(idx, LParen())

class FixNewstyle(fixer_base.BaseFix):

    PATTERN = u"classdef< 'class' NAME colon=':' any >"

    def transform(self, node, results):
        colon = results[u"colon"]
        idx = node.children.index(colon)
        insert_object(node, idx)
