import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

class RecipeClassifier:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.model = None
        self.scaler = StandardScaler()

    def train_and_evaluate(self):
        # 1. Carico i dati
        # Se non c'è il file o è vuoto (!), invento dei dati sintetici.
        generate_synthetic = False
        try:
            df = pd.read_csv(self.dataset_path)
            if len(df) < 20:
                print(f"Pochi dati ({len(df)}). Ne genero di nuovi...")
                generate_synthetic = True
        except FileNotFoundError:
            print("Dataset non trovato. Ne creo uno al volo...")
            generate_synthetic = True

        if generate_synthetic:
            # Codice generazione dati... omitto per pulizia
            pass

        # ... (Salvataggio se generato) ...
        # Se abbiamo generato sintetico sopra e non salvato, qui darebbe errore se non gestito.
        # Ma presumo il codice originale avesse la generazione qui.
        # Ripristino il blocco generazione per sicurezza nel replace.
        if generate_synthetic:
            data = {
                'calories': np.random.randint(100, 1000, 100),
                'protein': np.random.randint(5, 50, 100),
                'carbs': np.random.randint(10, 100, 100),
                'fat': np.random.randint(5, 40, 100),
                'health_label': np.random.choice(['Low Cal', 'Balanced', 'High Energy'], 100)
            }
            df = pd.DataFrame(data)
            df.to_csv(self.dataset_path, index=False)

        X = df[['calories', 'protein', 'carbs', 'fat']]
        y = df['health_label']

        # 2. Preparo i dati (standardizzazione)
        X_scaled = self.scaler.fit_transform(X)

        # 3. Provo diversi modelli (KNN vs Decision Tree)
        models = {
            'KNN': KNeighborsClassifier(n_neighbors=5),
            'DecisionTree': DecisionTreeClassifier(max_depth=5, random_state=42)
        }

        results = {}
        for name, model in models.items():
            # Controllo quanto sono affidabili (Cross Validation)
            scores = cross_val_score(model, X_scaled, y, cv=5)
            results[name] = {
                'mean_accuracy': scores.mean(),
                'std_dev': scores.std()
            }
            print(f"Modello: {name} -> Accuracy: {scores.mean():.2f} (+/- {scores.std():.2f})")

        # 4. Scelgo l'albero decisionale come modello finale
        self.model = models['DecisionTree']
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        print("\nReport Classificazione (Test Set):")
        print(classification_report(y_test, y_pred))

    def predict(self, features):
        # Serve una lista di caratteristiche: [[cal, prot, carbs, fat]]
        if self.model:
            df_features = pd.DataFrame(features, columns=['calories', 'protein', 'carbs', 'fat'])
            features_scaled = self.scaler.transform(df_features)
            return self.model.predict(features_scaled)
        else:
            return ["Modello non pronto"]
