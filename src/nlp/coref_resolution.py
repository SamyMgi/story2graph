import spacy
import re
from fastcoref import spacy_component


class CorefResolution:
    def __init__(self, text, task="coref", model="en_core_web_trf"):
        """
        Performs CorefResolution and NER tasks.
        Args:
            text (str): Text to be coref resolved.
            task (str): Task to be performed ('coref', 'NER').
                Default: 'coref'.
            model (str, optional): Model to be used for Coref resolution and NER.
                Default: Spacy transformers.
        """
        # Coref resolution needs less components when loading the model
        self.nlp = spacy.load(model, exclude=["lemmatizer", "ner", "textcat"])
        self.nlp.add_pipe("fastcoref")
        # Simple load, mostly for NER
        self.nlp_ner = spacy.load(model)
        self.characters = None
        self.doc = None
        self.text = text

    def get_person(self, text):
        """
        Get entities detected as person in the text.
        Args:
            text: Text to be used for NER.

        Returns:
            person (list[str]): List of entities detected as person by NER.
        """
        ner_doc = self.nlp_ner(text)
        person = [ent.text for ent in ner_doc.ents if ent.label_ == "PERSON"]
        return person

    # Improve the first coref resolution
    def _coref_correction(self):
        """
        Improves the first coref resolved text and the NER list of characters.
        Updates the original text by unifying all aliases into one common name.

        Returns:
            improved_resolution (str): Improved coref resolved text.

        """
        # First NER to get characters
        self.characters = self.get_person(self.text)
        # First version of the coref resolved text
        self.doc = self.nlp(self.text, component_cfg={"fastcoref": {'resolve_text': True}})
        resolved_text = self.doc._.resolved_text

        improved_resolution = resolved_text
        improved_characters = set()
        clusters = self.doc._.coref_clusters
        replacement_history = []
        print("All characters :", self.characters)
        # Characters only quote one time are not considered by the coref clusters
        char_out_coref = set(self.characters)
        # Parsing coref clusters to identify same entities with multiple aliases.=
        for cluster in clusters:
            names = [self.text[start:end] for start, end in cluster]
            print("All aliases :", names)
            main_name = {name for name in self.characters if name in names}
            # Removing names considered in coref clusters
            char_out_coref = char_out_coref - main_name
            main_name = list(main_name)
            print("All name of the character:", main_name)
            # Create a common name for all aliases
            full_main_name = "_".join(main_name)
            # The first element is the alias used by the coref model
            coref_name = names[0]
            print("Coref nam:", coref_name)
            # Replacing the name used by the coref model with the common name
            for replacement in replacement_history:
                coref_name = re.sub(rf"\b{re.escape(replacement[0])}\b(?!\w)", replacement[1], coref_name)
            print("After replacement:", coref_name)
            # If the name was detected by the NER
            if main_name:
                # Now considering only one alias for better NER performances
                full_main_name = full_main_name.split("_")[0]
                # Removing special characters for better NER performances
                full_main_name = re.sub(r"[^a-zA-Zàâäéèêëîïôöùûüÿç0-9]", "", full_main_name)
                improved_characters.add(full_main_name)
                # Replacing the common name by a simpler name
                improved_resolution = re.sub(rf"\b{re.escape(coref_name)}\b(?!\w)", full_main_name, improved_resolution)
                # Tracking replacement
                replacement_history.append((coref_name, full_main_name))

                # Replacing all aliases by the common selected name in the resolved text
                for alias in main_name:
                    if alias != full_main_name:
                        improved_resolution = re.sub(rf"\b{re.escape(alias)}\b(?!\w)", full_main_name,
                                                     improved_resolution)
                        replacement_history.append((alias, full_main_name))
                print("Name used by FCoref :", names[0], "->", coref_name)
                print("Replaced by :", main_name, "->", full_main_name)
            print("------------")
        # Adding the characters only quote one time (not in coref clusters)
        self.characters = improved_characters.union(char_out_coref)
        print(self.characters)
        print("HISTORY:", replacement_history)

        # Update the original text with unified names
        for replacement in replacement_history:
            self.text = re.sub(rf"\b{re.escape(replacement[0])}\b(?!\w)", replacement[1], self.text)

        return improved_resolution

    # Get the nlp improved resolution object
    def get_resolved_doc(self):
        """
        Get the coref resolved doc.
        Returns:
            Improved coref resolution (spacy.Doc).
        """
        return self.nlp(self._coref_correction())

    def get_resolved_text(self):
        """
        Get the coref resolved text.
        Returns:
            Improved coref resolution (str).
        """
        return self._coref_correction()
