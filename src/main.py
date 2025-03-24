from entity_extractor import EntityExtractor
import pandas as pd
from coref_resolution import CorefResolution
from interaction_matrix import InteractionMatrix
from graph_generator import GraphGenerator

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Opening the file
with open("../data/sw3.txt", "r", encoding="utf-8") as file:
    sample = file.read().replace('"', "'").replace("\n", " ")

print(sample)

ee = EntityExtractor()
ee.set_text(sample)
characters = ee.get_person()

cr = CorefResolution(characters)
cr.set_text(sample)

resolved_text = cr.get_resolved_doc()
resolved_characters = cr.characters

print("Characters after processing :", resolved_characters)
print("Text after processing :", resolved_text)

im = InteractionMatrix(cr.doc, resolved_text, resolved_characters)

print(im.characters)

im_df = im.get_interaction_matrix()

gg = GraphGenerator(im_df)

gg.generate_graph_viz("../data/test")