import nbformat as nbf

algorithm_name = "Page Rank"
algorithm_description = "PageRank is Google’s popular search algorithm. PageRank works by counting the number and quality of links to a page to determine a rough estimate of how important the website is. The underlying assumption is that more important websites are likely to receive more links from other websites"

text = """\
# {0}
{1}
""".format(algorithm_name, algorithm_description)

imports = """\
from neo4j.v1 import GraphDatabase, basic_auth
import pandas as pd
import os"""

driver_setup = """\
host = os.environ.get("NEO4J_HOST", "bolt://localhost") 
user = os.environ.get("NEO4J_USER", "neo4j")
password = os.environ.get("NEO4J_PASSWORD", "neo")
driver = GraphDatabase.driver(host, auth=basic_auth(user, password))"""

with open("create_graph.txt", "r") as create_graph_file:
    create_graph_content = create_graph_file.read()

with open("streaming_query.txt", "r") as streaming_query_file:
    streaming_query_content = streaming_query_file.read()

create_graph = """\
create_graph_query = '''\

%s
'''

with driver.session() as session:
    result = session.write_transaction(lambda tx: tx.run(create_graph_query))
    print("Stats: " + str(result.consume().metadata.get("stats", {})))""" % create_graph_content

run_algorithm = '''\
streaming_query = """\

%s
"""

with driver.session() as session:
    result = session.read_transaction(lambda tx: tx.run(streaming_query))        
    df = pd.DataFrame([r.values() for r in result], columns=result.keys())
    
df''' % streaming_query_content


nb = nbf.v4.new_notebook()
nb['cells'] = [nbf.v4.new_markdown_cell(text),
               nbf.v4.new_code_cell(imports),
               nbf.v4.new_code_cell(driver_setup),
               nbf.v4.new_code_cell(create_graph),
               nbf.v4.new_code_cell(run_algorithm)]

output_file = '{0}_generated.ipynb'.format(algorithm_name.replace(" ", ""))

with open(output_file, 'w') as f:
    nbf.write(nb, f)
