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
algorithm_file = sys.argv[2]
cypher_file = sys.argv[3]

algorithm_description = find_tag(algorithm_file, "introduction")

stream_graph_tag = "stream-sample-graph"
if len(sys.argv) >= 5:
    stream_graph_tag = sys.argv[4]

explanation_tag = "stream-sample-graph-explanation"
if len(sys.argv) >= 6:
    explanation_tag = sys.argv[5]

write_graph_tag = "write-sample-graph"
if len(sys.argv) >= 7:
    write_graph_tag = sys.argv[6]

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

streaming_graph_explanation_text = find_tag(algorithm_file, explanation_tag)

write_graph_text = '''We can also call a version of the algorithm that will store the result as a property on a
node. This is useful if we want to run future queries that use the result.'''

write_query_content = find_tag(cypher_file, write_graph_tag)

write_graph = '''\
write_query = """\

%s
"""

with driver.session() as session:
    session.write_transaction(lambda tx: tx.run(write_query))''' % write_query_content

viz_intro_text = '''\
## Graph Visualisation

Sometimes a picture can tell more than a table of results and this is often the case with graph algorithms. 
Let's see how to create a graph visualization using neovis.js.

First we'll create a div into which we will generate the visualisation.'''

python_to_js_text = '''Next we need to define the query that the visualization will be generated from, along with config 
that describes which properties will be used for node size, node colour, and relationship width. 

We'll then define a JavaScript variable that contains all our parameters.'''

neo_vis_js_text = '''Now we're ready to call neovis.js and generate our graph visualisation. 
The following code will create an interactive graph into the div defined above.
It will also extract an image representation of the graph and display that in the cell below.'''

query = "MATCH (p1:Page)-[r:LINKS]->(p2:Page) RETURN *"

labels_json = {
    "Page": {
        "caption": "name",
        "size": "pagerank"
    }
}

relationships_json = {
    "LINKS": {
        "thickness": "weight",
        "caption": False
    }
}

setup_js_graph_cell = '''\
from IPython.core.display import Javascript
import json
from scripts.algo import viz_config, render_image

config = viz_config("%s")
query = config["query"]
labels_json = config["labels_json"]
relationships_json = config["relationships_json"]

json_graph = {
    "query": query,
    "labels": labels_json,
    "relationships": relationships_json,
    "host": host,
    "user": user,
    "password": password
}

Javascript("""window.jsonGraph={};""".format(json.dumps(json_graph)))''' % algorithm_name

neo_vis_div_cell = '''\
%%html
<style type="text/css">                
.output_wrapper, .output {
    height:auto !important;
    max-height:600px;
}
.output_scroll {
    box-shadow:none !important;
    webkit-box-shadow:none !important;
}

#viz {
    width: 300px;
    height: 350px;
    font: 22pt arial;
}
</style>  
<div id="viz"></div>'''

neo_vis_js_cell = '''\
%%javascript
var output_area = this;
requirejs(['neovis.js'], function(NeoVis){    
    var config = {
      container_id: "viz",
      server_url: window.jsonGraph.host,
      server_user: window.jsonGraph.user,
      server_password: window.jsonGraph.password,
      labels: window.jsonGraph.labels,
      relationships: window.jsonGraph.relationships,
      initial_cypher: window.jsonGraph.query
    };
        
    let viz = new NeoVis.default(config);
    viz.render();
    
    viz.onVisualizationRendered(function(ctx) {
      let imageSrc = ctx.canvas.toDataURL();
      let kernel = IPython.notebook.kernel;
      let command = "image_src = '" + imageSrc + "'";
      kernel.execute(command);
      
      var cell_element = output_area.element.parents('.cell');
      var cell_idx = Jupyter.notebook.get_cell_elements().index(cell_element);
      var cell = Jupyter.notebook.get_cell(cell_idx+1);
      cell.set_text("render_image(image_src)")
      cell.execute();
    });
});'''

display_neo_vis_cell = ''''''

nb = nbf.v4.new_notebook()
nb['cells'] = [nbf.v4.new_markdown_cell(heading_text),
               nbf.v4.new_code_cell(imports),
               nbf.v4.new_markdown_cell(driver_setup_text),
               nbf.v4.new_code_cell(driver_setup),
               nbf.v4.new_markdown_cell(create_graph_text),
               nbf.v4.new_code_cell(create_graph),
               nbf.v4.new_markdown_cell(streaming_graph_text),
               nbf.v4.new_code_cell(run_algorithm),
               nbf.v4.new_markdown_cell(streaming_graph_explanation_text),
               nbf.v4.new_markdown_cell(write_graph_text),
               nbf.v4.new_code_cell(write_graph),
               nbf.v4.new_markdown_cell(viz_intro_text),
               nbf.v4.new_code_cell(neo_vis_div_cell),
               nbf.v4.new_markdown_cell(python_to_js_text),
               nbf.v4.new_code_cell(setup_js_graph_cell),
               nbf.v4.new_markdown_cell(neo_vis_js_text),
               nbf.v4.new_code_cell(neo_vis_js_cell),
               nbf.v4.new_code_cell(display_neo_vis_cell)
               ]

output_file = 'notebooks/{0}.ipynb'.format(algorithm_name.replace(" ", ""))

with open(output_file, 'w') as f:
    nbf.write(nb, f)
