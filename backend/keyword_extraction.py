#%%
import functools
from sql_info import sql_info
import pandas as pd
import time
import numpy as np
from datetime import datetime

# from code_timer import CodeTimer
from connect_mysql import MySQLConnection

from keybert import KeyBERT
from nltk.stem.wordnet import WordNetLemmatizer
from sentence_transformers import SentenceTransformer, util
from keyphrase_vectorizers import KeyphraseCountVectorizer


from typing import List
from functools import reduce
from nltk.stem import WordNetLemmatizer
import pandas as pd

from typing import List

import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
#%%

class KeywordExtraction:
    """
    Class for extracting keywords from a set of documents.

    Attributes:
    - connection: MySQLConnection object for connecting to the database
    - lemmatizer: WordNetLemmatizer object for lemmatizing words
    - model: KeyBERT object for extracting keywords
    - vectorizer: KeyphraseCountVectorizer object for transforming documents into a matrix of word counts
    - sentence_transformer: SentenceTransformer object for encoding sentences
    - threshold_kw: float, threshold score for selecting keywords (default=0.5)
    """
    def __init__(self, threshold_kw: float = 0.5):
        """
        Initialize the KeywordExtraction object.

        Args:
        - threshold_kw: float, threshold score for selecting keywords (default=0.5)
        """
        self.connection = MySQLConnection(sql_info['host'], sql_info['user'],
                                          sql_info['password'], sql_info['database'])
        
        self.lemmatizer = WordNetLemmatizer()
        self.model = KeyBERT()
        self.vectorizer = KeyphraseCountVectorizer()
        self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.threshold_kw = threshold_kw

    def jaccard_similarity(self, keyword_1: str, keyword_2: str) -> float:
        set_1 = set(keyword_1.split())
        set_2 = set(keyword_2.split())
        return len(set_1.intersection(set_2)) / len(set_1.union(set_2))

    def remove_similar_keywords(self, all_keywords: list[str]) -> list[str]:
        """
        Remove similar keywords from the list of all keywords.

        Args:
        - all_keywords: list of str, all keywords to be processed

        Returns:
        - list of str, filtered list of unique keywords

        This function uses Jaccard similarity to compare each keyword in all_keywords
        with already processed keywords stored in the unique_keywords list.
        If the Jaccard similarity between the keyword and any of the unique keywords is above 0.8,
        the keyword is considered similar and will not be added to the unique_keywords list.
        """
        unique_keywords = [] # initialize an empty list to store unique keywords
        for keyword in all_keywords: # iterate over all keywords
            is_unique = True # assume keyword is unique
            for unique_keyword in unique_keywords: # iterate over already processed unique keywords
                if self.jaccard_similarity(keyword, unique_keyword) > 0.8: # compare similarity between keyword and unique keyword
                    is_unique = False # keyword is not unique
                    break # no need to continue comparison
            if is_unique: # keyword is unique
                unique_keywords.append(keyword) # add keyword to the list of unique keywords
        return unique_keywords # return the filtered list of unique keywords


    def read_table(self, table: str) -> pd.DataFrame:
        """
        Read all documents from the database.

        Args:
        - table: str, name of the table to read

        Returns:
        - pandas DataFrame, containing all documents
        """
        return self.connection.select_all_from_data(table_name='posts')
    
    def get_keywords(self, docs_df: pd.DataFrame) -> dict[str, List[str]]:
        """
        Extract keywords from a set of documents.

        Args:
        - docs_df: pandas DataFrame, containing documents to extract keywords from

        Returns:
        - dict, mapping profile names to lists of keywords


        When comparing two sentences, Jaccard similarity is often a better choice
        than cosine similarity. Jaccard similarity is designed to compare the similarity
        between two sets, and a sentence can be represented as a set of words.
        This allows Jaccard similarity to take into account not only the presence
        or absence of words, but also their frequency and order.
        """
        unique_profile_names = docs_df['profile_name'].unique().tolist()
        profiles = docs_df.groupby('profile_name')['content'].apply(list).to_dict()
        all_kw = {}

        for profile_name in unique_profile_names:
            print(f"Extracting keywords for profile: {profile_name}")
            # Get all keywords for the profile
            key_words = self.model.extract_keywords(docs=profiles[profile_name], 
                                            vectorizer=self.vectorizer)
        
            # the concatenation of all elements
            # in the list key_words into a single list
            if(len(key_words) == 0):
                all_kw[profile_name] = []
                continue

            if type(key_words[0]) == list:                             
                key_words = functools.reduce(lambda x,y: x+y,key_words)
            # Filter keywords by threshold
            profile_key_words = [i[0] for i in key_words if i[1] > self.threshold_kw]
            # Remove similar keywords
            old_len = len(profile_key_words)
            profile_key_words = self.remove_similar_keywords(profile_key_words)
            new_len = len(profile_key_words)
            print(f"Removed {old_len - new_len} similar keywords")
            all_kw[profile_name] = profile_key_words
            
        return all_kw

    def encode_keywords(self, profiles: list[str], key_words: dict) -> dict:
        encoding = {}
        for profile in profiles:
            encoding[profile] = self.sentence_transformer.encode(key_words[profile],
                                                                 show_progress_bar=True)
        return encoding

    def get_adjacency_matrix(self, profiles_names, en_key_words):
        df_list = []
        for i in profiles_names:
            lst = []
            for j in profiles_names:
                try:
                    all_en = en_key_words
                    similarity = self.get_cos_similarity(all_en[i], all_en[j], threshold=0.5)
                    lst.append(similarity)
                except:
                    lst.append(0)
            df_list.append(lst)

        na = np.array(df_list)
        np.fill_diagonal(na, 0)
        row_sums = na.sum(axis=1)
        na /= row_sums[:, np.newaxis]
        na = np.nan_to_num(na)

        df = pd.DataFrame(na)
        df.columns = profiles_names
        df.index = profiles_names

        return df
    def get_cos_similarity(self, nd1: np.ndarray, nd2: np.ndarray,
                                                threshold = 0.5) -> np.float32:
        
        cos_ndarray = util.pytorch_cos_sim(nd1, nd2).numpy()
        cos_ndarray = cos_ndarray.flatten()
        
        N_most = np.sort(cos_ndarray)[::-1][:10]
        
        return np.sum(N_most[N_most>threshold])

    # def add_profile(self, profile, start_date=datetime(2000, 11, 1), end_date=datetime(2023, 1, 5)):
    #     self.all_docs[profile] = utils.read_from_time_range(self.lemmatizer, profile, start_date, end_date)
    #     self.all_kw[profile] = utils.extract_kw_from_docs(self.all_docs[profile], self.model, self.vectorizer)
    #     self.all_kw[profile] = utils.remove_sim_kw(self.all_kw[profile], self.threshold_kw)
    #     self.encoding[profile] = self.sentence_transformer.encode(self.all_kw[profile], show_progress_bar=True)

