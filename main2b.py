'''
Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
'''

#do NOT import ways. This should be done from other files
#simply import your modules and call the appropriate functions
from sympy.functions.elementary.trigonometric import cos

from astar import astar
import ways.graph as graph
import ways.tools as tools
import sys
import ways
import ucs
from cost import time_cost_func
import ways.info as info

max_speed = max([j[1] for j in info.SPEED_RANGES])

def time_h_func_aux(junc1,junc2):
    return tools.compute_distance(junc1.lat, junc1.lon, junc2.lat, junc2.lon)/max_speed

def uc_time(source, target):
    Roads = ways.graph.load_map_from_csv()
    (ucs_path, num_developed_nodes) = ucs.normal_ucs(Roads, source, [target], 1,cost_func=time_cost_func)
    ucs_path = ucs_path[0]
    return ucs_path[2]

    
def a_star_time(source, target):
    Roads = graph.load_map_from_csv()
    print("max speed = " + str(max_speed))
    result = astar(Roads, source, target, h_func=lambda junc: time_h_func_aux(junc, Roads[target]), cost_func=time_cost_func)
    return result[0]

def uc_time_exp(Roads,source, target):
    (ucs_path, num_developed_nodes) = ucs.normal_ucs(Roads, source, [target], 1,cost_func=time_cost_func)
    ucs_path = ucs_path[0]
    return (num_developed_nodes, ucs_path[1])

def a_star_time_exp(Roads,source, target):
    result = astar(Roads, source, target, h_func=lambda junc: time_h_func_aux(junc, Roads[target]), cost_func=time_cost_func)
    return result[2], result[1]

def dispatch(argv):
    from sys import argv
    source, target = int(argv[2]), int(argv[3])
    if argv[1] == 'uc_time':
        path = uc_time(source, target)
    elif argv[1] == 'a_star_time':
        path = a_star_time(source, target)
    print(' '.join(str(j) for j in path))


if __name__ == '__main__':
    from sys import argv
    dispatch(argv)
