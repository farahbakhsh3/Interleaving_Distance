from anytree import Node, RenderTree, NodeMixin
import math

udo = Node("Udo")
marc = Node("Marc", parent=udo)
lian = Node("Lian", parent=marc)
dan = Node("Dan", parent=udo)
jet = Node("Jet", parent=dan)
jan = Node("Jan", parent=dan)
joe = Node("Joe", parent=dan)
#Node("Joe", parent=marc)
dan.children = [jet, jan]
type(dan.children)
us = Node("Us")

print(udo)
# Node('/Udo')
#print(joe)
# Node('/Udo/Dan/Joe')
#def add_children(father, node): #we want to add node to the children of self
#    father.children = father.children + tuple(node)

for pre, fill, node in RenderTree(udo):
    print("%s%s" % (pre, node.name))
# Udo
# ├── Marc
# │   └── Lian
# └── Dan
#     ├── Jet
#     ├── Jan
#     └── Joe

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
        self.remove_single(self.root.children[0])
        
    def remove_single(self, node):
#        print(len(node.children))
        if node.parent != None:
            if len(node.children) == 1:
                x = node.parent 
                node.parent.remove_children(node)
                for n in x.children:
                    self.remove_single(n)
            else:
               for n in node.children:
                   self.remove_single(n)
        else:
            for n in node.children:
                self.remove_single(n)               


    def augmented_tree(self, tree2, epsilon):
        list_of_functions1 = []
        for pre, fill, node in RenderTree(self.root):
            list_of_functions1.append(-(node.distance))
        for pre, fill, node in RenderTree(tree2.root):
            list_of_functions1.append(-(node.distance)-epsilon)
        list_of_functions1.sort(reverse=True) # from bigest(0) to smalest
         
        list_of_functions2 = []
        for pre, fill, node in RenderTree(tree2.root):
            list_of_functions2.append(-(node.distance))
        for pre, fill, node in RenderTree(self.root):
            list_of_functions2.append(-(node.distance)+epsilon)
        list_of_functions2.sort(reverse=True) # from bigest(0) to smalest
        
        nodes = list(self.root.children) 
        l = Mylist(list_of_functions1) 
        for n in nodes:
            li = l.numbers_bet_two_distance(n.distance, n.parent.distance)
            if len(li)>0:
                n.make_long(li)
            nodes.remove(n)
            for node in n.children:
                nodes.add(node)
        
        nodes2 = list(tree2.root.children) 
        l2 = Mylist(list_of_functions2) 
        for n in nodes2:
            li2 = l2.numbers_bet_two_distance(n.distance, n.parent.distance)
            if len(li2)>0:
                n.make_long(li2)
            nodes2.remove(n)
            for node in n.children:
                nodes2.add(node)
                

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
            
    def make_long(self,list_of_distance):
#        list_of_distance.sort() # sort from smallest to bigest we think it has been sorted
        for d in list_of_distance:
            list_of_distance.remove(d)
            self.add_child(Mynode2(d))  # Mynode2(d) just d is important 
            self.make_long(Mynode2(d), list_of_distance)
            
        
    def add_child(self, node): #we want to add node between self and its parent 
        sf = self.parent 
        cl = list(sf.children)
        cl.append(node)
        cl.remove(self)
        sf.children = tuple(cl)

    def remove_children(self, node): #we want to add node to the children of self
        cl = list(self.children)
        cl.remove(node)
        cl.append(node.children[0])
        self.children = tuple(cl)   
        
        
class Mylist(list):
    
    def numbers_bet_two_distance(self,a,b):  
        l = []
        self.sort() # list is sorted from big to smal
        for d in self:
            if a<d<b :
                l.append(d)
        return l
            
#tree1= Tree()
#tree1.make_tree('test.csv')
#
#tree1.simplify_tree()
#DotExporter(tree1.root).to_picture("tree2_root.png")


