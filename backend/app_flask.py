from flask import Flask, jsonify, request
from flask_cors import CORS

import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
from keyword_extraction import KeywordExtraction
#%% Create a KeywordExtraction object
ke = KeywordExtraction()
posts_df = ke.read_table('posts')
posts_df = posts_df.sample(n=200, random_state=1)

key_words = ke.get_keywords(posts_df)
key_words_with_id = ke.get_keywords_with_id(posts_df)
profiles_names = list(key_words.keys())
en_key_words = ke.encode_keywords(profiles_names, key_words)
adjacency_matrix_insta = ke.get_adjacency_matrix(profiles_names, en_key_words)


def get_positions(adjacency_matrix: pd.DataFrame) -> list:
    """
    Given an adjacency matrix, returns a list of dictionaries, where each dictionary 
    represents a node with its position in the 2D space. The positions are calculated 
    using the spring layout algorithm from the NetworkX library.
    
    Parameters:
        adjacency_matrix (pd.DataFrame): The adjacency matrix of the graph.
    
    Returns:
        list: A list of dictionaries, where each dictionary contains the id, x, and y 
        values of a node's position.
    """
    # Create a NetworkX graph object from the adjacency matrix
    iG = nx.from_pandas_adjacency(adjacency_matrix)
    
    # Compute the positions of the nodes using the spring layout algorithm
    pos = nx.spring_layout(iG)
    
    # Convert the positions to a list of dictionaries containing the node's id, x, and y values
    positions = list(map(lambda row: ({'id': row, 'x': pos[row][0], 'y': pos[row][1]}), pos))

    # Return the list of node positions
    return positions


def get_weighted_edges(adjacency_matrix: pd.DataFrame) -> list:
    """
    Given an adjacency matrix, returns a list of dictionaries, where each dictionary 
    represents an edge with its weight. Only the edges with weights greater than 0 
    are included in the list.
    
    Parameters:
        adjacency_matrix (pd.DataFrame): The adjacency matrix of the graph.
    
    Returns:
        list: A list of dictionaries, where each dictionary contains the source, target, 
        and weight values of an edge.
    """
    # Initialize an empty list to store the weighted edges
    weighted_adjacency_list = []
    
    # Loop through each row and column of the adjacency matrix
    for row_name, row in adjacency_matrix_insta.iterrows():
        for col_name, value in row.iteritems():
            # If the weight is greater than 0, create a dictionary with the edge information
            if value > 0:
                lst = {'source': row_name, 'target': col_name, 'weight': value}
                # Append the dictionary to the list of weighted edges
                weighted_adjacency_list.append(lst)

    # Return the list of weighted edges
    return weighted_adjacency_list


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
    return jsonify(get_positions(adjacency_matrix_insta))


@app.route("/weighted_edges", methods=["GET"])
def get_weighted_edges():
    print("get_weighted_edges function called")
    try:
        result = jsonify(get_weighted_edges(adjacency_matrix_insta))
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

@app.route("/atr/sofifa/<player_name>", methods=["GET"])
def get_footbaler_atr(player_name: str):
    atr = so.get_footballer_atr(pn.dct_profiles[player_name]).to_dict('records')[0]
    print(atr)
    return jsonify(atr)

import pandas as pd
@app.route("/content/key_words/<player_name>", methods=["GET"])
def get_key_words(player_name: str):
    # get all posts of selected profile
    filtered_df = posts_df[posts_df['profile_name'] == player_name]
    # merge posts with keywords
    merged_df = pd.merge(filtered_df, key_words_with_id, on='id')
    # group by content and create a list of keywords
    grouped_df = merged_df.groupby(['profile_name','content', 'date'])['keyword'].apply(list).reset_index()
    return jsonify(grouped_df.to_json(orient='records'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
