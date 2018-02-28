from IPython.display import IFrame, HTML
import json
import uuid

def generate_vis(host, user, password, cypher):
    html = """\
<html>
<head>
    <title>Neovis.js Simple Example</title>
            <style type="text/css">
                html, body {{
                    font: 16pt arial;
                }}

                #viz {{
                    width: 300px;
                    height: 400px;
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
                    viz.onVisualizationRendered(function(ctx) {{
                        let imageSrc = document.getElementsByTagName("canvas")[0].toDataURL();
                        console.log(imageSrc);
                        document.getElementById("viz-image").src=imageSrc;
                        document.getElementById("viz").style="display:none";
                    }});

                }}
            </script>

         </head>
        <body onload="draw()">
            <div id="viz"></div>

            <img id="viz-image" src="" height="300px" />
        </body>


    </html>
    """
    html = html.format(host = host, user=user, password=password, cypher=cypher)
    unique_id = str(uuid.uuid4())

    filename = "figure/graph-{}.html".format(unique_id)
    with open(filename, "w") as f:
        f.write(html)

#     print(filename)

#     return HTML(html)

#     return HTML(html)
    
    return IFrame(filename, width="100%", height="320px")
