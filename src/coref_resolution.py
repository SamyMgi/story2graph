import spacy
from fastcoref import spacy_component


class CorefResolution:
    def __init__(self, model="en_core_web_trf"):
        self.nlp = spacy.load(model)
        self.nlp.add_pipe("fastcoref")
        self.doc = None

    # Set text to be coref resolved
    def set_text(self, text):
        self.doc = self.nlp(text, component_cfg={"fastcoref": {'resolve_text': True}})

    # Get the nlp resolved object
    def get_resolved_doc(self):
        return self.nlp(self.doc._.resolved_text)

    # Get the str resolved object
    def get_resolved_text(self):
        return self.doc._.resolved_text
