import ways.tools as tools
import math
import heapq
from ucs import calculate_path
import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


@tools.timed
def astar(Roads, start, goal, h_func, m=1, cost_func=lambda x: x.distance):
    # open nodes heap that stores nodes by minimal cost to get from source to them
    open_heap = [(h_func(Roads[start]), start)]
    # open set to used to check which nodes in heap
    open_set = set([start])
    # visited set to check which node we did visit
    visited = set([start])
    developed_nodes = 0
    developed_nodes_set = set([start])
    parents_dict = {start: (None, h_func(Roads[start]), 0)}
    # keep evaluating as long as heap is not empty
    while open_heap:
        node = heapq.heappop(open_heap)
        cost = node[0]  # f cost
        if node[1] not in open_set:
            continue
        open_set.discard(node[1])
        # check if current node is one of goals
        if node[1] == goal:
            #  check we got paths for all our targets= M*N' then stop
            break
        # node expansion
        developed_nodes += 1
        for i in Roads[node[1]].links:
            g_total_cost = parents_dict[node[1]][2] + cost_func(i)
            total_cost = g_total_cost + h_func(Roads[i.target])
            # check if node heap
            if i.target not in open_set:
                # check if node is already visited
                if i.target in visited:
                    # update cost if new cost is lower
                    if total_cost < parents_dict[i.target][1]:
                        open_set.add(i.target)
                        heapq.heappush(open_heap, (total_cost, i.target))
                        parents_dict[i.target] = (node[1], total_cost, g_total_cost)
                else:
                    open_set.add(i.target)
                    visited.add(i.target)
                    heapq.heappush(open_heap, (total_cost, i.target))
                    parents_dict[i.target] = (node[1], total_cost, g_total_cost)
            else:
                if total_cost < parents_dict[i.target][1]:
                    parents_dict[i.target] = (node[1], total_cost, g_total_cost)
                    open_set.add(i.target)
                    heapq.heappush(open_heap, (total_cost, i.target))
    # for each v in goals calculate the path from stored parent
    goal_path = calculate_path(parents_dict, goal)
    # return goal_path, parents_dict[goal][1], developed_nodes list where its parent,cost,path
    return goal_path, parents_dict[goal][1], developed_nodes
