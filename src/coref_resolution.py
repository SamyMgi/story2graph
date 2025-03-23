"""
    Coreference Resolution using FCoref.
    Improved using a first character list extracted via NER and rules.
"""

import spacy
import re
from fastcoref import spacy_component


class CorefResolution:
    def __init__(self, characters, model="en_core_web_trf"):
        self.nlp = spacy.load(model, exclude=["lemmatizer", "ner", "textcat"])
        self.nlp.add_pipe("fastcoref")
        self.characters = characters
        self.doc = None
        self.text = None

    # Set text to be coref resolved
    def set_text(self, text):
        self.text = text
        self.doc = self.nlp(self.text, component_cfg={"fastcoref": {'resolve_text': True}})

    # Improve the first coref resolution
    def _coref_correction(self):
        resolved_text = self.doc._.resolved_text
        improved_resolution = resolved_text
        improved_characters = set()
        clusters = self.doc._.coref_clusters
        replacement_history = []
        print("All characters :", self.characters)
        for cluster in clusters:
            names = [self.text[start:end] for start, end in cluster]
            print(names)
            set_names = set(names)
            print("All aliases :", names)
            main_name = list({name for name in self.characters if name in names})
            full_main_name = "_".join(main_name)
            coref_name = names[0]
            for replacement in replacement_history:
                coref_name = re.sub(rf"\b{re.escape(replacement[0])}\b(?!\w)", replacement[1], coref_name)
            if main_name:
                #HERE
                full_main_name = full_main_name.split("_")[0]
                full_main_name = full_main_name.replace("-", "")
                improved_characters.add(full_main_name)
                improved_resolution = re.sub(rf"\b{re.escape(coref_name)}\b(?!\w)", full_main_name, improved_resolution)
                replacement_history.append((coref_name, full_main_name))
                for alias in main_name:
                    if alias != full_main_name:
                        improved_resolution = re.sub(rf"\b{re.escape(alias)}\b(?!\w)", full_main_name,
                                                     improved_resolution)
                        replacement_history.append((alias, full_main_name))
                print("Name used by FCoref :", names[0], "->", coref_name)
                print("Replaced by :", main_name, "->", full_main_name)
            print("------------")
        self.characters = improved_characters
        print(self.characters)
        print("HISTORY:", replacement_history)

        for replacement in replacement_history:
            self.text = re.sub(rf"\b{re.escape(replacement[0])}\b(?!\w)", replacement[1], self.text)

        self.set_text(self.text)
        return improved_resolution

    # Get the nlp improved resolution object
    def get_resolved_doc(self):
        return self.nlp(self._coref_correction())

    # Get the str improved resolution object
    def get_resolved_text(self):
        return self._coref_correction()
