from IPython.core.display import HTML


def viz_config(algorithm_name):
    return {
        "Page Rank": {
            "query": "MATCH (p1:Page)-[r:LINKS]->(p2:Page) RETURN *",
            "labels_json": {'Page': {'caption': 'name', 'size': 'pagerank'}},
            "relationships_json": {'LINKS': {'thickness': 'weight', 'caption': False}}
        }
    }[algorithm_name]


def render_image(image_src):
    return HTML('<img id="viz-image" width="300px" src="%s" />' % image_src)
