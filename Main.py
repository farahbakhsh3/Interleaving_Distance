from anytree import Node, RenderTree, NodeMixin
import math

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
    pass

class MyTree(RenderTree):
    def __init__(self, root):
        self.root = root
        root.parent.parent = root

    class MyNode(Node):  # Add Node feature
        def __init__(self, name, length, x, y, parent=None, children=None):
           super(Node, self).__init__() #! super(MyNode)
           self.name = name
           self.length = length
           self.x = x
           self.y = y
           self.parent = parent
           if children:
              self.children = children

    def fill_length(self):
        self.fill_length_inside(self.root)

    def fill_length_inside(self, node):
        for n in node.children:
            k = math.sqrt(math.pow(n.x-node.x,2) + math.pow(n.y-node.y,2))+ node.length
            n.length = k
            self.fill_length_inside(n)


# class MyTree(RenderTree):
#     def __init__(self, root):
#         self.root = root
#         root.parent.parent = root
#         # man yek tree rishe dar ham dashte basham bayad betoonam jaye rishe ro avaz konam. yani har nodi bayad betoone dobare rishe beshe. man entekhab mikonam migam masalan node 4 beshe rishe. 4 ye pedar dare ghablan. khob alan pedaresh bayad beshe bachash bad az inke man 4 o rishe kardam. chon rishe pedar nadare. ine ke migam pedare pedare 4 bayad beshe 4. 

#     class MyNode(Node):  # Add Node feature
#         def __init__(self, name, x, y, length=0, parent=None, children=None):
#            super(MyNode, self).__init__() #! super(MyNode)
#            self.name = name
#            self.length = length
#            self.x = x
#            self.y = y
#            self.parent = parent
#            if children:
#               self.children = children

#     def fill_length(self):
#         self.root.length = 0
#         self.fill_length_inside(self.root)

#     def fill_length_inside(self, node):
#         for n in node.children:
#             k = math.sqrt(math.pow(n.x-node.x,2) + math.pow(n.y-node.y,2))+ node.length
#             n.length = k
#             self.fill_length_inside(n)


from neurom.io import swc
import napari
data = swc.read('data1.swc')
print(data.neurite_root_section_ids())
# napari.view_shapes([data.data_block[:, :3]], shape_type='path', edge_color='red', ndisplay=3)
