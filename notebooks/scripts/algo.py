from IPython.core.display import HTML


def viz_config(algorithm_name):
    return {
        "Page Rank": {
            "query": "MATCH (p1:Page)-[r:LINKS]->(p2:Page) RETURN *",
            "labels_json": {
                'Page': {
                    'caption': 'name',
                    'size': 'pagerank'
                }
            },
            "relationships_json": {
                'LINKS': {
                    'thickness': 'weight',
                    'caption': False
                }
            }
        },
        "Betweenness Centrality": {
            "query": "MATCH (p1:User)-[r:MANAGE]->(p2:User) RETURN *",
            "labels_json": {
                'User': {
                    'caption': 'id',
                    'size': 'centrality'
                }
            },
            "relationships_json": {
                'MANAGE': {
                    'thickness': 'weight',
                    'caption': False
                }
            }
        },
        "Closeness Centrality": {
            "query": "MATCH (p1:Node)-[r:LINK]->(p2:Node) RETURN *",
            "labels_json": {
                'Node': {
                    'caption': 'id',
                    'size': 'centrality'
                }
            },
            "relationships_json": {
                'LINK': {
                    'thickness': 'weight',
                    'caption': False
                }
            }
        },
        "Louvain": {
            "query": "MATCH (p1:User)-[r:FRIEND]->(p2:User) RETURN *",
            "labels_json": {
                'User': {
                    'caption': 'id',
                    'size': 'centrality',
                    'community': 'community'
                }
            },
            "relationships_json": {
                'FRIEND': {
                    'thickness': 'weight',
                    'caption': False
                }
            }
        },
        "Strongly Connected Components": {
            "query": "MATCH (p1:User)-[r:FOLLOW]->(p2:User) RETURN *",
            "labels_json": {
                'User': {
                    'caption': 'id',
                    'community': 'partition'
                }
            },
            "relationships_json": {
                'FOLLOW': {
                    'thickness': 'weight',
                    'caption': False
                }
            }
        }
    }[algorithm_name]


def render_image(image_src):
    return HTML('<img id="viz-image" width="300px" src="%s" />' % image_src)
