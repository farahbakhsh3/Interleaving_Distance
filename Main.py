from anytree import Node, RenderTree

udo = Node("Udo")
marc = Node("Marc", parent=udo)
lian = Node("Lian", parent=marc)
dan = Node("Dan", parent=udo)
jet = Node("Jet", parent=dan)
jan = Node("Jan", parent=dan)
joe = Node("Joe", parent=dan)

print(udo)
# Node('/Udo')
print(joe)
# Node('/Udo/Dan/Joe')

for pre, fill, node in RenderTree(udo):
    print("%s%s" % (pre, node.name))
# Udo
# ├── Marc
# │   └── Lian
# └── Dan
#     ├── Jet
#     ├── Jan
#     └── Joe

print(dan.children)
# (Node('/Udo/Dan/Jet'), Node('/Udo/Dan/Jan'), Node('/Udo/Dan/Joe'))

class MyBaseClass(object):  # Just an example of a base class
   foo = 4
class MyClass(MyBaseClass, NodeMixin):  # Add Node feature
    def __init__(self, name, length, width, parent=None, children=None):
       super(MyClass, self).__init__()
       self.name = name
       self.length = length
     self.width = width
         self.parent = parent
         if children:  # set children only if given
            self.children = children