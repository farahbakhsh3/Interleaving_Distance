
from anytree import Node, RenderTree, NodeMixin, PreOrderIter
import math
from anytree.search import find
from anytree.exporter import DotExporter
import pandas as pd
from tqdm import tqdm


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
                    distance = parent_distance - math.sqrt(math.pow(x - parent_x, 2) +
                                                           math.pow(y - parent_y, 2))
                    x = MyNode2(node_no, x, y, parent=parent, distance=distance)
                pbar.update(1)
        self.root = root

    def simplify_tree(self):
        self.remove_single(self.root.children[0])
        
    def remove_single(self, node):
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
        list_of_functions2 = []
        
        list_of_function1 = []
        for pre, fill, node in RenderTree(self.root):
            list_of_function1.append((node.distance))
        for pre, fill, node in RenderTree(tree2.root):
            list_of_function1.append((node.distance)+epsilon)
        list_of_function1.sort(reverse=True) # from bigest(0) to smalest
        print(list_of_function1)
        for d in list_of_function1:
            if d not in list_of_functions1:
                list_of_functions1.append(d)
        list_of_function2 = []
        for pre, fill, node in RenderTree(tree2.root):
            list_of_function2.append((node.distance))
        for pre, fill, node in RenderTree(self.root):
            list_of_function2.append((node.distance)-epsilon)
        list_of_function2.sort(reverse=True) # from bigest(0) to smalest

        for d in list_of_function2:
            if d not in list_of_functions2:
                list_of_functions2.append(d)
        nodes=[]
        nodes2=[]
        nodes = list(self.root.children) 
        l = Mylist(list_of_functions1) 
        while nodes:
            n = nodes[0]
            li = l.numbers_bet_two_distance(n.distance, n.parent.distance)
            print(len(li))
            if len(li)>0:
                n.make_long(li)
            nodes.remove(n)
            for node in n.children:
                nodes.append(node)
        
        nodes2 = list(tree2.root.children) 
        l2 = Mylist(list_of_functions2) 
        while nodes2:
            n = nodes2[0]
            li2 = l2.numbers_bet_two_distance(n.distance, n.parent.distance)
            if len(li2)>0:
                n.make_long(li2)
            nodes2.remove(n)
            for node in n.children:
                nodes2.append(node)
                
        return list_of_functions1
    
      
    def interleaving_distance(self, tree2, epsilon):
        
        nodelisttree1 = []
        nodelisttree2 = []
        list_of_functions1 = self.augmented_tree(tree2, epsilon)
        
             

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
        if len(list_of_distance) > 0:
            d = list_of_distance[0]
            list_of_distance.remove(d)
            name = round(self.name + 0.0001,5)
            n = self.add_child(name, d)  # Mynode2(d) just d is important 
            n.make_long(list_of_distance)
            
        
    def add_child(self, name, d): #we want to add node between self and its parent 
        sf = self.parent 
        l = list(sf.children)
        l.remove(self)
        n = MyNode2(name,0,0,d, sf,[self])
        l.append(n)
        sf.children = tuple(l)
        self.parent = n
        return n
        
        
    def remove_children(self, node): #
        cl = list(self.children)
        cl.remove(node)
        cl.append(node.children[0])
        self.children = tuple(cl)   
        
        
class Mylist(list):
    
    def numbers_bet_two_distance(self,a,b):  
        l = []
#        self.sort() # list is sorted from big to smal
        for d in self:
            if a<d<b :
                l.append(d)
        return l
    
#    def unique(self):
#        x = Mylist()
#        for d in self:
#            if d not in x:
#                x.append(d)
#        return x
            
    
    
tree1= Tree()
tree1.make_tree('test.csv')
#
tree1.simplify_tree()
DotExporter(tree1.root).to_picture("tree1_root.png")


tree2= Tree()
tree2.make_tree('test2.csv')
#
tree2.simplify_tree()
DotExporter(tree2.root).to_picture("tree2_root.png")

tree2.interleaving_distance(tree1,1)
DotExporter(tree2.root).to_picture("tree2_root_aug.png")
DotExporter(tree1.root).to_picture("tree1_root_aug.png")
