import spacy


class EntityExtractor:
    def __init__(self, model="en_core_web_trf"):
        self.nlp = spacy.load(model)
        self.doc = None

    # Set text to extract
    def set_text(self, text):
        self.doc = self.nlp(text)

    # Get Person entities from the text
    def get_person(self):
        person = [ent.text for ent in self.doc.ents if ent.label_ == "PERSON"]
        return person

    # Get verbs from the text
    def get_verbs(self):
        verbs = [token.text for token in self.doc if token.pos_ == "VERB"]
        return verbs
