# character-graph

Turning **stories** into interactive **graphs** with characters as nodes and relationships as edges.

## Current state :
1. Detect characters and more -> **NER**
2. Preprocessing -> **Coreference Resolution**
3. Get each characters associated with each sentences (group of sentences for optimization)

## TO-DO :
### Main
- Matrix of interactions
- Convert the matrix into graph

### Secondary
- Isolate principle algorithms into different files
- Unit tests
- Comments

## Thinking :
- Handle double characters identity
- The transformers model for NER shows difficulties with possessive "'s"