# NutriLogic

NutriLogic è un Sistema Intelligente per la pianificazione pasto personalizzata che integra:
1.  **Knowledge Base (Prolog)**: Gestisce regole dietetiche, allergie e conoscenza degli ingredienti (Programmazione Logica).
2.  **Machine Learning (Scikit-learn)**: Classifica le ricette in base al contenuto nutrizionale (Apprendimento Supervisionato).
3.  **Constraint Satisfaction Problem (CSP)**: Genera piani alimentari giornalieri ottimali che soddisfano i vincoli dell'utente.

## Componenti del Sistema

### 1. Knowledge Base (`knowledge_base.pl`)
-   **Paradigma**: Programmazione Logica (Clausole di Horn).
-   **Funzionalità**:
    -   Ragionamento su esigenze dietetiche specifiche (es. `safe_for(Recipe, lactose)`).
    -   Inferenza sulle proprietà degli ingredienti (es. `is_vegan/1`).
    -   Regole avanzate per Stagionalità e composizione del Piatto Completo.

### 2. Machine Learning (`ml_classifier.py`)
-   **Obiettivo**: Classificare le ricette in categorie salutari (`Bilanciato`, `Alto Proteico`, `Basse Calorie`, ecc.).
-   **Metodologia**:
    -   **Dataset**: 600+ istanze sintetiche realistiche.
    -   **Valutazione**: Nested Cross-Validation (Outer 5-Fold, Inner 3-Fold).
    -   **Metriche**: Accuracy, Precision, Recall, F1-Score.

### 3. Pianificatore di Diete (`csp_planner.py`)
-   **Paradigma**: Programmazione a Vincoli (Constraint Programming).
-   **Solver**: `python-constraint` (Backtracking con Forward Checking/Arc Consistency) vs Backtracking Custom.

#### Definizione Formale CSP
Il problema della pianificazione dei pasti è modellato come una tupla CSP $<V, D, C>$:

*   **Variabili ($V$)**: L'insieme dei pasti da assegnare.
    *   $V = \{M_1, M_2, \dots, M_k\}$ dove $k$ è il numero di pasti (es. Colazione, Pranzo, Cena).
*   **Domini ($D$)**: L'insieme delle ricette valide per ogni variabile.
    *   $D(v_i) \subseteq \{r \in \text{Ricette} \mid r.\text{tipo} = \text{tipo}(v_i) \land \text{sicuro\_per}(r, \text{intolleranze\_utente})\}$
*   **Vincoli ($C$)**:
    *   **Vincoli Hard** (Devono essere ottimizzati/soddisfatti):
        -   **Vincolo Calorico Globale**: $| \sum_{v \in V} \text{cal}(v) - \text{Target} | \le \text{Tolleranza}$
        -   **Vincolo di Varietà**: $\text{AllDifferent}(Pranzo, Cena)$
    *   **Vincoli Soft** (Modellati come preferenze o limiti ampi):
        -   Target nutrizionali (Min Proteine, Max Grassi).

## Come Eseguire
1.  **Installare le dipendenze**:
    ```bash
    pip install pandas numpy scikit-learn pyswip python-constraint
    ```
    *(Nota: `pyswip` richiede SWI-Prolog installato nel sistema).*

2.  **Eseguire il Sistema**:
    ```bash
    python main.py
    ```
    Questo comando:
    -   Addestrerà il modello ML (e salverà `report_esperimenti.md`).
    -   Caricherà la Knowledge Base Prolog (se disponibile).
    -   Eseguirà il CSP Planner e confronterà i solver.