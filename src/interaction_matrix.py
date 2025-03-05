import pandas as pd
from transformers import pipeline
from entity_extractor import EntityExtractor


class InteractionMatrix:
    def __init__(self, doc, model="facebook/bart-large-mnli"):
        self.doc = doc
        self.model = model
        self.entities = set()

    def set_doc(self, doc):
        self.doc = doc

    # Get dict associating groups of sentences to their implied character.
    # Ex : "A was talking to B." -> ["A", "B"]
    def get_relation_dict(self):
        relations = {}
        sent_index = 0
        par_index = -1
        ee = EntityExtractor()
        previous_person = []

        for sent in self.doc.sents:
            ee.set_text(sent.text)
            person = ee.get_person()
            self.entities = self.entities.union(person)
            if len(person) > 1:
                if person == previous_person:
                    relations[par_index]["sent"] += sent[sent_index].text
                else:
                    par_index += 1
                    relations[par_index] = {}
                    relations[par_index]["sent"], relations[par_index]["char"] = sent.text, list(person)

            sent_index += 1
            previous_person = set(person)

        return relations

    def get_interaction_matrix(self):
        relation_extraction = pipeline("zero-shot-classification", model=self.model)
        """
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
