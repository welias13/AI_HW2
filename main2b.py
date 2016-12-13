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
from cost import expected_time
import ways.info as info

# max speed allowed in the map
max_speed = max([j[1] for j in info.SPEED_RANGES])

# aux function for the heuristic time based function. return the Eucliduos distance divided by the max speed.
def time_h_func_aux(junc1,junc2):
    return tools.compute_distance(junc1.lat, junc1.lon, junc2.lat, junc2.lon)/max_speed

# perform uniform cost with "expected time" function as the g_cost function
def uc_time(source, target):
    Roads = ways.graph.load_map_from_csv()
    (ucs_path, num_developed_nodes) = ucs.normal_ucs(Roads, source, [target], 1, cost_func=expected_time)
    ucs_path = ucs_path[0]
    return ucs_path[2]

# perform A* with "expected time" function as the g_cost function and time_h_func as heuristic cost
def a_star_time(source, target):
    Roads = graph.load_map_from_csv()
    result = astar(Roads, source, target, h_func=lambda junc: time_h_func_aux(junc, Roads[target]), cost_func=expected_time)
    return result[0]

# same as uc_time, but return relevant information for the experiment.
def uc_time_exp(Roads,source, target):
    (ucs_path, num_developed_nodes) = ucs.normal_ucs(Roads, source, [target], 1, cost_func=expected_time)
    ucs_path = ucs_path[0]
    return (num_developed_nodes, ucs_path[1])

# same as a_star_time, but return relevant information for the experiment.
def a_star_time_exp(Roads,source, target):
    result = astar(Roads, source, target, h_func=lambda junc: time_h_func_aux(junc, Roads[target]), cost_func=expected_time)
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
