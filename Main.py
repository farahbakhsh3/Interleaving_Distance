from anytree import Node, RenderTree, NodeMixin
import math

udo = Node("Udo")
marc = Node("Marc", parent=udo)
lian = Node("Lian", parent=marc)
dan = Node("Dan", parent=udo)
jet = Node("Jet", parent=dan)
jan = Node("Jan", parent=dan)
joe = Node("Joe", parent=dan)
us = Node("Us")

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


from anytree import Node, RenderTree, NodeMixin, PreOrderIter
import math
from anytree.search import find
from anytree.exporter import DotExporter
import pandas as pd
from tqdm import tqdm
from neurom.io import swc


class Tree():  # Just an example of a base class

    def make_tree(self, csv_file):
        df = pd.read_csv(csv_file)
        self.nodes_count = len(df.index)

        with tqdm(total=len(df.index)) as pbar:
            for node_no, x, y, parent in zip(df['Node_No'], df['X'], df['Y'], df['Parent_No']):
                if parent == -1:
                    root = MyNode2(node_no, x, y, parent=None, distance=0)
                else:
                    parent = find(root, lambda node: node.name == parent)
                    parent_x = parent.x
                    parent_y = parent.y
                    parent_distance = parent.distance

                    distance = parent_distance + math.sqrt(math.pow(x - parent_x, 2) +
                                                           math.pow(y - parent_y, 2))
                    x = MyNode2(node_no, x, y, parent=parent, distance=distance)
                pbar.update(1)
        self.root = root

    def simplify_tree(self):
        self.remove_single(self.root)

    def remove_single(self, node):
        print(len(node.children))
        if len(node.children) !=0:
            if len(node.children) == 1:
                if node !=None :
                    self.remove(node)

    def remove(self, node):
        node.parent.children = node.children
        node.parent = None 
        node.children = None 


class MyNode2(Tree, NodeMixin):
    def __init__(self, name, x, y, distance=None, parent=None, children=None):
        super(MyNode2, self).__init__()
        self.name = name
        self.x = x
        self.y = y
        self.distance = distance
        self.parent = parent
        if children:
            self.children = children

tree1= Tree()
tree1.make_tree('test.csv')

tree1.simplify_tree()
DotExporter(tree1.root).to_picture("tree2_root.png")