import pandas as pd
from ml_classifier import RecipeClassifier
from csp_planner import DietPlanner
import os

try:
    from pyswip import Prolog
except ImportError:
    Prolog = None
    print("ATTENZIONE: 'pyswip' non trovato. Il modulo Knowledge Base non sarà attivo.")
except Exception as e:
    Prolog = None
    print(f"ATTENZIONE: Errore inizializzazione 'pyswip' (SWI-Prolog mancante?): {e}. Il modulo Knowledge Base non sarà attivo.")

def main():
    print("=== NutriLogic System Started ===")

    # 1. Avvio il Machine Learning
    print("\n[ML Module] Training Classificatore Ricette...")
    dataset_path = 'dataset.csv'
    classifier = RecipeClassifier(dataset_path)
    classifier.train_and_evaluate()

    # Proviamo a classificare una ricetta (esempio)
    new_recipe = [500, 20, 60, 15] # Cal, Prot, Carb, Fat
    prediction = classifier.predict([new_recipe])
    print(f"Nuova ricetta classificata come: {prediction[0]}")

    # 2. Logica Prolog (Knowledge Base)
    print("\n[KB Module] Caricamento regole logiche...")
    if Prolog:
        prolog = Prolog()
        try:
            prolog.consult("knowledge_base.pl")
        except Exception as e:
            print(f"Errore caricamento KB: {e}")
    else:
        print("Skipping KB initialization because Prolog is not available.")

    user_intolerances = ['lactose'] # Esempio di input
    print(f"Utente intollerante a: {user_intolerances}")

    # Cerchiamo ricette sicure...
    safe_recipes = []
    # Qui useremmo safe_recipe(Name, intolerance) dal file Prolog

    # 3. Pianificazione Dieta (CSP)
    print("\n[CSP Module] Generazione Piano Alimentare...")
    planner = DietPlanner()

    # Quante calorie vogliamo oggi?
    target_calories = 1000

    # Risolviamo il problema
    plan = planner.solve(target_calories, user_intolerances)

    if plan:
        print("\n=== Piano Giornaliero Suggerito ===")
        for meal, recipe in plan.items():
            if not meal.startswith('_'):  # Ignora chiavi speciali
                print(f"{meal}: {recipe['name']} ({recipe['calories']} kcal)")

        if '_totals' in plan:
            print(f"\nTotale Calorie: {plan['_totals']['calories']}")
            print(f"Proteine: {plan['_totals']['protein']}g | Carboidrati: {plan['_totals']['carbs']}g | Grassi: {plan['_totals']['fat']}g | Fibre: {plan['_totals']['fiber']}g")
        else:
            total_cal = sum(r['calories'] for r in plan.values() if isinstance(r, dict) and 'calories' in r)
            print(f"Totale Calorie: {total_cal}")
    else:
        print("Nessuna soluzione trovata che soddisfi i vincoli.")

if __name__ == "__main__":
    main()
