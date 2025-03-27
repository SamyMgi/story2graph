from src.nlp.coref_resolution import CorefResolution
from src.nlp.interaction_matrix import InteractionMatrix
from src.graph.graph_generator import GraphGenerator


class Story2Graph:
    def __init__(self, input_text, path=False):
        """
        Generate a graph from an input story.
        Args:
            input_text (str): Either raw text or a file path containing the story.
            path (bool, optional): Set to True if `input_text` is a file path,
                                   otherwise assumes raw text. Default is False.
        """
        self.text = self._load_text(input_text) if path else input_text
        self._characters = None
        self._resolved_text = None
        self._im_df = None

    @staticmethod
    def _load_text(input_path):
        """
        Load a text file.
        Args:
            input_path (str): Input file path.

        Returns:
            text (str): File content convert to string.

        """
        with open(input_path, "r", encoding="utf-8") as file:
            text = file.read().replace('"', "'").replace("\n", " ")
        return text

    def generate_graph(self, output_path):
        """
        Generate and save the graph in HTML format.
        Args:
            output_path (str): Path to save the graph in HTML format.

        Returns:

        """
        # Get coref resolved text and list of characters
        cr = CorefResolution(self.text)
        self._resolved_text = cr.get_resolved_doc()
        self._characters = cr.characters

        # Compute the Interaction Matrix
        im = InteractionMatrix(cr.doc, self._resolved_text, self._characters)
        self._im_df = im.get_interaction_matrix()

        # Generate and save the final Graph
        gg = GraphGenerator(self._im_df)
        gg.generate_graph_viz(output_path)

    def get_coref_resolution(self):
        """
        Get coref resolved text and detected characters.
        Returns:
            self._resolved_text (str): Coreference resolved text.
            self._characters list[str]: Characters detected in the text.
        """
        return self._resolved_text, self._characters

    def get_interaction_matrix(self):
        """
        Get the Interaction Matrix.
        Returns:
            self._im_df (pd.DataFrame): A DataFrame where the rows and columns represent characters, and each cell
                contains a score indicating the relationship between the characters.
                Values range from -1 (bad relationship) to +1 (good relationship).
        """
        return self._im_df
