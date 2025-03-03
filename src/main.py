from entity_extractor import EntityExtractor
from fastcoref import spacy_component
import spacy

# Opening the file
with open("../data/small_sample.txt", "r", encoding="utf-8") as file:
    sample = file.read().replace('"', "'").replace("\n", " ")

print(sample)

ee = EntityExtractor()

ee.set_text(sample)
print(ee.get_person())
print(ee.get_verbs())

relations = {}
sent_index = 0
par_index = -1

"""
    1) Get a first dictionary : {index: {original_sent: ..., characters_detection_after_coref: ...}, ...}
    Only keeping sentences involving 2 characters or more.
"""

nlp = spacy.load("en_core_web_trf")
nlp.add_pipe("fastcoref")
doc = nlp(sample, component_cfg={"fastcoref": {'resolve_text': True}})
resolved_doc = nlp(doc._.resolved_text)

sent_list = list(doc.sents)

previous_person = set()
"""
print("Base length :", len(sent_list))
print("Resolved length :", len(list(resolved_doc.sents)))

for i in range(len(sent_list)):
    print(sent_list[i])
    print(list(resolved_doc.sents)[i], "\n")
"""

for resolved_sent in resolved_doc.sents:
    ee.set_text(resolved_sent.text)
    person = set(ee.get_person())
    if len(person) > 1:
        if person == previous_person:
            relations[par_index]["sent"] += sent_list[sent_index].text
        else:
            par_index += 1

            relations[par_index] = {}
            relations[par_index]["sent"], relations[par_index]["char"] = sent_list[sent_index].text, ee.get_person()

        print(relations[par_index])
    sent_index += 1
    previous_person = set(person)

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
