#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 20:49:52 2019

@author: aysun
"""

import multiprocessing as mp
from random import randint
from functools import partial



def get_binary_random(node):
    return (node,bool(randint(0,1)))


def switch_flag(node,flags):
    """
    1) If it is false, we are not changing the node. 
    2) If the given node and any of its neighbors are true, 
    then we switch the node to false. 
    3) If all its neigbors are false, and then the node is true, it remains true.
    
    """
    def get_flag(x):
        return flags[x][1]
    #1
    if not flags[node][1]:
        return (node,False)
    #2,3
    Ngh = map(get_flag,graph.get(node,[]))
    return (node,not(any(Ngh)))
    
def first_element(x):
    return x[0]

def second_element(x):
    return x[1]

def independet_set(nodes,graph,pool):
    """
  I am assiging random true or false to each node. In order to do this, we use pool.map which
    will lock the main program until all processes are finished.  
    flags is a list of pairs including the nodes and its assigend true/flase
    """
    flags = pool.map(get_binary_random, nodes)
    #now we apply the switch_flag function to all nodes in parallel using pool.map.
    flags = pool.map(partial( partial(switch_flag, flags = flags), flags = flags),nodes)
    #filter nodes and only keep nodes which are true
    flags_independent = filter(second_element,flags)
    
    ind = pool.map(first_element,flags_independent)
    return ind

    


if __name__ == "__main__":
    #we defined a graph and a list of its nodes
    nodes = range(0,10)
    graph = {n:  [n+1] for n in nodes[:-1]}
   # graph = {n:  np.random.randint(0,10,3) for n in nodes}
   
    #for implementing parallel processing, I am using Python's pool class from multiprocessing module. 
    #Here, we will set the number of processes to 4, which means that the Pool class will only allow 4 processes running at the same time.
    pool = mp.Pool(processes=4)
    selected = independet_set(nodes,graph,pool)
    for n in nodes:
        print(n,list(graph.get(n,[])))
    print('--------')
    print('independet_set')
    print(selected)

