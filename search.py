from _treelib import *
from queue import PriorityQueue
import time

# Implementation of Breadth First Search, just searches using path cost
# Very bad, but just good for comparison
# ? Results of n=12:
# ? Path Length:     8191
# ? Nodes Expanded:  1594323
# ? Time Taken:      31.033885955810547
def BFS(s_0, show=False):
    strt = time.time()
    q = PriorityQueue()
    v = (0, s_0)
    S = {s_0.id: s_0.g}
    q.put(v)
    while not v[1].goal_check():
        v = q.get()
        for u in v[1].expand():
            if not u.id in S.keys():
                q.put((u.g, u))
                S[u.id] = True
    v = v[1]
    path = [v]
    while v.p:
        v = v.p
        path.append(v)
    path.append(s_0)
    path.reverse()
    path = path[1:]
    print('Path Length:     ' + str(len(path)-1) + '\n' + \
          'Nodes Expanded:  ' + str(len(S)) + '\n' + \
          'Time Taken:      ' + str(time.time()-strt))
    if show:
        [print(s) for s in path]
    return path

# uses a heuristic to guide the search,
#   - good compromise
# ? Results of n=14:
# ? Path Length:     29059
# ? Nodes Expanded:  2238032
# ? Time Taken:      39.604840993881226
def a_star_search(s_0, show=False):
    strt = time.time()
    q = PriorityQueue()
    v = (0, s_0)
    S = {s_0.id: True}
    q.put(v)
    while not v[1].goal_check():
        v = q.get()
        for u in v[1].expand():
            if not u.id in S.keys():
                q.put((u.f, u))
                S[u.id] = True
    v = v[1]
    path = [v]
    while v.p:
        v = v.p
        path.append(v)
    path.append(s_0)
    path.reverse()
    path = path[1:]
    print('Path Length:     ' + str(len(path)-1) + '\n' + \
          'Nodes Expanded:  ' + str(len(S)) + '\n' + \
          'Time Taken:      ' + str(time.time()-strt))
    if show:
        [print(s) for s in path]
    return path

# Implementation of greedy Best-First Search. 
# Actually quite fast, takes the same amount of time 
# as A* but produces worse paths
# ? Results of n=14:
# ? Path Length:     48137
# ? Nodes Expanded:  2234153
# ? Time Taken:      39.61396527290344
def greedy_BFS(s_0, show=False):
    strt = time.time()
    q = PriorityQueue()
    v = (0, s_0)
    S = {s_0.id: s_0.h()}
    q.put(v)
    while not v[1].goal_check():
        v = q.get()
        for u in v[1].expand():
            if not u.id in S.keys():
                q.put((u.h(), u))
                S[u.id] = True
    v = v[1]
    path = [v]
    while v.p:
        v = v.p
        path.append(v)
    path.append(s_0)
    path.reverse()
    path = path[1:]
    print('Path Length:     ' + str(len(path)-1) + '\n' + \
          'Nodes Expanded:  ' + str(len(S)) + '\n' + \
          'Time Taken:      ' + str(time.time()-strt))
    if show:
        [print(s) for s in path]
    return path


n = 15
s_0 = state({i:0 for i in range(1,n+1)}, 
            {0:n+1, 1:-1, 2:-1},
            {0:1, 1:-1, 2:-1},
            None)

path = a_star_search(s_0)
