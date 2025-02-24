import spacy #NER

# Opening the file
with open("../data/small_sample.txt", "r") as file:
    sample = file.read().replace('"', "'")

print(sample)


class EntityExtractor:
    def __init__(self, text, model="en_core_web_trf"):
        self.nlp = spacy.load(model)
        self.doc = self.nlp(text)

    def get_characters(self):
        characters = [ent.text for ent in self.doc.ents if ent.label_ == "PERSON"]
        return set(characters)

    def get_places(self):
        pass

    def get_objects(self):
        pass

    def get_organizations(self):
        pass

se = EntityExtractor(sample)
#print(se.get_characters())
