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

jupyter nbconvert --execute --inplace notebooks/PageRank.ipynb
jupyter nbconvert --execute --inplace notebooks/Louvain.ipynb
jupyter nbconvert --execute --inplace notebooks/BetweennessCentrality.ipynb
jupyter nbconvert --execute --inplace notebooks/ClosenessCentrality.ipynb
