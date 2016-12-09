'''
Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
'''

#do NOT import ways. This should be done from other files
#simply import your modules and call the appropriate functions

import ways
import ucs
import ways.tools as tools
import sys

def tuple_list_to_index_list(tuple_list):
    if tuple_list[0][0] is not None:
        output_list = [tuple_list[0][0]]
    else:
        output_list = []
    for tup in tuple_list:
        output_list.append(tup[1])
    return output_list


#func that runs a normal ucs from source to target in normal search space and returns the path of indices in list
def base(source, target):
    'call function to find path using uniform cost, and return list of indices'
    Roads = ways.graph.load_map_from_csv("tlv.csv")
    (ucs_path,num_developed_nodes) = ucs.normal_ucs(Roads,source, [target],1)
    ucs_path = ucs_path[0]
    return ucs_path[2]


def base_exp(Roads,source, target):
    'call function to find path using uniform cost, and return list of indices'
    (ucs_path,num_developed_nodes) = ucs.normal_ucs(Roads,source, [target],1)
    ucs_path = ucs_path[0]
    return (num_developed_nodes,ucs_path[1])


def betterWaze_exp(Roads ,source, target, abstractMap=None):
    'call function to find path using better ways algorithm, and return list of indices'
    if not abstractMap:
        raise NotImplementedError  # You should load the map you were asked to pickle
        # Note: pickle might give you an error for the namedtuples, even if they
        # are imported indirectly from ways.graph. You might need to declare, for
        # example: Link = ways.graph.Link
    develped_a = 0
    develped_b = 0
    develped_c = 0
    cost = 0
    final_list = []
    try:
        # phase a
        (ucs_paths,develped_a) = ucs.normal_ucs(Roads, source, list(abstractMap.keys()), float(1)/len(abstractMap))
        if ucs_paths:
            ucs_path = ucs_paths[0]
            junc1_path = ucs_path[2]
            junc1_index = ucs_path[0]
            cost += ucs_path[1]
        else:
            raise Exception("Phase a failed")

        # phase b
        junc2_index = -1
        junc2_min_distance = sys.maxsize
        for center in list(abstractMap.keys()):
            current_distance = tools.compute_distance(Roads[center].lat, Roads[center].lon, Roads[target].lat,
                                                      Roads[target].lon)
            if current_distance < junc2_min_distance:
                junc2_index = center
                junc2_min_distance = current_distance
        (ucs_paths,develped_b) = ucs.normal_ucs(Roads, junc2_index, [target], 1)
        if ucs_paths:
            ucs_path = ucs_paths[0]
            junc2_path = ucs_path[2]
            cost += ucs_path[1]
        else:
            raise Exception("Phase b failed")

        # phase c
        (ucs_paths,develped_c) = ucs.normal_ucs(abstractMap, junc1_index, [junc2_index], 1, lambda x: x.cost)
        if ucs_paths:
            ucs_path = ucs_paths[0]
            abstract_index_list = ucs_path[2]
            cost += ucs_path[1]
            expanded_index_list = []
            if junc1_index == junc2_index:
                junc_1_2_path = [junc1_index]
            else:
                expanded_tuple_list = []
                for i in range(1, len(abstract_index_list)):
                    # should return single value
                    abstact_link_list = [lnk.path for lnk in abstractMap[abstract_index_list[i - 1]].links if
                                         lnk.target == abstract_index_list[i]]
                    abstact_link_list = abstact_link_list[0]
                    expanded_tuple_list = expanded_tuple_list + abstact_link_list[1:len(abstact_link_list)]
                junc_1_2_path = expanded_tuple_list
        else:
            raise Exception("Phase c failed")
        return (develped_a +develped_b + develped_c,cost)
    except:
        print("Exception")
        (develped_base,cost) = base_exp(Roads,source, target)
        return (develped_base + develped_a +develped_b + develped_c,cost)



    
def betterWaze(source, target,abstractMap=None):
    'call function to find path using better ways algorithm, and return list of indices'
    if not abstractMap:
        raise NotImplementedError # You should load the map you were asked to pickle
        # Note: pickle might give you an error for the namedtuples, even if they
        # are imported indirectly from ways.graph. You might need to declare, for
        # example: Link = ways.graph.Link
    Roads = ways.graph.load_map_from_csv("tlv.csv")
    final_list = []
    try:
        #phase a
        #runs normal ucs from source all abstract space nodes
        (ucs_paths,temp) = ucs.normal_ucs(Roads, source, list(abstractMap.keys()), float(1)/len(abstractMap))
        #if there is such paths get the first one which is to the closet node = junc1
        if ucs_paths:
            ucs_path = ucs_paths[0]
            #get the path
            junc1_path = ucs_path[2]
            #get the index of junc1
            junc1_index = ucs_path[0]
        # if this phace failed run normal ucs from A to B by throwing exception that is dealt after
        else:
            raise Exception("Phase a failed")

        #phase b
        #find the closet abstract space node to B by air distance
        junc2_index = -1
        junc2_min_distance = sys.maxsize
        #iterate over all possible nodes
        for center in list(abstractMap.keys()):
            #compute the distance using provided func
            current_distance = tools.compute_distance(Roads[center].lat,Roads[center].lon,Roads[target].lat,Roads[target].lon)
            #update if new node is closer to B
            if current_distance < junc2_min_distance:
                junc2_index = center
                junc2_min_distance = current_distance
        #run ucs from junc2 to B to get the path
        (ucs_paths,temp) = ucs.normal_ucs(Roads, junc2_index, [target], 1)
        if ucs_paths:
            ucs_path = ucs_paths[0]
            junc2_path = ucs_path[2]
        #if this phace failed run normal ucs from A to B by throwing exception that is dealt after
        else:
            raise Exception("Phase b failed")

        #phase c
        #run ucs from junc1 to junc2 in normal search space
        (ucs_paths,temp) = ucs.normal_ucs(abstractMap, junc1_index, [junc2_index], 1,lambda x: x.cost)
        if ucs_paths:
            #path for j1 to j2
            ucs_path = ucs_paths[0]
            abstract_index_list = ucs_path[2]
            expanded_index_list = []
            if junc1_index == junc2_index:
                junc_1_2_path = [junc1_index]
            else:
                expanded_tuple_list = []
                for i in range(1,len(abstract_index_list)):
                    # should return single value
                    #get the the links list which ucs returned
                    abstact_link_list = [lnk.path for lnk in abstractMap[abstract_index_list[i-1]].links if lnk.target == abstract_index_list[i]]
                    abstact_link_list = abstact_link_list[0]
                    #extracth the path from junc1 to junc2 from the link
                    expanded_tuple_list = expanded_tuple_list + abstact_link_list[1:len(abstact_link_list)]
                junc_1_2_path = expanded_tuple_list
        # if this phace failed run normal ucs from A to B by throwing exception that is dealt after
        else:
            raise Exception("Phase c failed")
        #append all three paths from phases a,b,c respectively
        return junc1_path + junc_1_2_path + junc2_path[1:len(junc2_path)]
    # exception is caught therefor we need to run norma ucs from A to B
    except:
        return base(source, target)




def dispatch(argv):
    from sys import argv
    source, target = int(argv[2]), int(argv[3])
    if argv[1] == 'base':
        path = base(source, target)
    elif argv[1] == 'bw':
        abstractMap = None
        if len(argv)>4:
            import pickle as pkl
            abstractMap = pkl.load(open(argv[4],'rb'))
        path = betterWaze(source, target,abstractMap)
    print(' '.join(str(j) for j in path))


if __name__ == '__main__':
    from sys import argv
    dispatch(argv)
