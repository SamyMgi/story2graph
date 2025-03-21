"""
    Returns an n x n Interaction Matrix (where n is the number of characters in the text).
    Each pair has a value between -1 and +1, with -1 indicating a bad relationship and +1 a good one.
"""

import pandas as pd
from transformers import pipeline
from entity_extractor import EntityExtractor


class InteractionMatrix:
    def __init__(self, original_doc, resolved_doc, characters, model="facebook/bart-large-mnli"):
        self.original_doc = original_doc
        self.resolved_doc = resolved_doc
        self.model = model
        self.characters = set(characters)

    # Set doc to be used for the Interaction Matrix using the original one and its coref resolution.
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
        resolved_sents = list(self.resolved_doc.sents)

        print("///////////////////////////////////////")
        print(len(original_sents), "sentences for the original.")
        print(len(resolved_sents), "sentences for the resolved.")
        print("/////////// BEFORE CORRECTION /////////////////")

        original_sents = [sent.text for sent in original_sents if (sent.text and not sent.text.isspace())]
        resolved_sents = [sent.text for sent in resolved_sents if (sent.text and not sent.text.isspace())]

        print("/////////// AFTER CORRECTION /////////////////")
        print(len(original_sents), "sentences for the original.")
        print(len(resolved_sents), "sentences for the resolved.")
        print("///////////////////////////////////////")

        print("\n-----INTERACTION MATRIX-----\n")

        # Need to check same length for both texts
        for sent in resolved_sents:
            print("Original ver:", original_sents[sent_index])
            print("Resolved ver:", sent, "\n")
            ee.set_text(sent)
            person = set(ee.get_person())
            print("Person on coref resolved :", person)
            improved_person = set()
            for pers in person:
                if pers not in self.characters:
                    char = pers.split(" ")
                    for split_char in char:
                        if split_char in self.characters:
                            improved_person.add(split_char)
                else:
                    improved_person.add(pers)

            if len(person) > 1:
                if improved_person == previous_person:
                    relations[par_index]["sent"] += original_sents[sent_index]
                else:
                    par_index += 1
                    relations[par_index] = {}
                    relations[par_index]["sent"], relations[par_index]["char"] = original_sents[sent_index], list(
                        improved_person)

            sent_index += 1
            previous_person = improved_person

        return relations

    # Get the Interaction Matrix.
    # Ex: ["Character A", "Character B"] = Value between -1 and 1
    # 1 (Good relationship) / -1 (Bad relationship)
    def get_interaction_matrix(self, relations):
        data = {char_1: {char_2: [] for char_2 in self.characters} for char_1 in self.characters}

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
