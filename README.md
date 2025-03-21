# character-graph

Turning **stories** into interactive **graphs** with characters as nodes and relationships as edges.

## ✅ Current state :
1. Detect characters and more -> **NER**
2. Preprocessing -> **Coreference Resolution**
3. Improving NER and CR with some tricks
4. Get each character associated to each sentence (group of sentences for optimization)
5. **Matrix of interaction** between characters.

## 🎯 TO-DO :
### Main
- Integrate EntityExtractor to CorefResolution
- Generate graph from Interaction Matrix
- JSON export for Interaction Matrix

### Secondary
- Convert the matrix into graph
- Evaluation
- Comments

## ⁉️ Thinking :
- Multiple identity accuracy
- Optimization