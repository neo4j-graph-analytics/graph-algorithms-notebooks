#!/usr/bin/env bash


python generate_notebook.py \
    "Page Rank" \
    "https://github.com/neo4j-contrib/neo4j-graph-algorithms/raw/3.2/doc/asciidoc/pagerank.adoc" \
    "https://github.com/neo4j-contrib/neo4j-graph-algorithms/raw/3.2/doc/asciidoc/scripts/pagerank.cypher"

python generate_notebook.py \
    "Louvain" \
    "https://github.com/neo4j-contrib/neo4j-graph-algorithms/raw/3.2/doc/asciidoc/louvain.adoc" \
    "https://github.com/neo4j-contrib/neo4j-graph-algorithms/raw/3.2/doc/asciidoc/scripts/louvain.cypher"

python generate_notebook.py \
    "Betweenness Centrality" \
    "https://github.com/neo4j-contrib/neo4j-graph-algorithms/raw/3.2/doc/asciidoc/betweenness-centrality.adoc" \
    "https://github.com/neo4j-contrib/neo4j-graph-algorithms/raw/3.2/doc/asciidoc/scripts/betweenness-centrality.cypher"

python generate_notebook.py \
    "Closeness Centrality" \
    "https://github.com/neo4j-contrib/neo4j-graph-algorithms/raw/3.2/doc/asciidoc/closeness-centrality.adoc" \
    "https://github.com/neo4j-contrib/neo4j-graph-algorithms/raw/3.2/doc/asciidoc/scripts/closeness-centrality.cypher"

python generate_notebook.py \
    "Unweighted Connected Components" \
    "https://github.com/neo4j-contrib/neo4j-graph-algorithms/raw/3.2/doc/asciidoc/connected-components.adoc" \
    "https://github.com/neo4j-contrib/neo4j-graph-algorithms/raw/3.2/doc/asciidoc/scripts/connected-components.cypher" \
    "unweighted-stream-sample-graph"

python generate_notebook.py \
    "Weighted Connected Components" \
    "https://github.com/neo4j-contrib/neo4j-graph-algorithms/raw/3.2/doc/asciidoc/connected-components.adoc" \
    "https://github.com/neo4j-contrib/neo4j-graph-algorithms/raw/3.2/doc/asciidoc/scripts/connected-components.cypher" \
    "weighted-stream-sample-graph"

python generate_notebook.py \
    "Louvain" \
    "https://github.com/neo4j-contrib/neo4j-graph-algorithms/raw/3.2/doc/asciidoc/louvain.adoc" \
    "https://github.com/neo4j-contrib/neo4j-graph-algorithms/raw/3.2/doc/asciidoc/scripts/louvain.cypher"

python generate_notebook.py \
    "Single Source Shortest Path" \
    "https://github.com/neo4j-contrib/neo4j-graph-algorithms/raw/3.2/doc/asciidoc/single-shortest-path.adoc" \
    "https://github.com/neo4j-contrib/neo4j-graph-algorithms/raw/3.2/doc/asciidoc/scripts/single-shortest-path.cypher" \
    "single-pair-stream-sample-graph"

python generate_notebook.py \
    "All Pairs Shortest Path" \
    "https://github.com/neo4j-contrib/neo4j-graph-algorithms/raw/3.2/doc/asciidoc/all-pairs-shortest-path.adoc" \
    "https://github.com/neo4j-contrib/neo4j-graph-algorithms/raw/3.2/doc/asciidoc/scripts/single-shortest-path.cypher" \
    "all-pairs-sample-graph"

python generate_notebook.py \
    "Triangle Counting" \
    "https://github.com/neo4j-contrib/neo4j-graph-algorithms/blob/3.2/doc/asciidoc/triangleCount.adoc" \
    "https://github.com/neo4j-contrib/neo4j-graph-algorithms/raw/3.2/doc/asciidoc/scripts/triangle-count.cypher" \
    "stream-triples"


python empty.py
jupyter nbconvert --execute --inplace notebooks/PageRank.ipynb

python empty.py
jupyter nbconvert --execute --inplace notebooks/Louvain.ipynb

python empty.py
jupyter nbconvert --execute --inplace notebooks/BetweennessCentrality.ipynb

python empty.py
jupyter nbconvert --execute --inplace notebooks/ClosenessCentrality.ipynb

python empty.py
jupyter nbconvert --execute --inplace notebooks/UnweightedConnectedComponents.ipynb

python empty.py
jupyter nbconvert --execute --inplace notebooks/WeightedConnectedComponents.ipynb

python empty.py
jupyter nbconvert --execute --inplace notebooks/Louvain.ipynb

python empty.py
jupyter nbconvert --execute --inplace notebooks/SingleSourceShortestPath.ipynb

python empty.py
jupyter nbconvert --execute --inplace notebooks/AllPairsShortestPath.ipynb

python empty.py
jupyter nbconvert --execute --inplace notebooks/TriangleCounting.ipynb
