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

nlp = spacy.load("en_core_web_trf")
nlp.add_pipe("fastcoref")
doc = nlp(sample, component_cfg={"fastcoref": {'resolve_text': True}})
resolved_doc = nlp(doc._.resolved_text)

for sent in resolved_doc.sents:
    relations[index] = {}
    ee.set_text(sent.text)
    relations[index]["sent"], relations[index]["char"], relations[index][
        "verbs"] = sent.text, ee.get_person(), ee.get_verbs()
    index += 1

print(relations)
