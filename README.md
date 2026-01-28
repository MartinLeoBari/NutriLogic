# NutriLogic

NutriLogic è un sistema progettato per generare piani alimentari su misura. L'approccio combina tre tecniche distinte per offrire risultati accurati:

*   **Machine Learning**: Il modulo `ml_classifier.py` utilizza alberi decisionali e KNN per classificare le ricette in base ai loro valori nutrizionali (calibra se un piatto è energetico, bilanciato o ipocalorico).
*   **Programmazione Logica**: Tramite `knowledge_base.pl` (basato su SWI-Prolog), il sistema gestisce le conoscenze su ingredienti e intolleranze, deducendo logicamente proprietà implicite (come identificare se un piatto è vegano o privo di lattosio).
*   **Constraint Satisfaction Problem (CSP)**: Il cuore del sistema è `csp_planner.py`, che calcola la combinazione ottimale di colazione, pranzo e cena rispettando sia i vincoli calorici matematici che le preferenze dell'utente.

---

## Guida all'Installazione

Ecco i passaggi per configurare l'ambiente su un computer Windows pulito.

### 1. Requisiti Python
Assicurati di avere **Python 3** (versione 3.10 o superiore) installato. Se non lo hai, scaricalo dal [sito ufficiale](https://www.python.org/downloads/).
*   **Nota fondamentale:** Durante l'installazione, ricorda di spuntare la casella **"Add Python to PATH"**.

### 2. Configurazione SWI-Prolog
Il modulo logico si basa su SWI-Prolog. Senza di esso, quella parte del programma non funzionerà.

**Su Windows:**
1.  Scarica la versione **"Microsoft Windows 64-bit"** da [swi-prolog.org](https://www.swi-prolog.org/download/stable).
2.  Avvia l'installazione.
3.  Quando richiesto, seleziona l'opzione **"Add swipl to the system PATH for all users"** (o "current user"). Questo passaggio è essenziale per permettere a Python di comunicare con Prolog.

**Su macOS:**
L'approccio più semplice è usare Homebrew. Apri il terminale e digita:
```bash
brew install swi-prolog
```
Se invece usi il file `.dmg`, dovrai aggiungere manualmente SWI-Prolog al tuo PATH (es. nel file `.zshrc`), altrimenti Python non troverà l'eseguibile.

### 3. Setup del Progetto
Scarica la cartella del progetto e posizionati al suo interno tramite terminale.

### 4. Installazione Dipendenze
Per installare tutte le librerie necessarie, esegui questo comando nel terminale:

```bash
pip install pandas scikit-learn pyswip python-constraint numpy
```
*Se riscontri errori con `pyswip`, assicurati che SWI-Prolog sia installato correttamente e aggiunto al PATH.*

---

## Come Usare NutriLogic

Hai due modalità per utilizzare il software.

### A. Interfaccia Grafica (Consigliata)
Per un'esperienza più intuitiva, avvia la GUI.
1.  Apri il terminale nella cartella del progetto.
2.  Esegui:
    ```bash
    python gui.py
    ```
    (o `python3 gui.py` su macOS/Linux)

Dall'interfaccia potrai inserire i tuoi dati, calcolare il tuo fabbisogno calorico e generare la dieta cliccando sui pulsanti dedicati.

### B. Linea di Comando
Se preferisci vedere il funzionamento "dietro le quinte" o testare l'algoritmo rapidamente:
1.  Apri il terminale nella cartella del progetto.
2.  Esegui:
    ```bash
    python main.py
    ```

Il sistema eseguirà una simulazione predefinita: addestrerà il modello, caricherà la base di conoscenza e genererà un menu di esempio da 1000 kcal per un utente intollerante al lattosio.

---

## Risoluzione Problemi

**Errore "Libreria python-constraint non trovata"** o simili:
Probabilmente hai saltato l'installazione delle dipendenze. Riprova con `pip install python-constraint`.

**Errore legato a PySWIP o Prolog:**
Se vedi errori che menzionano DLL mancanti o Prolog non trovato, al 99% il problema è che SWI-Prolog non è nel PATH di sistema. Reinstalla SWI-Prolog assicurandoti di spuntare "Add to PATH" o aggiungilo manualmente alle variabili d'ambiente.