from flask import Flask, jsonify, request
from flask_cors import CORS

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
adjacency_matrix_insta = ke.get_adjacency_matrix(profiles_names, en_key_words)



print(adjacency_matrix_insta.head())

# Plot the graph using networkx
iG = nx.from_pandas_adjacency(adjacency_matrix_insta)
pos = nx.spring_layout(iG)

positions = list(map(lambda row: ({'id': row, 'x': pos[row][0], 'y': pos[row][1]}), pos))

_,weights = zip(*nx.get_edge_attributes(iG,'weight').items())

nodes = nx.draw_networkx_nodes(iG, pos, node_color="b")
edges = nx.draw_networkx_edges(iG, pos,
                            edge_color=weights, edge_cmap=plt.cm.Blues)
nx.draw_networkx_labels(iG, pos, font_color="black")


weighted_adjacency_list = []

for row_name, row in adjacency_matrix_insta.iterrows():
    for col_name, value in row.iteritems():
        if value > 0:
            lst = {'source': row_name, 'target': col_name, 'weight': value}
            weighted_adjacency_list.append(lst)

#%% Get values from sofifa
import profiles_names as pn
from sofifa_scraping import SofifaScraping
so = SofifaScraping('sofifa_processed.csv')
so.get_footballer_dict(pn.names)
adjacency_matrix_sofifa = so.get_cosine_similarity_matrix(pn.dct_profiles)

#%%
# Path: backend\app_flask.py

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def find_similar_insta():
    return jsonify(positions)


@app.route("/weighted_edges", methods=["GET"])
def get_weighted_edges():
    print("get_weighted_edges function called")
    try:
        result = jsonify(weighted_adjacency_list)
        print("jsonify succeeded")
        return result
    except Exception as e:
        print(f"Error in jsonify: {e}")
        return "Error converting data to JSON format", 500


@app.route("/similarity/insta/<player_name>", methods=["GET"])
@app.route("/similarity/insta/<player_name>/<int:number>", methods=["GET"])
def get_insta_similarity(player_name: str, number: int = 5):

    notna_and_not_zero = adjacency_matrix_insta[player_name].notna() & (adjacency_matrix_insta[player_name] != 0)
    similarity = adjacency_matrix_insta[player_name][notna_and_not_zero].nlargest(number).to_json()
    
    return jsonify(similarity)
    

@app.route("/similarity/sofifa/<player_name>", methods=["GET"])
@app.route("/similarity/sofifa/<player_name>/<int:number>", methods=["GET"])
def get_sofifa_similarity(player_name: str, number: int = 5):
    notna_and_not_zero = adjacency_matrix_sofifa[player_name].notna() & (adjacency_matrix_sofifa[player_name] != 0)
    similarity = adjacency_matrix_sofifa[player_name][notna_and_not_zero].nlargest(number).to_json()
    
    return jsonify(similarity)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