#%%
def main():
    ke = KeywordExtraction()
    df = ke.read_table('posts')

    # key_words = ke.get_keywords(df.sample(n=200, random_state=1))
    key_words = ke.get_keywords(df)
    profiles_names = list(key_words.keys())
    en_key_words = ke.encode_keywords(profiles_names, key_words)
    adjacency_matrix = ke.get_adjacency_matrix(profiles_names, en_key_words)


    # Plot the graph using networkx
    iG = nx.from_pandas_adjacency(adjacency_matrix)
    pos = nx.spring_layout(iG)


    _,weights = zip(*nx.get_edge_attributes(iG,'weight').items())

    nodes = nx.draw_networkx_nodes(iG, pos, node_color="b")
    edges = nx.draw_networkx_edges(iG, pos,
                                edge_color=weights, edge_cmap=plt.cm.Blues)
    nx.draw_networkx_labels(iG, pos, font_color="black")

    fig = mpl.pyplot.gcf()
    fig.set_size_inches(18.5, 10.5)
    # fig.savefig('insta.png', dpi=360)
    plt.show()

if __name__ == "__main__":
    main()
#%%
# columns = {"id": "INT AUTO_INCREMENT PRIMARY KEY", "profile_name": "VARCHAR(255) NOT NULL", "key_word": "VARCHAR(255) NOT NULL"}

# ke.connection.add_table("key_words", columns)

