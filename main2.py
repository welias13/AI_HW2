'''
Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
'''

# do NOT import ways. This should be done from other files
# simply import your modules and call the appropriate functions

from astar import astar
import ways.graph as graph
import ways.tools as tools
import sys


def ex_h_func(junc):
    h_dict = {1: 9, 2: 10, 3: 11, 4: 15, 5: 1, 6: 2, 7: 5, 8: 0}
    return h_dict[junc.index]


def h_func_aux(junc1, junc2):
    return tools.compute_distance(junc1.lat, junc1.lon, junc2.lat, junc2.lon)


def a_star(source, target):
    Roads = graph.load_map_from_csv()
    result = astar(Roads, source, target, h_func=lambda junc: h_func_aux(junc, Roads[target]))
    return result[0]


def a_star_exp(Roads, source, target):
    result = astar(Roads, source, target, h_func=lambda junc: h_func_aux(junc, Roads[target]))
    return result[2], result[1]


#####################################################################################################
#####################################################################################################
#####################################################################################################
#####################################################################################################
def a_star_exp3(source, target, abstractMap):
    Roads = graph.load_map_from_csv()
    return a_star_exp3_aux(Roads, source, target, abstractMap)


@tools.timed
def a_star_exp3_aux(Roads, source, target, abstractMap, experiment=False):
    develped_a = 0
    develped_b = 0
    develped_c = 0
    cost = 0
    'call function to find path using better ways algorithm, and return list of indices'
    if not abstractMap:
        raise NotImplementedError  # You should load the map you were asked to pickle
        # Note: pickle might give you an error for the namedtuples, even if they
        # are imported indirectly from ways.graph. You might need to declare, for
        # example: Link = ways.graph.Link
    Roads = graph.load_map_from_csv()
    final_list = []
    try:
        # phase a
        # find the closet abstract space node to A by air distance
        junc1_index = -1
        junc1_min_distance = sys.maxsize
        # iterate over all possible nodes
        for center in list(abstractMap.keys()):
            # compute the distance using provided func
            current_distance = tools.compute_distance(Roads[center].lat, Roads[center].lon, Roads[source].lat,
                                                      Roads[source].lon)
            # update if new node is closer to B
            if current_distance < junc1_min_distance:
                junc1_index = center
                junc1_min_distance = current_distance
        # run ucs from junc2 to B to get the path
        (a_star_path, a_cost, develped_a) = astar(Roads, source, junc1_index,
                                                  h_func=lambda junc: h_func_aux(junc, Roads[junc1_index]))
        cost += a_cost
        if a_star_path:
            junc1_path = a_star_path
        # if this phace failed run normal ucs from A to B by throwing exception that is dealt after
        else:
            raise Exception("Phase a failed")
        # phase b
        # find the closet abstract space node to B by air distance
        junc2_index = -1
        junc2_min_distance = sys.maxsize
        # iterate over all possible nodes
        for center in list(abstractMap.keys()):
            # compute the distance using provided func
            current_distance = tools.compute_distance(Roads[center].lat, Roads[center].lon, Roads[target].lat,
                                                      Roads[target].lon)
            # update if new node is closer to B
            if current_distance < junc2_min_distance:
                junc2_index = center
                junc2_min_distance = current_distance
        # run ucs from junc2 to B to get the path
        (a_star_path, b_cost, develped_b) = astar(Roads, junc2_index, target,
                                                  h_func=lambda junc: h_func_aux(junc, Roads[target]))
        cost += b_cost
        if a_star_path:
            junc2_path = a_star_path
        # if this phace failed run normal ucs from A to B by throwing exception that is dealt after
        else:
            raise Exception("Phase b failed")

        # phase c
        # run ucs from junc1 to junc2 in normal search space
        (a_star_path, c_cost, develped_c) = astar(abstractMap, junc1_index, junc2_index,
                                                  h_func=lambda junc: h_func_aux(junc, Roads[junc2_index]),
                                                  cost_func=lambda x: x.cost)
        cost += c_cost
        if a_star_path:
            # path for j1 to j2
            abstract_index_list = a_star_path
            if junc1_index == junc2_index:
                junc_1_2_path = [junc1_index]
            else:
                expanded_list = []
                for i in range(1, len(abstract_index_list)):
                    # should return single value
                    # get the the links list which ucs returned
                    abstact_link_list = [lnk.path for lnk in abstractMap[abstract_index_list[i - 1]].links if
                                         lnk.target == abstract_index_list[i]]
                    abstact_link_list = abstact_link_list[0]
                    # extracth the path from junc1 to junc2 from the link
                    expanded_list = expanded_list + abstact_link_list[1:len(abstact_link_list)]
                junc_1_2_path = expanded_list
        # if this phace failed run normal ucs from A to B by throwing exception that is dealt after
        else:
            raise Exception("Phase c failed")
        # append all three paths from phases a,b,c respectively
        if experiment:
            return (develped_a + develped_b + develped_c, cost)
        else:
            return junc1_path + junc_1_2_path + junc2_path[1:len(junc2_path)]
    # exception is caught therefor we need to run norma ucs from A to B
    except:
        print('astar failed!!')
        (a_star_path, cost, fail_num_dev) = astar(Roads, source, target,
                                                  h_func=lambda junc: h_func_aux(junc, Roads[target]))
        if experiment:
            return (develped_a + develped_b + develped_c + fail_num_dev, cost)
        else:
            return a_star_path


def dispatch(argv):
    from sys import argv
    source, target = int(argv[2]), int(argv[3])
    if argv[1] == 'a_star':
        path = a_star(source, target)
    if argv[1] == 'a_star_exp3':
        import pickle as pkl
        abstractMap = pkl.load(open(argv[4], 'rb'))
        path = a_star_exp3(source, target, abstractMap)
    print(' '.join(str(j) for j in path))


if __name__ == '__main__':
    from sys import argv

    dispatch(argv)
