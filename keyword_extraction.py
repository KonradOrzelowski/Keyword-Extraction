#%%
import utils as utils

# import torch
# import numpy as np
# import pandas as pd
# import networkx as nx
# import matplotlib as mpl
# import matplotlib.pyplot as plt
import time

from datetime import datetime

from code_timer import CodeTimer

from keybert import KeyBERT
from nltk.stem.wordnet import WordNetLemmatizer
from sentence_transformers import SentenceTransformer
from keyphrase_vectorizers import KeyphraseCountVectorizer
#%%

class KeywordExtraction:
    def __init__(self, profiles, threshold_kw,
                 start_date = datetime(2000, 11, 1),
                 end_date = datetime(2023, 1, 5)):
        
        self.__lemmatizer = WordNetLemmatizer()
        self.__kw_model = KeyBERT()
        self.__vectorizer = KeyphraseCountVectorizer()
        self.__sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.__threshold_kw = threshold_kw
        
        self.__start_date = start_date
        self.__end_date = end_date      
        
        self.all_docs = self.read_profiles(profiles, self.__start_date, self.__end_date)
        self.all_kw = self.find_all_keywords(profiles, self.all_docs, threshold_kw)
        self.encoding = self.encode_keywords(profiles, self.all_kw)

    def read_profiles(self, profiles: list[str], start_date, end_date) -> dict:
        '''Read all docs without emoji'''
        with CodeTimer('self.all_docs'):
            all_docs = {}
            for profile in profiles:
                # print(profile)
                all_docs[profile] = utils.read_from_time_range(self.__lemmatizer, profile,
                                                               start_date, end_date)
        return all_docs

    def find_all_keywords(self, profiles: list[str], all_docs: dict, threshold:float) -> dict:
        with CodeTimer('self.all_kw'):
            all_kw = {}
            for profile in profiles:
                print(profile)
                try:
                    all_kw[profile] = utils.extract_kw_from_docs(
                        all_docs[profile], self.__kw_model, self.__vectorizer)
                    all_kw[profile] = utils.remove_sim_kw(all_kw[profile], threshold)
                except:
                    all_kw[profile] = ['']
        return all_kw

    def encode_keywords(self, profiles: list[str], key_words: dict) -> dict:
        with CodeTimer('self.encoding'):
            encoding = {}
            for profile in profiles:
                encoding[profile] = self.__sentence_transformer.encode(key_words[profile],
                                                                       show_progress_bar=True)
        return encoding

    def add_profile(self, profile, start_date=datetime(2000, 11, 1), end_date=datetime(2023, 1, 5)):
        self.all_docs[profile] = utils.read_from_time_range(self.__lemmatizer, profile, start_date, end_date)
        self.all_kw[profile] = utils.extract_kw_from_docs(self.all_docs[profile], self.__kw_model, self.__vectorizer)
        self.all_kw[profile] = utils.remove_sim_kw(self.all_kw[profile], self.__threshold_kw)
        self.encoding[profile] = self.__sentence_transformer.encode(self.all_kw[profile], show_progress_bar=True)
