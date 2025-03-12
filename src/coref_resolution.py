import spacy
from fastcoref import spacy_component

class CorefResolution:
    def __init__(self, characters, model="en_core_web_trf"):
        self.nlp = spacy.load(model)
        self.nlp.add_pipe("fastcoref")
        self.characters = characters
        self.doc = None
        self.text = None

    # Set text to be coref resolved
    def set_text(self, text):
        self.text = text
        self.doc = self.nlp(self.text, component_cfg={"fastcoref": {'resolve_text': True}})

    def _coref_correction(self):
        resolved_text = self.doc._.resolved_text
        improved_resolution = resolved_text
        clusters = self.doc._.coref_clusters
        for cluster in clusters:
            names = [self.text[start:end] for start, end in cluster]
            #print(names)
            set_names = set(names)
            #print("All characters :", self.characters)
            #print("All aliases :", set_names)
            main_name = next((name for name in self.characters if name in set_names), names[0])
            print("Name used by FCoref :", names[0])
            print("Replaced by :", main_name)
            improved_resolution = improved_resolution.replace(names[0], main_name)
        return improved_resolution



    # Get the nlp resolved object
    def get_resolved_doc(self):
        return self.nlp(self._coref_correction())

    # Get the str resolved object
    def get_resolved_text(self):
        return self.doc._.resolved_text, self._coref_correction()

with open("../data/small_sample.txt", "r", encoding="utf-8") as file:
    sample = file.read().replace('"', "'").replace("\n", " ")

characters = ['Kevin Flynn', 'Flynn', 'Clu', 'Zuse', 'Rinzler', 'Kevin', 'Quorra', 'Alan', 'Alan Bradley', 'Tron', 'Sam']

print("Original text :\n", sample)

cr = CorefResolution(characters)
cr.set_text(sample)

before_correction, after_correction = cr.get_resolved_text()

print("\nBefore correction :\n", before_correction)
print("\nAfter correction :\n", after_correction)