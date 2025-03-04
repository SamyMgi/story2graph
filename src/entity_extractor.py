import spacy


class EntityExtractor:
    def __init__(self, model="en_core_web_trf"):
        self.nlp = spacy.load(model)
        self.doc = None

    def set_text(self, text):
        self.doc = self.nlp(text)

    def get_person(self):
        person = set([ent.text for ent in self.doc.ents if ent.label_ == "PERSON"])
        person_custom = set()
        for pers in person:
            person_custom.add(pers.split("'s")[0]) if "'s" in pers else person_custom.add(pers)
        return person_custom

    def get_verbs(self):
        verbs = [token.text for token in self.doc if token.pos_ == "VERB"]
        return verbs
