from entity_extractor import EntityExtractor
from fastcoref import spacy_component

# Opening the file
with open("../data/small_sample.txt", "r") as file:
    sample = file.read().replace('"', "'")

print(sample)

ee = EntityExtractor()

"""
self.nlp.add_pipe("fastcoref")
self.doc = self.nlp(text, component_cfg={"fastcoref": {'resolve_text': True}})
relations = {}
index = 0
resolved_doc = self.nlp(self.doc._.resolved_text)
for sent in resolved_doc.sents:
    relations[index]["sent"], relations[index]["char"] = self.get_characters()
    relations[index]
"""
