import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV, cross_validate
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, make_scorer, f1_score

class RecipeClassifier:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()

    def _generate_realistic_data(self, n_samples=600):
        """Genera dataset sintetico controllato BILANCIATO per il training."""
        np.random.seed(42)
        data = []
        labels = []

        # Target: ~120 samples per class (5 classes)
        samples_per_class = n_samples // 5

        # Generazione guidata per classe per garantire il bilanciamento
        classes_definitions = {
            'Low Cal': {'cal': (150, 300), 'prot': (5, 20), 'fat': (0, 10)},
            'High Protein': {'cal': (300, 600), 'prot': (30, 60), 'fat': (5, 20)},
            'Low Fat': {'cal': (200, 500), 'prot': (10, 30), 'fat': (0, 5)},
            'High Energy': {'cal': (700, 1000), 'prot': (15, 30), 'fat': (20, 45)},
            'Balanced': {'cal': (400, 700), 'prot': (15, 25), 'fat': (10, 20)}
        }

        for label, ranges in classes_definitions.items():
            for _ in range(samples_per_class):
                # Genera features conformi alla definizione
                calories = np.random.randint(ranges['cal'][0], ranges['cal'][1])
                protein = np.random.randint(ranges['prot'][0], ranges['prot'][1])
                fat = np.random.randint(ranges['fat'][0], ranges['fat'][1])

                # Calcola carbs residui
                remaining_cal = calories - (protein * 4 + fat * 9)
                carbs = max(0, int(remaining_cal / 4))
                # Add noise
                carbs += np.random.randint(-5, 5)

                data.append([calories, protein, carbs, fat])
                labels.append(label)

        df = pd.DataFrame(data, columns=['calories', 'protein', 'carbs', 'fat'])
        df['health_label'] = labels
        # Shuffle finale
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        return df

    def train_and_evaluate(self):
        print("--- Avvio Procedura di Training e Validazione ---")

        # 1. Gestione Dataset
        if not os.path.exists(self.dataset_path):
            print(f"Dataset non trovato. Genero {600} istanze realistiche...")
            df = self._generate_realistic_data(600)
            df.to_csv(self.dataset_path, index=False)
        else:
            df = pd.read_csv(self.dataset_path)
            # Verifica Bilanciamento
            print("\nDistribuzione Classi (Dataset):")
            print(df['health_label'].value_counts())

            if len(df) < 500:
                print(f"Dataset insufficiente ({len(df)} righe). Rigenerazione dataset esteso (600 righe).")
                df = self._generate_realistic_data(600)
                df.to_csv(self.dataset_path, index=False)

        # 2. Preprocessing
        X = df[['calories', 'protein', 'carbs', 'fat']]
        y = df['health_label']

        X_scaled = self.scaler.fit_transform(X)
        # Encoding labels per scikit-learn (opzionale ma consigliato)
        y_encoded = self.label_encoder.fit_transform(y)

        # 3. Disegno Sperimentale: Nested Cross-Validation
        # Outer Loop: Valutazione Performance (Stratified 5-Fold)
        # Inner Loop: Model Selection / Tuning (GridSearch 3-Fold)

        outer_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        inner_cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

        # Griglie Iperparametri
        dt_params = {
            'max_depth': [3, 5, 8, 12, None],
            'min_samples_split': [2, 5, 10],
            'criterion': ['gini', 'entropy']
        }

        knn_params = {
            'n_neighbors': [3, 5, 7, 9, 11, 15],
            'weights': ['uniform', 'distance'],
            'metric': ['euclidean', 'manhattan']
        }

        models = {
            'DecisionTree': GridSearchCV(DecisionTreeClassifier(random_state=42), dt_params, cv=inner_cv, scoring='f1_macro'),
            'KNN': GridSearchCV(KNeighborsClassifier(), knn_params, cv=inner_cv, scoring='f1_macro')
        }

        report_lines = ["# Report Esperimenti Machine Learning\n"]
        report_lines.append(f"Dataset: {len(df)} istanze (Bilanciato). Features: [Calories, Protein, Carbs, Fat]. Target: 'health_label'.\n")
        report_lines.append("Metodologia: Nested Cross-Validation (Outer: 5-Fold, Inner: 3-Fold GridSearch).\n")

        best_overall_model = None
        best_overall_score = -1
        best_name = ""

        print("\nEsecuzione Nested Cross-Validation...")

        for name, grid_clf in models.items():
            # cross_validate per ottenere metriche multiple sull'Outer Loop
            scoring_metrics = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']
            cv_results = cross_validate(grid_clf, X_scaled, y_encoded, cv=outer_cv, scoring=scoring_metrics)

            mean_acc = cv_results['test_accuracy'].mean()
            mean_f1 = cv_results['test_f1_macro'].mean()
            std_f1 = cv_results['test_f1_macro'].std()

            print(f"Modello {name} -> F1 Macro: {mean_f1:.3f} (+/- {std_f1:.3f}) | Accuracy: {mean_acc:.3f}")

            report_lines.append(f"## Modello: {name}")
            report_lines.append(f"- **Accuratezza Media**: {mean_acc:.3f}")
            report_lines.append(f"- **F1-Score Macro Medio**: {mean_f1:.3f} (+/- {std_f1:.3f})")
            report_lines.append(f"- **Precision Macro**: {cv_results['test_precision_macro'].mean():.3f}")
            report_lines.append(f"- **Recall Macro**: {cv_results['test_recall_macro'].mean():.3f}\n")

            if mean_f1 > best_overall_score:
                best_overall_score = mean_f1
                best_overall_model = grid_clf # Questo è un GridSearchCV object
                best_name = name

        # 4. Training Finale sul Modello Migliore
        # Addestriamo il GridSearch su tutto il dataset per trovare i parametri ottimi finali
        print(f"\nTraining finale modello scelto ({best_name}) su tutto il dataset...")
        best_overall_model.fit(X_scaled, y_encoded)

        self.model = best_overall_model.best_estimator_
        best_params = best_overall_model.best_params_
        print(f"Migliori Parametri Trovati: {best_params}")

        report_lines.append(f"## Conclusioni")
        report_lines.append(f"Il modello selezionato è **{best_name}** con i seguenti parametri ottimi (trovati su tutto il dataset):")
        report_lines.append(f"```json\n{best_params}\n```")

        # Scrittura Report
        with open("report_esperimenti.md", "w") as f:
            f.writelines("\n".join(report_lines))
        print("Report salvato in 'report_esperimenti.md'.")

    def predict(self, features):
        if self.model:
            df_features = pd.DataFrame(features, columns=['calories', 'protein', 'carbs', 'fat'])
            features_scaled = self.scaler.transform(df_features)
            pred_encoded = self.model.predict(features_scaled)
            return self.label_encoder.inverse_transform(pred_encoded)
        else:
            return ["Modello non pronto"]

if __name__ == '__main__':
    # Cancella il vecchio dataset se esiste per forzare la rigenerazione bilanciata
    if os.path.exists('dataset.csv'):
        os.remove('dataset.csv')

    classifier = RecipeClassifier('dataset.csv')
    classifier.train_and_evaluate()
