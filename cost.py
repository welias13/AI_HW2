import ways.graph as graph


def expected_time(link):
    return (link.distance/1000)/graph.current_speed(link)