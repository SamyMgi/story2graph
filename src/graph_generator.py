"""
    Generate graph from the Interaction Matrix.
"""

import numpy as np
import pandas as pd
import networkx as nx
from pyvis.network import Network


class GraphGenerator:
    def __init__(self, interaction_matrix_df):
        self.im_df = interaction_matrix_df

    # Turning the interaction matrix into a graph G
    def _create_graph(self, colors):
        characters = self.im_df.index
        G = nx.Graph()
        for char1 in characters:
            for char2 in characters:
                if char1 != char2:
                    if not pd.isna(self.im_df.loc[char1, char2]):
                        score = self.im_df.loc[char1, char2]
                        # Simplifying the scores/weights
                        weight = 1 if score >= 0 else -1
                        color = colors[0] if weight == 1 else colors[1]
                        G.add_edge(char1, char2, weight=weight, color=color)

        print("Nodes :", G.nodes())
        print("Edges :", G.edges(data=True))
        return G

    # Create and visualize the graph network
    def generate_graph_viz(self, path, colors_relationship=["blue", "red"], bgcolor="#FFFFFF", font_color="#000000"):
        G = self._create_graph(colors_relationship)
        nt = Network(height="800px", width="100%", bgcolor=bgcolor, font_color=font_color)
        nt.from_nx(G)
        path = path + ".html"
        nt.save_graph(path)
        print("Graph visualization saved at:", path)

    # Export the graph G into JSON
    def export_json(self):
        pass
