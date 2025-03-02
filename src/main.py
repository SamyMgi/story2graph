from entity_extractor import EntityExtractor
from fastcoref import spacy_component
import spacy

# Opening the file
with open("../data/small_sample.txt", "r") as file:
    sample = file.read().replace('"', "'")

print(sample)

ee = EntityExtractor()

ee.set_text(sample)
print(ee.get_person())
print(ee.get_verbs())

relations = {}
index = 0

"""
    1) Get a first dictionary : {index: {original_sent: ..., characters_detection_after_coref: ...}, ...}
    Only keeping sentences involving 2 characters or more.
"""

nlp = spacy.load("en_core_web_trf")
nlp.add_pipe("fastcoref")
doc = nlp(sample, component_cfg={"fastcoref": {'resolve_text': True}})
resolved_doc = nlp(doc._.resolved_text)

sent_list = list(doc.sents)

for resolved_sent in resolved_doc.sents:
    ee.set_text(resolved_sent.text)
    person = ee.get_person()
    if len(person) > 1:
        relations[index] = {}
        relations[index]["sent"], relations[index]["char"] = sent_list[index].text, ee.get_person()
    index += 1

print(relations)

"""
    2) Optimizing dict by grouping indexes when consecutive sentences involve the same characters to reduce future computations.
"""

"""
    3) Parsing the dict and creating interaction matrix.
"""

"""
    4) Regrouping all the previous steps (1-3) in one class file interaction_matrix.
"""

"""
    5) Graph creation.
"""