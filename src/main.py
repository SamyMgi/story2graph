from entity_extractor import EntityExtractor
from fastcoref import spacy_component
import spacy
from transformers import pipeline
import pandas as pd
from coref_resolution import CorefResolution
from interaction_matrix import InteractionMatrix

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Opening the file
with open("../data/small_sample.txt", "r", encoding="utf-8") as file:
    sample = file.read().replace('"', "'").replace("\n", " ")

print(sample)

cr = CorefResolution()
cr.set_text(sample)

resolved_text = cr.get_resolved_doc()

im = InteractionMatrix(resolved_text)
relation_dict = im.get_relation_dict()

for val in relation_dict.values():
    print(val)

print(im.entities)