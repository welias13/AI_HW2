import ways.tools as tools
import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
import ways
import operator
import math
import heapq
import sys

#func that iterates over parent feild in each node to recover the path from node to None which is start node
def calculate_path(parents_dict,node):
    if node not in parents_dict:
        return []
    link_list = [node]
    curr_node = node
    #iterate over the parent
    while curr_node in parents_dict and parents_dict[curr_node][0] is not None:
        link_list.append(parents_dict[curr_node][0])
        curr_node = parents_dict[curr_node][0]
    link_list.reverse()
    return link_list


#func that runs normal ucs from start index to goals indexes list
# @tools.timed
def normal_ucs(Roads, start, goals, m, cost_func = lambda x : x.distance):
    #M*N' targets we need to get their paths starting from 'start'
    mNtag = math.ceil(m*(len(goals)))
    #open nodes heap that stores nodes by minimal cost to get from source to them
    open_heap = [(0,start)]
    #open set to used to check which nodes in heap
    open_set = set([start])
    #visited set to check which node we did visist
    visited = set([start])
    remaining_goals = set(goals)
    reached_goals = 0
    target_neighbours = []
    developed_nodes = set([])
    parents_dict = {start: (None,0)}
    #keep evaluating as long as heap is not empty
    while open_heap:
        node = heapq.heappop(open_heap)
        cost = node[0]
        open_set.discard(node[1])
        #check if current node is one of goals
        if node[1] in remaining_goals:
            remaining_goals.discard(node[1])
            reached_goals += 1
            # check we got paths for all our targers= M*N' then stop
            if reached_goals >= mNtag:
                break
            else:
                continue
		#node expansion
        if node[1] in developed_nodes:
            continue
        developed_nodes.add(node[1])
        for i in Roads[node[1]].links:
            total_cost = cost + cost_func(i)
            #check if node heap
            if i.target not in open_set:
                #check if node is already visited
                if i.target in visited:
                    #update cost if new cost is lower
                    if total_cost < parents_dict[i.target][1]:
                        open_set.add(i.target)
                        heapq.heappush(open_heap,(total_cost,i.target))
                        parents_dict[i.target] = (node[1], total_cost)
                else:
                    open_set.add(i.target)
                    visited.add(i.target)
                    heapq.heappush(open_heap, (total_cost, i.target))
                    parents_dict[i.target] = (node[1], total_cost)
            else:
                if total_cost < parents_dict[i.target][1]:
                    parents_dict[i.target] = (node[1], total_cost)
                    open_set.add(i.target)
                    heapq.heappush(open_heap, (total_cost, i.target))
    #for each v in goals calculate the path from stored parent
    for v in goals:
        v_path = calculate_path(parents_dict,v)
        if v_path:
            target_neighbours.append((v, parents_dict[v][1], v_path))
    #return ((v, parents_dict[v][1], v_path)) list where its parent,cost,path
    return (target_neighbours,len(developed_nodes))



#minimal ucs used to search for the shortest minimal path from star to goal,other than that is normal ucs
# @tools.timed
def minimal_ucs(Roads, start, goals, m, cond = lambda i : False):
    open_dict = {start:0}
    open_set = set([start])
    visited = set([start])
    target_neighbours = []
    parents_dict = {start: (None,0)}
    while open_dict and not cond(open_dict):
        node = min(open_dict, key=open_dict.get)
        cost = open_dict[node]
        del open_dict[node]
        open_set.discard(node)
        for i in Roads[node].links:
            total_cost = cost + i.distance
            if i.target not in open_set:
                if i.target in visited:
                    if total_cost >= parents_dict[i.target][1]:
                        continue
                    elif total_cost == parents_dict[i.target][1]:
                        target_path = len(calculate_path(parents_dict, i.target))
                        new_path = len(calculate_path(parents_dict, i.source)) + 1
                        #check if the new path of same cost is shortest and then update accordingly
                        if new_path < target_path:
                            parents_dict[i.target] = (i.source, parents_dict[i.target][1])
                    else:
                        open_set.add(i.target)
                        open_dict[i.target] = total_cost
                        parents_dict[i.target] = (node, total_cost)
                else:
                    open_set.add(i.target)
                    visited.add(i.target)
                    open_dict[i.target] = total_cost
                    parents_dict[i.target] = (node, total_cost)
            else:
                if total_cost < parents_dict[i.target][1]:
                    parents_dict[i.target] = (node, total_cost)
                    open_set.add(i.target)
                    open_dict[i.target] = total_cost
                elif total_cost == parents_dict[i.target][1]:
                    target_path = len(calculate_path(parents_dict, i.target))
                    new_path = len(calculate_path(parents_dict, i.source)) + 1
                    if new_path < target_path:
                        parents_dict[i.target] = (i.source, parents_dict[i.target][1])
    for v in goals:
        v_path = calculate_path(parents_dict,v)
        if v_path:
            target_neighbours.append((v, parents_dict[v][1], v_path))
    sorted_nodes = sorted(target_neighbours, key=operator.itemgetter(1))
    return sorted_nodes[0:math.floor((len(goals)+1)*m)]




if __name__ == "__main__":
    logging.info("Main start")
    Roads = ways.graph.load_map_from_csv("tlv.csv")
    print(normal_ucs(Roads, 65159, [61505], 1))
    logging.info("Done")

