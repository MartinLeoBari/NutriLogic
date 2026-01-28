import tkinter as tk
from tkinter import ttk, messagebox
import threading

from ml_classifier import RecipeClassifier
from csp_planner import DietPlanner

class ToolTip:
    """Tooltip al passaggio del mouse."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None

        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 20

        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                       background="#2d2d30", fg="white", relief=tk.SOLID, borderwidth=1,
                       font=("Segoe UI", 9))
        label.pack(ipadx=5, ipady=3)

    def hide_tip(self, event=None):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

class NutriLogicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NutriLogic - AI Diet Assistant")
        self.root.geometry("1400x830")
        self.root.minsize(1400, 830)


        style = ttk.Style()
        try:
            style.theme_use('clam')
        except:
            pass

        bg_color = "#f4f4f4"
        self.root.configure(bg=bg_color)

        style.configure('TFrame', background=bg_color)
        style.configure('TLabelframe', background=bg_color, relief='groove', borderwidth=2)
        style.configure('TLabelframe.Label', font=('Segoe UI', 11, 'bold'), background=bg_color, foreground="#333")

        style.configure('TLabel', background=bg_color, font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=8)
        style.map('TButton', background=[('active', '#e1e1e1')])

        style.configure('TCheckbutton', background=bg_color, font=('Segoe UI', 10))

        self.planner = DietPlanner()
        self.classifier = None

        self.create_widgets()

        self.status_var.set("Training ML Model...")
        threading.Thread(target=self.init_ml, daemon=True).start()

    def add_info_btn(self, parent, msg, r, c):
        lbl = tk.Label(parent, text="ⓘ", fg="#0078d7", bg="#f4f4f4", font=("Segoe UI", 12), cursor="hand2")
        lbl.grid(row=r, column=c, sticky=tk.W, padx=5)
        ToolTip(lbl, msg)

    def init_ml(self):
        try:
            dataset_path = 'dataset.csv'
            self.classifier = RecipeClassifier(dataset_path)
            self.classifier.train_and_evaluate()
            self.root.after(0, lambda: self.status_var.set("System Ready - ML Model Trained"))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"ML Error: {str(e)}"))  # noqa: F821

    def create_widgets(self):
        style = ttk.Style()
        style.configure('TNotebook', background="#f4f4f4", borderwidth=0)

        style.configure('TNotebook.Tab',
                       padding=[15, 5],
                       font=('Segoe UI', 9),
                       background="#e0e0e0",
                       foreground="#555")

        style.map("TNotebook.Tab",
            padding=[("selected", [25, 12])],
            font=[("selected", ('Segoe UI', 11, 'bold'))],
            background=[("selected", "#ffffff")],
            foreground=[("selected", "#000000")],
            expand=[("selected", [1, 1, 1, 0])]
        )

        tab_control = ttk.Notebook(self.root)

        self.tab_planner = ttk.Frame(tab_control)
        self.tab_classifier = ttk.Frame(tab_control)

        tab_control.add(self.tab_planner, text=' Plan Dieta (CSP) ')
        tab_control.add(self.tab_classifier, text=' Analisi Ricette (ML) ')
        tab_control.pack(expand=1, fill="both", padx=10, pady=10)

        self.setup_planner_tab()
        self.setup_classifier_tab()

        self.status_var = tk.StringVar()
        self.status_var.set("Initializing...")

        status_frame = tk.Frame(self.root, bd=1, relief=tk.SUNKEN, bg="#e8e8e8")
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        status_lbl = tk.Label(status_frame, textvariable=self.status_var, bg="#e8e8e8", fg="#555", anchor=tk.W, padx=10, pady=5)
        status_lbl.pack(fill=tk.X)

    def setup_planner_tab(self):
        frame = ttk.LabelFrame(self.tab_planner, text=" Generatore Piano Alimentare ", padding=15)
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(3, weight=1)
        frame.rowconfigure(10, weight=1)

        intro = ttk.Label(frame, text="Questo modulo usa tecniche CSP (Constraint Satisfaction Problem) per generare un menu personalizzato.", foreground="#666")
        intro.grid(row=0, column=0, columnspan=5, pady=(0, 15), sticky=tk.W)

        ttk.Label(frame, text="Calorie Target (kcal):").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.cal_entry = ttk.Entry(frame, width=12)
        self.cal_entry.insert(0, "2000")
        self.cal_entry.grid(row=1, column=1, sticky=tk.W, pady=8)
        self.add_info_btn(frame, "Definisci il totale calorico giornaliero desiderato.\nIl sistema troverà una combinazione ottimale (+/- tolleranza).", 1, 2)

        ttk.Label(frame, text="Numero Pasti:").grid(row=1, column=3, sticky=tk.W, pady=8, padx=(20, 0))
        self.meals_var = tk.StringVar(value="5")
        meals_combo = ttk.Combobox(frame, textvariable=self.meals_var, values=["3", "5"], width=8, state="readonly")
        meals_combo.grid(row=1, column=4, sticky=tk.W, pady=8)

        ttk.Label(frame, text="Intolleranze:").grid(row=2, column=0, sticky=tk.NW, pady=8)
        intol_frame = ttk.Frame(frame)
        intol_frame.grid(row=2, column=1, columnspan=4, sticky=tk.W, pady=8)

        self.lactose_var = tk.BooleanVar()
        self.gluten_var = tk.BooleanVar()
        ttk.Checkbutton(intol_frame, text="Lattosio", variable=self.lactose_var).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Checkbutton(intol_frame, text="Glutine", variable=self.gluten_var).pack(side=tk.LEFT, padx=(0, 15))

        info_intol = tk.Label(frame, text="ⓘ", fg="#0078d7", bg="#f4f4f4", font=("Segoe UI", 12), cursor="hand2")
        info_intol.grid(row=2, column=4, sticky=tk.E, padx=5)
        ToolTip(info_intol, "Filtra automaticamente le ricette contenenti\nlatticini e/o glutine dal piano alimentare.")

        ttk.Label(frame, text="Preferenza Alimentare:").grid(row=3, column=0, sticky=tk.W, pady=8)
        self.diet_pref_var = tk.StringVar(value="Nessuna")
        pref_combo = ttk.Combobox(frame, textvariable=self.diet_pref_var,
                                   values=["Nessuna", "Vegetariano", "Vegano"], width=15, state="readonly")
        pref_combo.grid(row=3, column=1, sticky=tk.W, pady=8)
        self.add_info_btn(frame, "Seleziona la tua preferenza alimentare:\n• Nessuna: include tutti i cibi\n• Vegetariano: esclude carne e pesce\n• Vegano: esclude tutti i prodotti animali", 3, 2)

        ttk.Label(frame, text="Vincoli Opzionali:").grid(row=4, column=0, sticky=tk.NW, pady=8)

        constraints_frame = ttk.Frame(frame)
        constraints_frame.grid(row=4, column=1, columnspan=4, sticky=tk.W, pady=8)

        ttk.Label(constraints_frame, text="Min Proteine (g):").pack(side=tk.LEFT)
        self.min_protein_entry = ttk.Entry(constraints_frame, width=6)
        self.min_protein_entry.pack(side=tk.LEFT, padx=(2, 15))

        ttk.Label(constraints_frame, text="Max Grassi (g):").pack(side=tk.LEFT)
        self.max_fat_entry = ttk.Entry(constraints_frame, width=6)
        self.max_fat_entry.pack(side=tk.LEFT, padx=(2, 15))

        ttk.Label(constraints_frame, text="Min Fibre (g):").pack(side=tk.LEFT)
        self.min_fiber_entry = ttk.Entry(constraints_frame, width=6)
        self.min_fiber_entry.pack(side=tk.LEFT, padx=(2, 0))

        ttk.Label(frame, text="Opzioni Output:").grid(row=5, column=0, sticky=tk.W, pady=8)
        self.show_alternatives_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text="Mostra alternative per ogni pasto", variable=self.show_alternatives_var).grid(row=5, column=1, columnspan=2, sticky=tk.W, pady=8)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=6, column=0, columnspan=5, pady=20, sticky=tk.W)

        self.btn_generate = ttk.Button(btn_frame, text="Genera Piano Ottimale", command=self.generate_plan)
        self.btn_generate.pack(side=tk.LEFT, padx=(0, 10))

        info_btn = tk.Label(frame, text="ⓘ", fg="#0078d7", bg="#f4f4f4", font=("Segoe UI", 12), cursor="hand2")
        info_btn.grid(row=6, column=4, sticky=tk.E, padx=5)
        ToolTip(info_btn, "Genera un piano alimentare ottimizzato\nche rispetta tutti i vincoli impostati.")

        res_lbl = ttk.Label(frame, text="Risultato Elaborazione:", font=('Segoe UI', 10, 'bold'))
        res_lbl.grid(row=9, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))

        # Frame per la tabella dei pasti
        table_frame = ttk.Frame(frame)
        table_frame.grid(row=10, column=0, columnspan=5, sticky="nsew", pady=(0, 10))

        # Configurazione stile Treeview
        style = ttk.Style()
        style.configure("Meal.Treeview", font=('Segoe UI', 10), rowheight=28, background="white", fieldbackground="white")
        style.configure("Meal.Treeview.Heading", font=('Segoe UI', 10, 'bold'), background="#1a5f7a", foreground="white")
        style.map("Meal.Treeview.Heading", background=[('active', '#1a5f7a')], foreground=[('active', 'white')])

        # Rimuovi effetti hover e selezione

        # Treeview per i pasti (selectmode="none" disabilita la selezione)
        columns = ("meal", "recipe", "kcal", "protein", "carbs", "fat", "alternatives")
        self.meal_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10, style="Meal.Treeview", selectmode="none")

        self.meal_tree.heading("meal", text="Pasto")
        self.meal_tree.heading("recipe", text="Ricetta")
        self.meal_tree.heading("kcal", text="Kcal")
        self.meal_tree.heading("protein", text="P")
        self.meal_tree.heading("carbs", text="C")
        self.meal_tree.heading("fat", text="G")
        self.meal_tree.heading("alternatives", text="Alternative")

        self.meal_tree.column("meal", width=110, anchor="w")
        self.meal_tree.column("recipe", width=160, anchor="w")
        self.meal_tree.column("kcal", width=45, anchor="center")
        self.meal_tree.column("protein", width=35, anchor="center")
        self.meal_tree.column("carbs", width=35, anchor="center")
        self.meal_tree.column("fat", width=35, anchor="center")
        self.meal_tree.column("alternatives", width=350, anchor="w")

        self.meal_tree.pack(fill="both", expand=True)

        # Frame per i totali
        self.totals_frame = tk.Frame(frame, bg="#e8f5e9", pady=8, padx=15, bd=1, relief="groove")
        self.totals_frame.grid(row=11, column=0, columnspan=5, sticky="ew", pady=(5, 0))

        self.totals_label = tk.Label(self.totals_frame, text="Totali giornalieri: -",
                                      font=('Segoe UI', 11, 'bold'), bg="#e8f5e9", fg="#2e7d32")
        self.totals_label.pack()

        self.totals_detail = tk.Label(self.totals_frame, text="",
                                       font=('Segoe UI', 10), bg="#e8f5e9", fg="#1b5e20")
        self.totals_detail.pack()

        # Label per messaggi/errori
        self.status_result_var = tk.StringVar(value="")
        self.status_result_label = tk.Label(frame, textvariable=self.status_result_var,
                                             font=('Segoe UI', 10), fg="#666", bg="#f4f4f4")
        self.status_result_label.grid(row=12, column=0, columnspan=5, sticky="w", pady=(5, 0))

    def setup_classifier_tab(self):
        frame = ttk.LabelFrame(self.tab_classifier, text=" Analisi Nutrizionale Ricetta ", padding=20)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        intro = ttk.Label(frame, text="Questo modulo usa il Machine Learning (KNN/Decision Tree)\nper classificare una ricetta in base ai suoi macronutrienti.", foreground="#666")
        intro.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky=tk.W)

        def add_input(idx, label_text, var_ref, info_text):
            ttk.Label(frame, text=label_text).grid(row=idx, column=0, sticky=tk.W, pady=8)
            entry = ttk.Entry(frame, width=15)
            entry.grid(row=idx, column=1, sticky=tk.W, pady=8)
            self.add_info_btn(frame, info_text, idx, 2)
            return entry

        self.r_cal = add_input(1, "Calorie (kcal):", None, "Quantità totale di energia fornita dalla ricetta.")
        self.r_prot = add_input(2, "Proteine (g):", None, "Grammi di proteine (es. carne, legumi). Importante per i muscoli.")
        self.r_carb = add_input(3, "Carboidrati (g):", None, "Grammi di carboidrati (es. pasta, pane, zuccheri). Fonte primaria di energia.")
        self.r_fat  = add_input(4, "Grassi (g):", None, "Grammi di lipidi (es. olio, burro). Alta densità energetica.")

        btn = ttk.Button(frame, text="Classifica Ricetta", command=self.classify_recipe)
        btn.grid(row=5, column=0, columnspan=2, pady=25)

        self.add_info_btn(frame, "Invia i dati al modello predittivo addestrato.\nIl sistema stimerà l'etichetta nutrizionale (es. 'Balanced', 'High Energy').", 5, 2)

        result_container = tk.Frame(frame, bg="#e0f7fa", pady=15, padx=15, bd=1, relief="solid")
        result_container.grid(row=6, column=0, columnspan=3, sticky="ew")

        tk.Label(result_container, text="Esito Predizione:", bg="#e0f7fa", font=("Segoe UI", 10)).pack()
        self.lbl_prediction = tk.Label(result_container, text="-", font=("Arial", 16, "bold"), fg="#00695c", bg="#e0f7fa")
        self.lbl_prediction.pack()

    def _get_plan_params(self):
        try:
            target = int(self.cal_entry.get())
        except ValueError:
            raise ValueError("Inserisci un numero valido per le calorie.")

        intolerances = []
        if self.lactose_var.get():
            intolerances.append('lactose')
        if self.gluten_var.get():
            intolerances.append('gluten')

        pref_map = {"Nessuna": None, "Vegetariano": "vegetarian", "Vegano": "vegan"}
        dietary_pref = pref_map.get(self.diet_pref_var.get(), None)

        min_protein = None
        max_fat = None
        min_fiber = None

        if self.min_protein_entry.get().strip():
            min_protein = int(self.min_protein_entry.get())
        if self.max_fat_entry.get().strip():
            max_fat = int(self.max_fat_entry.get())
        if self.min_fiber_entry.get().strip():
            min_fiber = int(self.min_fiber_entry.get())

        num_meals = int(self.meals_var.get())

        return target, intolerances, dietary_pref, min_protein, max_fat, min_fiber, num_meals

    def _format_meal_name(self, meal_key):
        translations = {
            'Breakfast': 'Colazione',
            'Lunch': 'Pranzo (Primo)',
            'LunchSecond': 'Pranzo (Secondo)',
            'Dinner': 'Cena',
            'MorningSnack': 'Spuntino Mattina',
            'AfternoonSnack': 'Spuntino Pomeriggio',
            'Snack': 'Snack'
        }
        return translations.get(meal_key, meal_key)

    def _estimate_serving(self, recipe):
        """Stima la porzione in grammi basata su tipo e calorie."""
        recipe_type = recipe.get('type', 'main')
        calories = recipe.get('calories', 300)

        # Porzioni standard per tipo
        serving_map = {
            'breakfast': 200,   # Colazione ~200g
            'main': 350,        # Primi ~350g (pasta, riso)
            'second': 180,      # Secondi ~180g (carne, pesce)
            'side': 150,        # Contorni ~150g
            'snack': 100,       # Snack ~100g
            'dessert': 120      # Dolci ~120g
        }

        base = serving_map.get(recipe_type, 200)

        # Aggiustamento in base alle calorie (più calorie = porzione più densa)
        if calories > 600:
            base = int(base * 0.9)
        elif calories < 200:
            base = int(base * 1.1)

        return base

    def _display_plan(self, plan, plan_num=None):
        # Pulisci la tabella
        for item in self.meal_tree.get_children():
            self.meal_tree.delete(item)

        order_5 = ['Breakfast', 'MorningSnack', 'Lunch', 'LunchSecond', 'AfternoonSnack', 'Dinner']
        order_3 = ['Lunch', 'Dinner', 'Snack']
        order = order_5 if 'Breakfast' in plan else order_3

        for meal in order:
            if meal in plan and not meal.startswith('_'):
                recipe = plan[meal]
                meal_name = self._format_meal_name(meal)

                kcal = recipe.get('calories', '-')
                protein = recipe.get('protein', '-')
                carbs = recipe.get('carbs', '-')
                fat = recipe.get('fat', '-')

                # Calcola porzione stimata in grammi
                serving = recipe.get('serving', self._estimate_serving(recipe))
                recipe_display = f"{recipe['name']} ({serving}g)"

                # Ottieni alternative se richiesto
                alt_text = ""
                if self.show_alternatives_var.get():
                    alternatives = self.planner.suggest_alternatives(
                        recipe['name'],
                        self._get_current_intolerances(),
                        self._get_current_dietary_pref()
                    )
                    if alternatives:
                        alt_names = [f"{a['name']} ({self._estimate_serving(a)}g)" for a in alternatives[:2]]
                        alt_text = ", ".join(alt_names)

                # Inserisci riga nella tabella
                self.meal_tree.insert("", "end", values=(
                    meal_name, recipe_display, kcal, protein, carbs, fat, alt_text
                ))

        # Aggiorna i totali
        if '_totals' in plan:
            totals = plan['_totals']
            target_info = ""
            if '_target' in plan:
                diff = plan['_diff']
                target_info = f" (target: {plan['_target']} kcal, diff: {'+' if diff >= 0 else ''}{diff})"

            self.totals_label.config(text=f"Totale Calorie: {totals['calories']} kcal{target_info}")
            self.totals_detail.config(text=f"Proteine: {totals['protein']}g  |  Carboidrati: {totals['carbs']}g  |  Grassi: {totals['fat']}g  |  Fibre: {totals['fiber']}g")

    def _get_current_intolerances(self):
        intolerances = []
        if self.lactose_var.get():
            intolerances.append('lactose')
        if self.gluten_var.get():
            intolerances.append('gluten')
        return intolerances

    def _get_current_dietary_pref(self):
        pref_map = {"Nessuna": None, "Vegetariano": "vegetarian", "Vegano": "vegan"}
        return pref_map.get(self.diet_pref_var.get(), None)

    def _set_buttons_state(self, state):
        self.btn_generate.config(state=state)

    def generate_plan(self):
        try:
            target, intolerances, dietary_pref, min_protein, max_fat, min_fiber, num_meals = self._get_plan_params()
        except ValueError as e:
            messagebox.showerror("Errore", str(e))
            return

        self._set_buttons_state('disabled')
        # Pulisci la tabella
        for item in self.meal_tree.get_children():
            self.meal_tree.delete(item)
        self.totals_label.config(text="Totali giornalieri: -")
        self.totals_detail.config(text="")
        self.status_result_var.set("⏳ Ricerca in corso...")
        self.root.update()

        # Flag per gestire il timeout
        self._search_completed = False
        self._search_result = None

        def run_solver():
            try:
                plan = self.planner.solve(
                    target,
                    intolerances=intolerances,
                    dietary_preference=dietary_pref,
                    min_protein=min_protein,
                    max_fat=max_fat,
                    min_fiber=min_fiber,
                    num_meals=num_meals
                )
                self._search_result = plan
                self._search_completed = True
                self.root.after(0, lambda: self._on_plan_complete(plan))
            except Exception as e:
                self._search_completed = True
                self.root.after(0, lambda: self._on_plan_error(str(e)))  # noqa: F821

        def check_timeout():
            if not self._search_completed:
                # Timeout raggiunto, mostra messaggio
                self._on_timeout()

        threading.Thread(target=run_solver, daemon=True).start()
        # Imposta timeout di 20 secondi
        self.root.after(20000, check_timeout)

    def _on_timeout(self):
        if not self._search_completed:
            self._search_completed = True  # Evita che il solver completi dopo
            self._set_buttons_state('normal')
            # Pulisci la tabella
            for item in self.meal_tree.get_children():
                self.meal_tree.delete(item)
            self.totals_label.config(text=" Timeout - Nessun risultato trovato")
            self.totals_detail.config(text="")
            self.status_result_var.set("Ricerca annullata. Prova con vincoli meno restrittivi.")

    def _on_plan_complete(self, plan):
        if not self._search_completed:
            return  # Ignorato se timeout già scattato
        self._set_buttons_state('normal')
        self.status_result_var.set("")

        if plan:
            self._display_plan(plan)
            self.status_result_var.set("Piano generato con successo!")
        else:
            # Pulisci la tabella
            for item in self.meal_tree.get_children():
                self.meal_tree.delete(item)
            self.totals_label.config(text="Nessun piano trovato")
            self.totals_detail.config(text="")
            self.status_result_var.set("❌ Suggerimenti: aumenta calorie target, riduci vincoli, verifica intolleranze")

    def _on_plan_error(self, error_msg):
        self._set_buttons_state('normal')
        messagebox.showerror("Errore Planner", error_msg)

    def classify_recipe(self):
        if not self.classifier:
            messagebox.showwarning("Wait", "Classifier is still training...")
            return

        try:
            cal = float(self.r_cal.get())
            prot = float(self.r_prot.get())
            carb = float(self.r_carb.get())
            fat = float(self.r_fat.get())

            new_recipe = [cal, prot, carb, fat]
            prediction = self.classifier.predict([new_recipe])

            self.lbl_prediction.config(text=f"Prediction: {prediction[0]}")

        except ValueError:
            messagebox.showerror("Error", "Please enter numeric values for all fields.")
        except Exception as e:
            messagebox.showerror("Prediction Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    # Set icon if available (skip for portability)
    app = NutriLogicApp(root)
    root.mainloop()
