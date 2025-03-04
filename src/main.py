from entity_extractor import EntityExtractor
from fastcoref import spacy_component
import spacy
from transformers import pipeline
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Opening the file
with open("../data/small_sample.txt", "r", encoding="utf-8") as file:
    sample = file.read().replace('"', "'").replace("\n", " ")

print(sample)

ee = EntityExtractor()

#

relations = {}
sent_index = 0
par_index = -1

"""
    1) Get a first dictionary : {index: {original_sent: ..., characters_detection_after_coref: ...}, ...}
    Only keeping sentences involving 2 characters or more.
    2) Optimizing dict by grouping indexes when consecutive sentences involve the same characters to reduce future computations.
"""

nlp = spacy.load("en_core_web_lg")
nlp.add_pipe("fastcoref")
doc = nlp(sample, component_cfg={"fastcoref": {'resolve_text': True}})
resolved_doc = nlp(doc._.resolved_text)

ee.set_text(doc._.resolved_text)

characters = list(ee.get_person())
print(characters)

sent_list = list(doc.sents)

previous_person = set()

for resolved_sent in resolved_doc.sents:
    ee.set_text(resolved_sent.text)
    person = ee.get_person()

    if len(person) > 1:
        if person == previous_person:
            relations[par_index]["sent"] += sent_list[sent_index].text
        else:
            par_index += 1
            relations[par_index] = {}
            relations[par_index]["sent"], relations[par_index]["char"] = resolved_sent.text, list(person)

        # print(relations[par_index])
    sent_index += 1
    previous_person = set(person)

print(relations)

"""
    3) Parsing the dict and creating interaction matrix.
"""

data = {char_1: {char_2: [] for char_2 in characters} for char_1 in characters}

df = pd.DataFrame(data)

print(df)

relation_extraction = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

for part in relations.values():
    sent = part["sent"]
    chars = part["char"]
    pairs = [[chars[i], chars[j]] for i in range(len(chars)) for j in range(i + 1, len(chars))]

    for cand in pairs:
        cand_labels = [f"{cand[0]} and {cand[1]} are friends", f"{cand[0]} and {cand[1]} are enemies"]
        output = relation_extraction(sent, candidate_labels=cand_labels)
        # print(output)
        relationship = 1 if "friends" in output["labels"][0] else -1
        df[cand[0]][cand[1]].append(relationship)
        df[cand[1]][cand[0]].append(relationship)

df = df.applymap(lambda cell: 0 if len(cell) == 0 else sum(cell) / len(cell))

print(df)

"""
    4) Regrouping all the previous steps (1-3) in one class file interaction_matrix.
"""

"""
    5) Graph creation.
"""
