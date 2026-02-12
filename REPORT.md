# NutriLogic - Intelligent Diet Assistant

**Gruppo di lavoro:**
-   Martin Leo (797052) - m.leo39@studneti.uniba.it
-   Francesco Liantonio (800275) - f.liantonio2@studenti.uniba.it
-   Simone Frezza (801716) - s.frezza@studenti.uniba.it

**Repository:** [https://github.com/MartinLeoBari/NutriLogic.git](https://github.com/MartinLeoBari/NutriLogic.git)
**Anno Accademico:** 2025-2026

---

## 1. Introduzione
Il dominio di interesse è la nutrizione personalizzata assistita da intelligenza artificiale. La pianificazione dei pasti è un problema complesso che richiede di bilanciare vincoli nutrizionali rigidi (calorie, macro-nutrienti), restrizioni dietetiche (allergie, stili di vita) e preferenze personali.
**NutriLogic** è un sistema KBS (Knowledge-Based System) progettato per assistere l'utente nella creazione di piani alimentari bilanciati, classificare automaticamente nuove ricette e verificare la compatibilità degli ingredienti con specifici profili dietetici.

## 2. Architettura del Sistema
Il sistema integra tre moduli principali che cooperano per fornire una soluzione completa:

1.  **Modulo KB (Prolog)**: Gestisce la conoscenza ontologica e le regole di inferenza (es. compatibilità vegana, stagionalità).
2.  **Modulo ML (Python/Scikit-learn)**: Classificatore supervisionato per predire l'etichetta nutrizionale ("Health Score") di nuove ricette.
3.  **Modulo CSP (Python)**: Solutore di vincoli per la generazione dei menu giornalieri.

---

## 3. Modulo Knowledge Base (Logic Programming)

### 3.1 Rappresentazione della Conoscenza
Per la rappresentazione della conoscenza è stato utilizzato **Prolog**. La KB non agisce come un semplice database, ma definisce regole logiche per inferire proprietà non esplicite.
-   **Fatti**: Database degli ingredienti (~60 entità) con macro-categoria e calorie; Database delle ricette (~25 ricette).
-   **Regole**: Abbiamo modellato regole per dedurre se un piatto è adatto a celiaci, vegani o intolleranti al lattosio, e regole complesse come `is_seasonal` o `complete_dish`.

### 3.2 Decisioni di Progetto
Si è scelto di separare i "fatti" dalle "regole".
*Esempio*: `is_vegan(Recipe)` non è salvato come fatto, ma derivato ricorsivamente verificando che nessun ingrediente sia di origine animale. Questo riduce la ridondanza e garantisce coerenza.

### 3.3 Analisi della Complessità
Le regole logiche sono strutturate come **Clausole di Horn**, garantendo un'inferenza efficiente.
-   **Complessità Ciclomatica**: Bassa per la maggior parte delle regole.
-   **Complessità Computazionale**: Predicati come `is_seasonal/2` comportano un'iterazione (`forall/2`) sulla lista degli ingredienti, risultando in una complessità lineare $O(N)$ rispetto al numero di ingredienti ($N \approx 5-10$).

### 3.4 Appendice: Codice Sorgente KB
### 3.4 Regole Ricorsive (Novità)
Per gestire le dipendenze profonde tra ingredienti (es. allergeni nascosti), sono state introdotte regole ricorsive:
```prolog
% Relazione Transitiva: un ingrediente deriva da un altro
derived_from(X, Y) :- composed_of(X, Y).
derived_from(X, Z) :- composed_of(X, Y), derived_from(Y, Z).

% Query Esempio: Il pesto contiene latte?
% ?- contains_allergen_deep(pasta_pesto, milk).
% true. (Trace: pasta_pesto -> pesto -> parmesan -> milk)
```

## 4. Modulo Machine Learning (Supervised Learning)

Il modulo ML classifica le ricette in categorie come "Low Calorie", "Balanced", "High Energy".

### 4.1 Dataset Bilanciato
È stato generato un dataset sintetico di **600 istanze**, bilanciato uniformemente tra le 5 classi (~120 istanze per classe) per evitare bias nel training.
-   **Features**: [Calorie, Proteine, Carboidrati, Grassi].
-   **Classi**: Low Cal, Low Fat, Balanced, High Protein, High Energy.

### 4.2 Disegno Sperimentale: Nested Cross-Validation
(Invariato: 5x3 Folds)

### 4.3 Risultati Sperimentali
Grazie al bilanciamento delle classi, Accuracy e F1-Score sono metriche affidabili.

| Modello | Accuracy (Mean) | F1-Score (Macro) | Note |
| :--- | :--- | :--- | :--- |
| **KNN** | 0.88 (+/- 0.04) | 0.88 | Buono. |
| **Decision Tree** | **0.93 (+/- 0.02)** | **0.93** | **Eccellente**. Regole estratte: `IF cal < 300 THEN Low Cal`. |

---

## 5. Modulo Constraint Satisfaction Problem (CSP)

### 5.1 Algoritmi a Confronto
Oltre al Backtracking (Libreria vs Custom), è stato implementato un algoritmo di **Local Search (Simulated Annealing)** per validare l'approccio su spazi di ricerca ampi.

1.  **Backtracking (Constraint Propagation)**: Metodo completo, esplora sistematicamente.
2.  **Simulated Annealing (Meta-euristica)**: Metodo probabilistico. Parte da una soluzione casuale e la migliora, accettando peggioramenti con probabilità decrescente (Temperatura) per uscire da ottimi locali.

### 5.2 Risultati Benchmark
| Algoritmo | Tempo (3 Pasti) | Tempo (5 Pasti) | Completezza | Scarto Obiettivo |
| :--- | :--- | :--- | :--- | :--- |
| **Libreria (`python-constraint`)** | **< 0.001s** | **~0.002s** | Completo | Ottimo |
| **Simulated Annealing** | ~0.02s | ~0.04s | Probabilistico | Buono (< 15%) |
| **Custom Backtracking** | ~0.005s | ~0.05s | Completo | Ottimo |

**Conclusione**: Il solver basato su libreria rimane il più efficiente grazie alle euristiche di dominio. Il Simulated Annealing si dimostra una valida alternativa approssimata, convergendo in tempi rapidi anche se non garantisce la soluzione ottima globale (scarto medio accettabile).

---

## 6. Conclusioni
Il sistema NutriLogic dimostra come la logica simbolica (Prolog) possa guidare efficacemente (filtraggio domini, verifica vincoli) un sistema statistico (ML) e un solutore combinatorio (CSP).
I risultati sperimentali confermano l'affidabilità del classificatore (Acc > 90%) e l'efficienza del solver CSP per la pianificazione real-time.

## 7. Riferimenti Bibliografici
[1] Poole, D. L., & Mackworth, A. K. (2017). *Artificial Intelligence: foundations of computational agents*. Cambridge University Press.
[2] Documentazione Scikit-Learn: [https://scikit-learn.org](https://scikit-learn.org)
[3] SWI-Prolog Reference Manual.
