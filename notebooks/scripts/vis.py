from IPython.display import IFrame
import json
import uuid

def generate_vis(host, user, password, cypher):
    html = """\
    <!doctype html>
    <html>
        <head>
            <title>Neovis.js Simple Example</title>
            <style type="text/css">
                html, body {{
                    font: 16pt arial;
                }}

                #viz {{
                    width: 100%;
                    height: 500px;
                    font: 22pt arial;
                }}
            </style>

            <script type="text/javascript" src="neovis.js"></script>

            <script
                    src="https://code.jquery.com/jquery-3.2.1.min.js"
                    integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4="
                    crossorigin="anonymous"></script>

            <script type="text/javascript">
                var viz;

                function draw() {{
                    var config = {{
                        container_id: "viz",
                        server_url: "{host}",
                        server_user: "{user}",
                        server_password: "{password}",
                        labels: {{
                            "Page": {{
                                "caption": "name",
                                "size": "pagerank"
                            }}
                        }},
                        relationships: {{
                            "LINKS": {{
                                "thickness": "weight",
                                "caption": false
                            }}
                        }},
                        initial_cypher: "{cypher}"
                    }};

                    viz = new NeoVis.default(config);
                    viz.render();
                    console.log(viz);

                }}
            </script>
        </head>
        <body onload="draw()">
            <div id="viz"></div>
        </body>
    </html>
    """
    html = html.format(host = host, user=user, password=password, cypher=cypher)
    unique_id = str(uuid.uuid4())

    filename = "figure/graph-{}.html".format(unique_id)
    with open(filename, "w") as f:
        f.write(html)

    return IFrame(filename, width="100%", height="550px")
