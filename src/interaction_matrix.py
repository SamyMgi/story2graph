import pandas as pd

characters = ["Batman", "Joker", "Robin", "Catwoman", "Poison Ivy"]
text = "Batman & Robin fought the Joker. While Robing was fighting the Joker, Batman rescued Catwoman. Batman and Catwoman teamed-up against Poison Ivy."

dict_text = {0: {"sent": "Batman & Robin fought the Joker.", "char": ["Batman", "Robin", "Joker"]},
             1: {"sent": "While Robing was fighting the Joker, Batman rescued Catwoman.",
                 "char": ["Robin", "Joker", "Batman", "Catwoman"]},
             2: {"sent": "Batman and Catwoman teamed-up against Poison Ivy.",
                 "char": ["Batman", "Catwoman", "Poison Ivy"]}}

print(characters)

df = pd.DataFrame(0, index=characters, columns=characters)

print(df)
