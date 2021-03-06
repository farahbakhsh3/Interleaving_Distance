
from anytree import Node, RenderTree, NodeMixin, PreOrderIter
import math
from anytree.search import find
from anytree.exporter import DotExporter
import pandas as pd
from tqdm import tqdm


        

        
class Mylist(list):
    
    def numbers_bet_two_distance(self,a,b):  
        l = []
#        self.sort() # list is sorted from big to smal
        for d in self:
            if a<d<b :
                l.append(d)
        return l
    
    def nearest_lower(self, d):
        i = 0
        while d < self[i]:
                i = i+1
        return self[i]   
            
#    def unique(self):
#        x = Mylist()
#        for d in self:
#            if d not in x:
#                x.append(d)
#        return x

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
        self.list_of_function1 = []

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
        
        for pre, fill, node in RenderTree(self.root):
            if node.distance not in list_of_functions1:
                list_of_functions1.append((node.distance))
                self.list_of_function1.append(node.distance)
        for pre, fill, node in RenderTree(tree2.root):
            if node.distance not in list_of_functions1:
                list_of_functions1.append((node.distance)-epsilon)
                self.list_of_function1.append((node.distance)-epsilon)
        self.list_of_function1.sort(reverse=True) # from bigest(0) to smalest
        list_of_functions1.sort(reverse=True)
        
        nodes=[]
        nodes2=[]
        nodes = list(self.root.children) 
        l = Mylist(self.list_of_function1) 
        while nodes:
            n = nodes[0]
            li = l.numbers_bet_two_distance(n.distance, n.parent.distance)
            if len(li)>0:
                n.make_long(li)
            nodes.remove(n)
            for node in n.children:
                nodes.append(node)
        
        nodes2 = list(tree2.root.children) 
        l2 = Mylist(list_of_functions1) 
        while nodes2:
            n = nodes2[0]
            li2 = l2.numbers_bet_two_distance(n.distance, n.parent.distance)
            if len(li2)>0:
                n.make_long(li2)
            nodes2.remove(n)
            for node in n.children:
                nodes2.append(node)
        
    
    def interleaving_distance(self, tree2, epsilon):
        dis = True 
        
        nodelisttree1 = []
        nodelisttree2 = []
        self.augmented_tree(tree2, epsilon)
        
#       first we put all the nodes in a list to be able to delet them easily and reduce the run time
        print("Augmented trees were made")
        
        for pre, fill, node in RenderTree(self.root):
            nodelisttree1.append(node)  
        for pre, fill, node in RenderTree(tree2.root):
            nodelisttree2.append(node) 
        
#       we copy list of function to be able to delete easily 
        list_of_function = self.list_of_function1.copy()
        list_of_function.sort()
        
        
#       first line
        List_gh = [] 
        List_nu = []
        
#        i = 1
#        while(len(List_gh)==0 and dis ==True and i<=4): # the goal of this while is to go to other lines easily if we have nothing yet to calculate when we start from bottom
#            i= i+1
#            nodelist1_new = []
#            nodelist2_new = []
#            d = list_of_function[0]
#            list_of_function.remove(d)
#            print(d)
#            print(nodelist1_new)
#            # remove nodes we consider in the first stage or line
#            for node in nodelisttree1: 
#                if node.distance == d:
#                    print(nodelist1_new)
#                    print(node.name, node.distance)
#                    nodelist1_new.append(node)
#                    nodelisttree1.remove(node)
#            for node in nodelisttree2: 
#                if node.distance == d + epsilon:
#                    nodelist2_new.append(node)
#                    nodelisttree2.remove(node)
#            print("node1")
#            for p in nodelist1_new:
#                print(p.name)
##           no of children of the first line
#            ch1= []
#            for n in nodelist1_new:
#                for ni in n.children:
#                    if ni not in ch1:
#                        ch1.append(ni)
##           no of children of the second line
#            ch2 = []
#            for n in nodelist2_new:
#                for ni in n.children:
#                    if ni not in ch2:
#                        ch2.append(ni)
#                  
#
#            if len(nodelist2_new)==0:
#                if len(nodelist1_new)!=0: # we do not need this if
#                    dis = False
#            else:
#                if len(nodelist1_new)!=0:
#                    vp=self.Valid_pair(nodelist1_new, nodelist2_new)
##                    print(vp)
#                    print("node1")
#                    for p in nodelist1_new:
#                        print(p.name)
#                    print("node2")
#                    for p in nodelist2_new:
#                        print(p.name)
#                print("=f")
#                    
#             
##        if dis == True:
##            if len(nodelist1_new)>0:
##                List_gh = self.Valid_pair(nodelist1_new, nodelist2_new)
##                print(List_gh)

                    
        return dis
    
    
