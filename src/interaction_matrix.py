import pandas as pd
from transformers import pipeline
from entity_extractor import EntityExtractor


class InteractionMatrix:
    def __init__(self, original_doc, resolved_doc, entities, model="facebook/bart-large-mnli"):
        self.original_doc = original_doc
        self.resolved_doc = resolved_doc
        self.model = model
        self.entities = set(entities)

    def set_doc(self, original_doc, resolved_doc):
        self.resolved_doc = resolved_doc
        self.original_doc = original_doc

    # Get dict associating groups of sentences to their involved character.
    # Ex : {sentence -> "A was talking to B.", characters involved -> ["A", "B"]}
    def get_relation_dict(self):
        relations = {}
        sent_index = 0
        par_index = -1
        ee = EntityExtractor()
        previous_person = []
        original_sents = list(self.original_doc.sents)

        print("\n-----INTERACTION MATRIX-----\n")
        for sent in self.resolved_doc.sents:
            print("Original ver:", original_sents[sent_index].text)
            print("Resolved ver:", sent.text, "\n")
            ee.set_text(sent.text)
            person = set(ee.get_person())
            improved_person = set()
            for pers in person:
                if pers not in self.entities:
                    char = pers.split(" ")
                    for split_char in char:
                        if split_char in self.entities:
                            improved_person.add(split_char)
                else:
                    improved_person.add(pers)

            # self.entities = self.entities.union(person)

            if len(person) > 1:
                if improved_person == previous_person:
                    relations[par_index]["sent"] += original_sents[sent_index].text
                else:
                    par_index += 1
                    relations[par_index] = {}
                    relations[par_index]["sent"], relations[par_index]["char"] = original_sents[sent_index].text, list(
                        improved_person)

            sent_index += 1
            previous_person = improved_person

        return relations

    def get_interaction_matrix(self, relations):
        data = {char_1: {char_2: [] for char_2 in self.entities} for char_1 in self.entities}

        df = pd.DataFrame(data)

        relation_extraction = pipeline("zero-shot-classification", model=self.model)

        for part in relations.values():
            sent = part["sent"]
            chars = part["char"]
            print("Sentence :", sent)
            print("Involved :", chars)
            pairs = [[chars[i], chars[j]] for i in range(len(chars)) for j in range(i + 1, len(chars))]

            for cand in pairs:
                cand_labels = [f"{cand[0]} and {cand[1]} are allies", f"{cand[0]} and {cand[1]} are enemies"]
                output = relation_extraction(sent, candidate_labels=cand_labels)
                # print(output)
                relationship = 1 if "allies" in output["labels"][0] else -1
                df[cand[0]][cand[1]].append(relationship)
                df[cand[1]][cand[0]].append(relationship)
                print(cand_labels, " = ", relationship, "\n")

        df = df.applymap(lambda cell: 0 if len(cell) == 0 else sum(cell) / len(cell))

        print(df)
