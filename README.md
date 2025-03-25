# character-graph

Turning **stories** into interactive **graphs** with characters as nodes and relationships as edges.

| Input                                          | Output |
|------------------------------------------------|--------|
| _"At his workplace, Neo is pursued by police and Agents led by Agent Smith. Morpheus guides Neo's escape by phone, able to somehow remotely observe their movements, but Neo ultimately surrenders rather than risk a hazardous getaway."_ | Output |


## ✅ Current state :
1. Detect characters (**NER**)
2. Preprocessing (**Coreference Resolution**)
3. **Improving NER** and **CR** with some tricks
4. Get each character associated to each sentence (group of sentences for optimization)
5. **Matrix of interaction** between characters: Each pairs of characters get a value with **Zero-Shot Learning** based on their interactions.
6. Matrix converted to **interactive Graph**
7. Graph can be **saved** to .html

---

## How it works ?

---

## How to use it ?

### Clone this repository
```bash
git clone https://github.com/SamyMgi/...
```

### Install the dependencies
```bash
pip install -r requirements.txt
```
### Example of usage

```python
  # Import the class
```