#    else:
#                for n in nodelist2_new:
#                    if n.height() > 2*epsilon:
#                        dis = False
    
#       now we have a list of children of list1 and children of list2.
   
# should be gone to another page      
#   print(all_subset(2,[1,2,3]))   [[1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2], [3, 3]]
    def partition(self, integ, collection2):
        i = 0
        s_gh = []
        s_j=[]
        for j in collection2:
            s_j.append([j])
        for i in range(1, integ):
            s_gh = s_j.copy() 
            s_j.clear()
            for j in range(0,len(s_gh)):
                for s in collection2:
                    k = s_gh[j]+[s]
                    s_j.append(k)
        return s_j
       
        
#       for any list of nodes in tree1 and nodes in tree2 returns all the valid pairs
    def Valid_pair(self, list1, list2):
        l = [] # list of children of a node
        ret = []
        FList = [] # lists of fathers
        function = list1[0].distance
        eps = abs(function - list2[0].distance)
        for node in list1:
            NF= node.upper2eps(eps)
            if NF not in FList:
                FList.append(NF)
        
#       we earn a list of parent which is unique FList
        for node in FList: 
            l.clear()
            for n in node.findc(function):
                l.append(n)
                
#            print(l)   
            for pair in self.allpair(l,list2):
                ret.append(pair)   
        
            # we have a list of tau of children with same parent l
        return ret
        
                
#    for a given pair of lists gives all partition of list1 and list2
    def allpair(self, list1, list2):   
        L = []
        AS = self.all_subset(list1)
        for node2 in list2:
            for pair in AS:
                pair.append(node2)
                L.append(pair)
        return L
                
         
        
#     Was coppied from https://stackoverflow.com/questions/19368375/set-partitions-in-python
    def partition_help(self, collection):
        if len(collection) == 1:
            yield [ collection ]
            return
    
        first = collection[0]
        for smaller in self.partition_help(collection[1:]):
            # insert `first` in each of the subpartition's subsets
            for n, subset in enumerate(smaller):
                yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
            # put `first` in its own subset 
            yield [ [ first ] ] + smaller
#    L for [1,2,3]
# [[1, 2, 3], [1], [2, 3], [1, 2], [3], [2], [1, 3]]
    def all_subset (self, collection):
        L = []
        for s in self.partition_help(collection):
            for l in s:
                if l not in L:
                    L.append(l)
        return L
        
#    for a given d returns all the nodes with this distance or function       
    def allnode(self, d):
        nodes = []
        for pre, fill, node in RenderTree(self.root):
            if node.distance == d :
                nodes.append(node)
        return nodes    
            
            
        
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
     
#        finds the father which is in 2 eps higher 
    def upper2eps(self, eps):
        f = self.parent
        d = self.distance
        x = self
        while abs(f.distance - d) <= 2 * eps:
            x = f
            f = f.parent
        
        return x
    
        
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
        
    def height(self):
        dis = 100
        for pre, fill, node in RenderTree(self):
            if node.distance < dis:
                dis = node.distance
        return abs(self.distance-dis)





# for a given node it finds the children of the node which are 2epsilon lowerand their distances are f2eps
    def findc(self, f2eps):
        c = []
        for pre, fill, node in RenderTree(self):
            if node.distance == f2eps :
                if node not in c:
                    c.append(node)
                
        return c
            
            
    
if __name__ == "__main__":
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
    
    
    print("Simplified trees were made")
    
    print(tree1.interleaving_distance(tree2,1))
#    print(tree1.interleaving_distance(tree1,-11))
    DotExporter(tree2.root).to_picture("tree2_root_aug.png")
    DotExporter(tree1.root).to_picture("tree1_root_aug.png")
    
    