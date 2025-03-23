"""
    Generate graph from the Interaction Matrix.
"""

import numpy as np
import pandas as pd
import networkx as nx


class GraphGenerator:
    def __init__(self, interaction_matrix_df):
        self.im_df = interaction_matrix_df

    # Turning the interaction matrix into a graph G
    def _create_graph(self):
        characters = self.im_df.index
        G = nx.Graph()
        for char1 in characters:
            for char2 in characters:
                if char1 != char2:
                    if not pd.isna(self.im_df.loc[char1, char2]):
                        score = self.im_df.loc[char1, char2]
                        weight = 1 if score >= 0 else -1
                        G.add_edge(char1, char2, weight=weight)

        print("Nodes :", G.nodes())
        print("Edges :", G.edges(data=True))
        return G

    # Create and visualize the graph network
    def visualize_graph(self):
        self._create_graph()
        pass

    # Export the graph G into JSON
    def export_json(self):
        pass


data = {
    "Kevin": {"Kevin": np.nan, "Sam": 0.8, "Clu": -1},
    "Sam": {"Kevin": 0.8, "Sam": np.nan, "Clu": -0.5},
    "Clu": {"Kevin": -1, "Sam": -0.5, "Clu": np.nan},
}

df = pd.DataFrame(data)

gg = GraphGenerator(df)
gg.visualize_graph()
