from flask import Blueprint, render_template, send_file
import matplotlib.pyplot as plt
from io import BytesIO
import networkx as nx

webui_blueprint = Blueprint('webui_blueprint', __name__)


@webui_blueprint.route('/<int:nodes>')
def ind(nodes):
    # az index hiv bele a lenti függvénybe
    return render_template("index.html", nodes=nodes)


@webui_blueprint.route('/graph/<int:nodes>')
def graph(nodes):
    G = nx.complete_graph(nodes)
    nx.draw(G)

    img = BytesIO()  # file-like object for the image
    plt.savefig(img)  # save the image to the stream
    img.seek(0)  # writing moved the cursor to the end of the file, reset
    plt.clf()  # clear pyplot

    # Here, I'm creating the ontology class and use here the ontology

    return send_file(img, mimetype='image/png')
