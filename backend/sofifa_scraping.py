import pandas as pd

import profiles_names as pn
import itertools
import numpy as np

class SofifaScraping:
    def __init__(self, path2dataset):
        self.footballers = {}

        self.dataset = pd.read_csv(path2dataset, index_col = None)
        
        self.footballer_info = self.dataset[['Name', 'Country', 'Club', 'Id','Salary', 'Value']]
        self.footballer_atr = self.dataset.loc[:,~self.dataset.columns.isin(
                                            ['Country', 'Club', 'Id','Salary', 'Value'])]
        
    
    def get_footballer_atr(self, name, col = 'Name'):
        row = self.footballer_atr[self.footballer_atr[col] == name]
        row = row[row['Overall'] == max(row['Overall'])]
        return row.loc[:,~row.columns.isin(['Name'])]
    
    def get_footballer_info(self, name, col = 'Name'):
        row = self.footballer_atr[self.footballer_atr[col] == name]
        return row[row['Salary'] == max(row['Salary'])]
    
    def get_footballer_dict(self, names: list[str]):
        self.footballers = {name: self.get_footballer_atr(name).values.flatten() for name in names}


    def get_cosine_similarity_matrix(self, dct_profiles: dict):
        names = list(dct_profiles.values())
        # create a temporary dictionary that maps each name to its vector
        temp_dict = {name: self.footballers[name] for name in names}
        
        # precompute the norm of each vector
        norm_dict = {name: np.linalg.norm(temp_dict[name]) for name in names}

        # initialize the 2D array to store cosine similarity values
        cos_sim_array = np.zeros((len(names), len(names)))
        
        # loop through each pair of footballers
        for i, j in itertools.combinations(range(len(names)), 2):
            name1, name2 = names[i], names[j]
            
            # compute the cosine similarity using the precomputed norms and the temporary dictionary
            cos_sim = np.dot(temp_dict[name1], temp_dict[name2]) / (norm_dict[name1] * norm_dict[name2])
            
            # store the cosine similarity value in the array at the appropriate indices
            cos_sim_array[i, j] = cos_sim
            cos_sim_array[j, i] = cos_sim
        
        # fill the diagonal with 0s
        np.fill_diagonal(cos_sim_array, 0)
        
        row_sums = cos_sim_array.sum(axis=1)
        # normalize the array
        cos_sim_array = cos_sim_array / row_sums[:, np.newaxis]

        # create a pandas dataframe from the array
        df = pd.DataFrame(cos_sim_array)
        # set the column and index names to the footballer names
        insta_names = list(dct_profiles.keys())

        df.columns = insta_names
        df.index = insta_names

        return df
    
    
#%%
def main():
    
    so = SofifaScraping('sofifa_processed.csv')
    so.get_footballer_dict(pn.names)
    adjacency_matrix_sofifa = so.get_cosine_similarity_matrix(pn.names)
    print(adjacency_matrix_sofifa)

      
      
# if __name__ == '__main__':
#     main()
