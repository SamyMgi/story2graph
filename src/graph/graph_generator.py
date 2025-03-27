import pandas as pd
import networkx as nx
from pyvis.network import Network


class GraphGenerator:
    def __init__(self, interaction_matrix_df):
        """
        Generate a graph from the Interaction Matrix.
        Args:
            interaction_matrix_df (pd.DataFrame): A DataFrame where the rows and columns represent characters, and each cell
                contains a score indicating the relationship between the characters.
                Values range from -1 (bad relationship) to +1 (good relationship).
        """
        self.im_df = interaction_matrix_df

    # Turning the interaction matrix into a graph G
    def _create_graph(self, colors):
        """
        Convert the Interaction Matrix to a Networkx Graph.
        Args:
            colors (list[str]): List of colors to be used for edges.

        Returns:
            G (Graph): Interaction Matrix as a Graph with characters as nodes and relationship as edges.
        """
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
        """
        Generates an interactive HTML visualization of the graph.
        Args:
            path (str): Path to save the graph output.
            colors_relationship (list[str], optional): List of colors to be used for edges.
                    Default: Blue for positive and red for negative.
            bgcolor (str, optional): Background color for the graph.
                    Default: White.
            font_color (str, optional): Font color for characters.
                    Default: Black.
        Returns:
            None: Saves the graph visualization as an HTML file.
        """
        G = self._create_graph(colors_relationship)
        nt = Network(height="800px", width="100%", bgcolor=bgcolor, font_color=font_color)
        nt.from_nx(G)
        path = path + ".html"
        nt.save_graph(path)
        print("Graph visualization saved at:", path)

    # Export the graph G into JSON
    def export_json(self, path):
        pass
