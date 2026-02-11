# NutriLogic - Relazione Tecnica

## 1. Knowledge Base (Prolog)

La Knowledge Base (`knowledge_base.pl`) costituisce il cuore deduttivo del sistema. È stata progettata per modellare ingredienti, ricette, valori nutrizionali e regole dietetiche complesse.

### Struttura e Complessità
La base di conoscenza è organizzata in fatti e regole:
-   **Fatti**: Database degli ingredienti (~60 entità) con macro-categoria e calorie; Database delle ricette (~25 ricette) definite come liste di ingredienti; Fatti sulla stagionalità.
-   **Regole**: Implementano la logica di dominio. Le regole più significative includono controlli ricorsivi (calcolo calorie), iterazioni su liste (`is_seasonal`), e inferenza su proprietà composte (`complete_dish`).

Le regole utilizzano la logica di Horn per garantire decidibilità ed efficienza. La complessità computazionale per il controllo dei vincoli (es. `is_seasonal`) è lineare $O(N)$ rispetto al numero di ingredienti nella ricetta.

### Codice Sorgente Knowledge Base
Di seguito riportiamo il contenuto integrale della KB per mostrare l'estensione delle regole e dei fatti.

```prolog
% --- Knowledge Base NutriLogic ---

% --- 1. FATTI: Ingredienti ---
% ingredient(Name, MacroCategory, CaloriesPer100g).

% Carni & Pesce
ingredient(chicken, meat, 165).
ingredient(beef, meat, 250).
ingredient(salmon, fish, 208).
ingredient(tuna, fish, 132).
% [... omessi altri ingredienti comuni per brevità, vedi file sorgente ...]

% --- 3. FATTI: Ricette (Campione) ---
recipe(carbonara, [pasta, egg, cheese, bacon]).
recipe(pasta_pomodoro, [pasta, tomato, oil, onion]).
recipe(grilled_chicken, [chicken, oil]).
% [... 20+ ricette totali ...]

% --- 4. REGOLE LOGICHE ---

% 4.1 Regole Dietetiche
contains_meat(Recipe) :- recipe(Recipe, Ings), member(I, Ings), ingredient(I, meat, _).
contains_dairy(Recipe) :- recipe(Recipe, Ings), member(I, Ings), ingredient(I, dairy, _).
is_vegan(Recipe) :- \+ contains_meat(Recipe), \+ contains_dairy(Recipe), \+ contains_fish(Recipe), \+ contains_eggs(Recipe).

% 4.2 Piatto Completo (Macro-nutrienti)
has_carb(R) :- recipe(R, Ings), member(I, Ings), ingredient(I, grain, _).
has_protein(R) :- recipe(R, Ings), member(I, Ings), (ingredient(I, meat, _); ingredient(I, fish, _); ingredient(I, legume, _)).
has_veg(R) :- recipe(R, Ings), member(I, Ings), ingredient(I, vegetable, _).

complete_dish(R) :- has_carb(R), has_protein(R), has_veg(R).

% 4.3 Stagionalità (Inferenza su Liste)
is_seasonal(Recipe, Season) :-
    recipe(Recipe, Ings),
    forall(member(I, Ings), (
        (ingredient(I, vegetable, _); ingredient(I, fruit, _)) ->
        (season(I, Season); \+ season(I, _))
        ; true
    )).

% 4.4 Calcolo Calorie (Ricorsione)
calculate_cal([], 0).
calculate_cal([Ing|Tail], Tot) :-
    ingredient(Ing, _, Cal),
    calculate_cal(Tail, SubTot),
    Tot is Cal + SubTot.
```

## 2. Machine Learning: Classificatore di Ricette

Il modulo di classificazione etichetta le ricette in base al loro profilo nutrizionale (es. *High Protein*, *Low Cal*, *Balanced*).

### Dataset e Preprocessing
Poiché non era disponibile un dataset pubblico idoneo, è stato generato un **dataset sintetico controllato** di 600 istanze.
-   **Features ($X$)**: 4 attributi continui: [Calorie, Proteine, Carboidrati, Grassi].
-   **Target ($Y$)**: 5 classi di etichette nutrizionali.
-   **Preprocessing**: Scaling delle feature (StandardScaler) per normalizzare i range numerici diversi (es. calorie vs grammi).

### Disegno Sperimentale: Nested Cross-Validation
Per garantire una valutazione robusta e priva di bias, è stato adottato un approccio **Nested Cross-Validation (5x3)**:

1.  **Outer Loop (5-Fold Stratified CV)**:
    -   Divide il dataset in 5 parti. In ogni iterazione, trattiene un *Test Set* (20%) completamente separato per la valutazione finale delle performance.
    -   Fornisce metriche non distorte (Accuracy, F1-Score) sulla capacità di generalizzazione.

2.  **Inner Loop (3-Fold CV con GridSearch)**:
    -   Eseguito sul *Training Set* dell'Outer Loop.
    -   Esplora la griglia degli iperparametri (es. `max_depth` per DecisionTree, `k` per KNN) per selezionare la configurazione migliore.

Questo approccio assicura che gli iperparametri non siano ottimizzati sui dati di test, prevenendo l'overfitting (data leakage).

## 3. Constraint Satisfaction Problem (CSP)

Il Pianificatore di Diete è modellato formalmente come un CSP $<V, D, C>$.

### Definizione Formale
-   **Variabili ($V$)**: L'insieme dei pasti da pianificare in un giorno.
    $$V = \{ \text{Colazione}, \text{Pranzo}, \text{Cena}, \text{Snack}_1, \dots \}$$
-   **Domini ($D$)**: Per ogni variabile $v \in V$, il dominio $D_v$ è il sottoinsieme di ricette compatibili (es. $D_{Colazione} \subset \text{Ricette}$ di tipo 'breakfast').
    $$D_v = \{ r \in \text{KB} \mid \text{tipo}(r) \text{ compatibile con } v \land \text{rispetta vincoli unari} \}$$
    I vincoli unari (intolleranze) riducono il dominio *a priori*.
-   **Vincoli ($C$)**:
    1.  **Vincolo Globale sulle Calorie**:
        $$\left| \sum_{v \in V} \text{cal}(v) - \text{Target} \right| \leq \epsilon$$
    2.  **Varietà (AllDifferent)**:
        $$\forall v_i, v_j \in \{\text{Pranzo, Cena}\}, v_i \neq v_j$$

### Confronto Algoritmico
| Algoritmo | Tempo Esecuzione (3 Pasti) | Tempo Esecuzione (5 Pasti) | Completezza | Utilizzo |
| :--- | :--- | :--- | :--- | :--- |
| **Libreria (`python-constraint`)** | **< 0.001s** | **~0.002s** | Completo | Produzione |
| **Custom Backtracking** | ~0.005s | ~0.05s | Completo | Didattica/Verifica |

**Conclusione**: Il solver della libreria mantiene prestazioni costanti anche all'aumentare della complessità (5 pasti), mentre il backtracking custom mostra un leggero degrado prestazionale lineare/esponenziale, confermando l'efficacia delle euristiche di ottimizzazione (Forward Checking) integrate nella libreria. Entrambi garantiscono soluzioni valide (Scarto Calorie ~15-20% tolleranza).
