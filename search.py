from _treelib import *
from queue import PriorityQueue
import time

# BFS but orders by how close the goal is as well, 
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
#   - faster but doesn't give optimal solutions
def a_star_search(s_0, show=False):
    strt = time.time()
    q = PriorityQueue()
    v = (0, s_0)
    S = {s_0.id: s_0.f}
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


# using the heuristic search, this takes 52 secs
# using BFS this doesn't rly finish
n = 16
s_0 = state({i:0 for i in range(1,n+1)}, 
            {0:n+1, 1:-1, 2:-1},
            {0:1, 1:-1, 2:-1},
            None)

path = a_star_search(s_0)
