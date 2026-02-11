# Report Esperimenti Machine Learning

Dataset: 600 istanze sintetiche. Features: [Calories, Protein, Carbs, Fat]. Target: 'health_label'.

Metodologia: Nested Cross-Validation (Outer: 5-Fold, Inner: 3-Fold GridSearch).

## Modello: DecisionTree
- **Accuratezza Media**: 0.995
- **F1-Score Macro Medio**: 0.938 (+/- 0.082)
- **Precision Macro**: 0.938
- **Recall Macro**: 0.939

## Modello: KNN
- **Accuratezza Media**: 0.923
- **F1-Score Macro Medio**: 0.884 (+/- 0.086)
- **Precision Macro**: 0.898
- **Recall Macro**: 0.877

## Conclusioni
Il modello selezionato è **DecisionTree** con i seguenti parametri ottimi (trovati su tutto il dataset):
```json
{'criterion': 'gini', 'max_depth': 8, 'min_samples_split': 2}
```