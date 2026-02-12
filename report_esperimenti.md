# Report Esperimenti Machine Learning

Dataset: 600 istanze (Bilanciato). Features: [Calories, Protein, Carbs, Fat]. Target: 'health_label'.

Metodologia: Nested Cross-Validation (Outer: 5-Fold, Inner: 3-Fold GridSearch).

## Modello: DecisionTree
- **Accuratezza Media**: 0.963
- **F1-Score Macro Medio**: 0.963 (+/- 0.017)
- **Precision Macro**: 0.965
- **Recall Macro**: 0.963

## Modello: KNN
- **Accuratezza Media**: 0.955
- **F1-Score Macro Medio**: 0.955 (+/- 0.012)
- **Precision Macro**: 0.956
- **Recall Macro**: 0.955

## Conclusioni
Il modello selezionato è **DecisionTree** con i seguenti parametri ottimi (trovati su tutto il dataset):
```json
{'criterion': 'entropy', 'max_depth': 5, 'min_samples_split': 2}
```