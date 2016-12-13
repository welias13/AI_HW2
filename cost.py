import ways.graph as graph

# expected time is the g_cost function for each link fot the time based searched algorithm
def expected_time(link):
    return (link.distance/1000)/graph.current_speed(link)