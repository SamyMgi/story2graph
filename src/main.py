import pandas as pd
from coref_resolution import CorefResolution
from interaction_matrix import InteractionMatrix
from graph_generator import GraphGenerator

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Opening the file
with open("../data/cp_episode.txt", "r", encoding="utf-8") as file:
    sample = file.read().replace('"', "'").replace("\n", " ")

print(sample)

cr = CorefResolution(sample)

resolved_text = cr.get_resolved_doc()
resolved_characters = cr.characters

print("Characters after processing :", resolved_characters)
print("Text after processing :", resolved_text)

im = InteractionMatrix(cr.doc, resolved_text, resolved_characters)

print(im.characters)

im_df = im.get_interaction_matrix()

gg = GraphGenerator(im_df)

gg.generate_graph_viz("../data/test")