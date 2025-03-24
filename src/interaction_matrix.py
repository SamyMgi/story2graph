import numpy as np
import pandas as pd
from transformers import pipeline
from coref_resolution import CorefResolution


class InteractionMatrix:
    def __init__(self, original_doc, resolved_doc, characters, model="facebook/bart-large-mnli"):
        """
        Generate Interaction Matrix to analyze relationship between characters using Zero-Shot Learning.

            original_doc (spacy.Doc): Original text.
            resolved_doc (spacy.Doc): Coref Resolved text.
            characters (list[str]): Characters list.
            model (str): Model used for Zero-Shot Learning (BART by default).
        """
        self.original_doc = original_doc
        self.resolved_doc = resolved_doc
        self.model = model
        self.characters = set(characters)

    def _get_relation_dict(self):
        """
        Create a dictionary mapping each sentences to their involved characters.

        Returns: A dictionary where each key is a sentence index (int), and the value
                  is another dictionary containing:
                  - "sentence" (str): The original sentence.
                  - "characters" (list[str]): The characters involved in the sentence.
                Ex : {0: {sentence -> "A was talking to B.", characters involved -> ["A", "B"]}, ...}

        """
        relations = {}
        sent_index = 0
        par_index = -1
        # CorefResolution only used for NER task
        cr = CorefResolution([], task="NER")
        previous_person = []
        original_sents = list(self.original_doc.sents)
        resolved_sents = list(self.resolved_doc.sents)

        original_sents = [sent.text for sent in original_sents if (sent.text and not sent.text.isspace())]
        resolved_sents = [sent.text for sent in resolved_sents if (sent.text and not sent.text.isspace())]

        print("\n-----INTERACTION MATRIX-----\n")

        # Need to check same length for both texts
        for sent in resolved_sents:
            print("Original ver:", original_sents[sent_index])
            print("Resolved ver:", sent, "\n")
            person = set(cr.get_person(sent))
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

            if len(improved_person) > 1:
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
    def get_interaction_matrix(self):
        """
        Generates the Interaction Matrix using Zero-Shot Learning.
        The matrix will have dimensions n x n, where n is the number of unique characters.
        Each element quantifies the nature of the relationship between the corresponding characters,
        with values between -1 and +1, indicating negative or positive relationships respectively.

        Returns: A DataFrame (pd.DataFrame) where the rows and columns represent characters, and each cell
                contains a score indicating the relationship between the characters.
                Values range from -1 (bad relationship) to +1 (good relationship).
        """
        relation_dict = self._get_relation_dict()
        data = {char_1: {char_2: [] for char_2 in self.characters} for char_1 in self.characters}

        df = pd.DataFrame(data)

        relation_extraction = pipeline("zero-shot-classification", model=self.model)

        for part in relation_dict.values():
            sent = part["sent"]
            chars = part["char"]
            print("Sentence :", sent)
            print("Involved :", chars)
            pairs = [[chars[i], chars[j]] for i in range(len(chars)) for j in range(i + 1, len(chars))]

            for cand in pairs:
                cand_labels = [f"{cand[0]} and {cand[1]} are allies", f"{cand[0]} and {cand[1]} are enemies"]
                output = relation_extraction(sent, candidate_labels=cand_labels)
                # print(output)
                if "allies" in output["labels"][0]:
                    relationship = 1
                elif "enemies" in output["labels"][0]:
                    relationship = -1
                else:
                    relationship = 0
                # relationship = 1 if "allies" in output["labels"][0] else -1
                # score = relationship * output["scores"][0]
                score = relationship
                if score != 0:
                    df[cand[0]][cand[1]].append(score)
                    df[cand[1]][cand[0]].append(score)
                print(cand_labels, " = ", score, "\n")

        df = df.apply(lambda column: column.map(lambda cell: np.nan if len(cell) == 0 else sum(cell) / len(cell)))

        print(df)
        return df
