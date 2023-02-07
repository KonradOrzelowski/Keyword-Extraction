from flask import Flask, jsonify, request
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
from keyword_extraction import KeywordExtraction
#%% Create a KeywordExtraction object
ke = KeywordExtraction()
df = ke.read_table('posts')

key_words = ke.get_keywords(df.sample(n=200, random_state=1))
# key_words = ke.get_keywords(df)
profiles_names = list(key_words.keys())
en_key_words = ke.encode_keywords(profiles_names, key_words)
adjacency_matrix = ke.get_adjacency_matrix(profiles_names, en_key_words)

print(adjacency_matrix.head())

# Plot the graph using networkx
iG = nx.from_pandas_adjacency(adjacency_matrix)
pos = nx.spring_layout(iG)


_,weights = zip(*nx.get_edge_attributes(iG,'weight').items())

nodes = nx.draw_networkx_nodes(iG, pos, node_color="b")
edges = nx.draw_networkx_edges(iG, pos,
                            edge_color=weights, edge_cmap=plt.cm.Blues)
nx.draw_networkx_labels(iG, pos, font_color="black")

# fig = mpl.pyplot.gcf()
# fig.set_size_inches(18.5, 10.5)
# # fig.savefig('insta.png', dpi=360)
# plt.show()


#%%
# Path: backend\app_flask.py



for row in pos:
    pos[row] = pos[row].tolist()
    print(pos[row])

app = Flask(__name__)
@app.route("/", methods=["GET"])
def find_similar_insta():
    return jsonify(pos)



if __name__ == '__main__':
    app.run(host='0.0.0.0')


# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"


# if __name__ == '__main__':
#     app.run(host='0.0.0.0')