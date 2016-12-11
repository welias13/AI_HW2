import ways.graph as graph


def time_cost_func(link):
    return (link.distance/1000)/graph.current_speed(link)