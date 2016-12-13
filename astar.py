import ways.tools as tools
import math
import heapq
from ucs import calculate_path
import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


#@tools.timed
def astar(Roads, start, goal, h_func, m=1, cost_func=lambda x: x.distance):
    # open nodes heap that stores nodes by minimal f_cost
    open_heap = [(h_func(Roads[start]), start)]
    # open set to used to check which nodes is open
    open_set = set([start])
    # visited set to check which node we did visit before
    visited = set([start])
    # number of nodes developed
    developed_nodes = 0
    # keeps all result information for each visited node
    parents_dict = {start: (None, h_func(Roads[start]), 0)}
    # keep evaluating as long as heap is not empty
    while open_heap:
        # pop minimal f_cost node
        node = heapq.heappop(open_heap)
        # checks if node is in open group. if we reach a node from more that one path, we add it again to the heap.
        # first time we take it out of the heap it shouldn't be in the open group, so we discard it from the set.
        if node[1] not in open_set:
            continue
        open_set.discard(node[1])
        # check if current node is the goal
        if node[1] == goal:
            #  Goal reached at it's minimal cost
            break
        # developing a node, add it to the developed nodes counter
        developed_nodes += 1
        # node expansion
        for i in Roads[node[1]].links:
            # new g_cost of the for the current son
            g_total_cost = parents_dict[node[1]][2] + cost_func(i)
            # f_cost for this son
            total_cost = g_total_cost + h_func(Roads[i.target])
            # check if node is in the open group
            if i.target not in open_set:
                # check if node is already visited
                if i.target in visited:
                    # update cost if new cost is lower and insert again to the heap and the open set.
                    if total_cost < parents_dict[i.target][1]:
                        open_set.add(i.target)
                        heapq.heappush(open_heap, (total_cost, i.target))
                        parents_dict[i.target] = (node[1], total_cost, g_total_cost)
                else:
                    # first time visiting this node, insert a new instance to the heap, the open set and the paretn dict.
                    open_set.add(i.target)
                    visited.add(i.target)
                    heapq.heappush(open_heap, (total_cost, i.target))
                    parents_dict[i.target] = (node[1], total_cost, g_total_cost)
            else:
                # already in teh open set
                if total_cost < parents_dict[i.target][1]:
                    # better path, update all information, and insert again to the heap.
                    parents_dict[i.target] = (node[1], total_cost, g_total_cost)
                    open_set.add(i.target)
                    heapq.heappush(open_heap, (total_cost, i.target))
    # for the goal node calculate the path from stored parent (same function we used in ucs)
    goal_path = calculate_path(parents_dict, goal)
    # return goal_path, parents_dict[goal][1], developed_nodes list where its path, cost, number of developed nodes.
    return goal_path, parents_dict[goal][1], developed_nodes
