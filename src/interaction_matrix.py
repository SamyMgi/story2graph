import pandas as pd
from transformers import pipeline

characters = ["Batman", "Joker", "Robin", "Catwoman", "Poison Ivy"]
text = "Batman and Robin fought the Joker. While Robing was fighting the Joker, Batman rescued Catwoman. Batman and Catwoman teamed-up against Poison Ivy."

dict_text = {0: {"sent": "Batman and Robin fought the Joker.", "char": ["Batman", "Robin", "Joker"]},
             1: {"sent": "While Robing was fighting the Joker, Batman rescued Catwoman.",
                 "char": ["Robin", "Joker", "Batman", "Catwoman"]},
             2: {"sent": "Batman and Catwoman teamed-up against Poison Ivy.",
                 "char": ["Batman", "Catwoman", "Poison Ivy"]}}

print(characters)

data = {char_1: {char_2: [] for char_2 in characters} for char_1 in characters}

df = pd.DataFrame(data)

print(df)

relation_extraction = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

for part in dict_text.values():
    sent = part["sent"]
    chars = part["char"]
    pairs = [[chars[i], chars[j]] for i in range(len(chars)) for j in range(i + 1, len(chars))]

    for cand in pairs:
        cand_labels = [f"{cand[0]} and {cand[1]} are friends", f"{cand[0]} and {cand[1]} are enemies"]
        output = relation_extraction(sent, candidate_labels=cand_labels)
        print(output)
        relationship = 1 if "friends" in output["labels"][0] else -1
        df[cand[0]][cand[1]].append(relationship)
        df[cand[1]][cand[0]].append(relationship)

print(df)

df = df.applymap(lambda cell: 0 if len(cell) == 0 else sum(cell) / len(cell))

print(df)
