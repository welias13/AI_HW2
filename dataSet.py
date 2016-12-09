import ways.tools as tools
import random
import ucs
import logging
import csv
import ways

#function generate data set which is pairs of nodes the minimal path between them is 200 links
# @tools.timed
def generate_data_set(Roads):
    data_set = {}
    #we need 20 pairs
    for i in range(0,20):
        nodes = Roads.keys()
        #generating random node to be the start node
        random_start_node = random.choice(list(nodes))
        #check is this node was used before, continue if yes and generating new one
        while random_start_node in data_set or not Roads[random_start_node].links:
            random_start_node = random.choice(list(nodes))
        while True:
            # generate random node to be goal node
            random_goal_node = random.choice(list(nodes))
            #calculate path from random_start_node to random_goal_node
            paths_to_heaven = ucs.minimal_ucs(Roads, random_start_node, [random_goal_node], m = 1)
            #check if the returned path is atleast 200 links,if not do the process again
            if paths_to_heaven and len(paths_to_heaven[0][2]) >= 200:
                data_set[random_start_node] = paths_to_heaven[0][0]
                break
    #writing the output file,each row is start,goal
    with open('dataSet.csv', 'w', newline='') as out:
        csv_out = csv.writer(out)
        for junc_pair in data_set.items():
            csv_out.writerow(junc_pair)


if __name__ == "__main__":
    logging.info("Main start")
    logging.info("Loading Roads")
    Roads = ways.graph.load_map_from_csv("tlv.csv")
    logging.info("load finished")
    logging.info("generating data set")
    generate_data_set(Roads)
    logging.info("generating data set finished")