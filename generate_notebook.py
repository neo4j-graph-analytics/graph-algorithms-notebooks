import re
import nbformat as nbf
import sys
from urllib.request import urlopen


def find_tag(file, tag):
    inner_text = ""
    found_tag = False
    with urlopen(file) as pagerank_file:
        for line in pagerank_file.readlines():
            line = line.decode("utf-8")
            if line.startswith("// tag::"):
                groups = re.match("// tag::(.*)\[\]", line)
                tag_name = groups[1]
                if tag_name == tag:
                    found_tag = True
                    continue
            if line.startswith("// end::"):
                groups = re.match("// end::(.*)\[\]", line)
                tag_name = groups[1]
                if tag_name == tag:
                    found_tag = False
                    continue
            if found_tag:
                inner_text += "{0}".format(line)
    return inner_text.strip()


if len(sys.argv) < 4:
    print("Usage: python generate_notebook.py <Algorithm Name> <Description> <Cypher File>")
    sys.exit(1)

algorithm_name = sys.argv[1]
algorithm_description = find_tag(sys.argv[2], "introduction")
cypher_file = sys.argv[3]

stream_graph_tag = "stream-sample-graph"
if len(sys.argv) >= 5:
    stream_graph_tag = sys.argv[4]


heading_text = """\
# {0}
{1}

First we'll import the Neo4j driver and Pandas libraries:
""".format(algorithm_name, algorithm_description)

imports = """\
from neo4j.v1 import GraphDatabase, basic_auth
import pandas as pd
import os"""

driver_setup_text = """\
Next let's create an instance of the Neo4j driver which we'll use to execute our queries.
"""

driver_setup = """\
host = os.environ.get("NEO4J_HOST", "bolt://localhost") 
user = os.environ.get("NEO4J_USER", "neo4j")
password = os.environ.get("NEO4J_PASSWORD", "neo")
driver = GraphDatabase.driver(host, auth=basic_auth(user, password))"""

create_graph_text = """\
Now let's create a sample graph that we'll run the algorithm against.
"""

create_graph_content = find_tag(cypher_file, "create-sample-graph")
create_graph = """\
create_graph_query = '''\

%s
'''

with driver.session() as session:
    result = session.write_transaction(lambda tx: tx.run(create_graph_query))
    print("Stats: " + str(result.consume().metadata.get("stats", {})))""" % create_graph_content

streaming_graph_text = """\
Finally we can run the algorithm by executing the following query:
"""

streaming_query_content = find_tag(cypher_file, stream_graph_tag)
run_algorithm = '''\
streaming_query = """\

%s
"""

with driver.session() as session:
    result = session.read_transaction(lambda tx: tx.run(streaming_query))        
    df = pd.DataFrame([r.values() for r in result], columns=result.keys())

df''' % streaming_query_content

nb = nbf.v4.new_notebook()
nb['cells'] = [nbf.v4.new_markdown_cell(heading_text),
               nbf.v4.new_code_cell(imports),
               nbf.v4.new_markdown_cell(driver_setup_text),
               nbf.v4.new_code_cell(driver_setup),
               nbf.v4.new_markdown_cell(create_graph_text),
               nbf.v4.new_code_cell(create_graph),
               nbf.v4.new_markdown_cell(streaming_graph_text),
               nbf.v4.new_code_cell(run_algorithm)]

output_file = 'notebooks/{0}.ipynb'.format(algorithm_name.replace(" ", ""))

with open(output_file, 'w') as f:
    nbf.write(nb, f)
