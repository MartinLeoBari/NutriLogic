try:
    from constraint import Problem, AllDifferentConstraint, FunctionConstraint
except ImportError:
    print("Libreria 'python-constraint' non trovata. Installa con: pip install python-constraint")
    class Problem:
        def addVariable(self, name, domain): pass
        def addConstraint(self, func, vars): pass
        def getSolution(self): return None
        def getSolutions(self): return []
    class AllDifferentConstraint:
         pass

class DietPlanner:
    """
    Pianificatore di Dieta basato su CSP (Constraint Satisfaction Problem).

    FORMALIZZAZIONE CSP:
    --------------------
    1. Variabili (V):
       Insieme dei pasti giornalieri da pianificare.
       V = {Breakfast, Lunch, LunchSecond, Dinner, MorningSnack, AfternoonSnack} (se 5 pasti)
       V = {Lunch, Dinner, Snack} (se 3 pasti)

    2. Domini (D):
       Insieme delle ricette valide per ciascuna variabile (pasto).
       D_Breakfast = {r in Recipes | r.type == 'breakfast'}
       D_Lunch/Dinner = {r in Recipes | r.type in {'main', 'second'}}
       D_Snack = {r in Recipes | r.type in {'snack', 'dessert'}}

    3. Vincoli (C):
       - C_Calorie: |sum(calories(v)) - Target| <= Tolerance
         (Vincolo 'Soft' implementato come Hard con range di tolleranza)
       - C_Nutritional (Opzionali): sum(protein) >= Min, sum(fat) <= Max
       - C_Variety (AllDifferent): Lunch != Dinner, Snack1 != Snack2
    """

    def __init__(self):
        # Lista espansa di ricette (sincronizzata con knowledge_base.pl)
        self.recipes = [
             # --- COLAZIONE ---
            {'name': 'Porridge con Frutta', 'calories': 320, 'protein': 10, 'carbs': 55, 'fat': 8, 'fiber': 6, 'type': 'breakfast', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},
            {'name': 'Toast Integrale con Avocado', 'calories': 350, 'protein': 8, 'carbs': 40, 'fat': 18, 'fiber': 8, 'type': 'breakfast', 'contains_lactose': False, 'contains_gluten': True, 'vegetarian': True, 'vegan': True},
            {'name': 'Yogurt Greco con Miele e Noci', 'calories': 280, 'protein': 15, 'carbs': 25, 'fat': 14, 'fiber': 2, 'type': 'breakfast', 'contains_lactose': True, 'contains_gluten': False, 'vegetarian': True, 'vegan': False},
            {'name': 'Pancakes Proteici', 'calories': 400, 'protein': 25, 'carbs': 45, 'fat': 12, 'fiber': 3, 'type': 'breakfast', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},
            {'name': 'Muesli con Latte', 'calories': 350, 'protein': 12, 'carbs': 55, 'fat': 10, 'fiber': 5, 'type': 'breakfast', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},

            # --- PRIMI ---
            {'name': 'Carbonara', 'calories': 700, 'protein': 25, 'carbs': 70, 'fat': 35, 'fiber': 2, 'type': 'main', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': False, 'vegan': False},
            {'name': 'Pasta Pomodoro', 'calories': 450, 'protein': 12, 'carbs': 80, 'fat': 10, 'fiber': 4, 'type': 'main', 'contains_lactose': False, 'contains_gluten': True, 'vegetarian': True, 'vegan': True},
            {'name': 'Mac and Cheese', 'calories': 800, 'protein': 22, 'carbs': 75, 'fat': 45, 'fiber': 2, 'type': 'main', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},
            {'name': 'Risotto ai Funghi', 'calories': 480, 'protein': 10, 'carbs': 75, 'fat': 15, 'fiber': 3, 'type': 'main', 'contains_lactose': True, 'contains_gluten': False, 'vegetarian': True, 'vegan': False},
            {'name': 'Pasta al Pesto', 'calories': 550, 'protein': 15, 'carbs': 70, 'fat': 25, 'fiber': 3, 'type': 'main', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},
            {'name': 'Lasagna', 'calories': 850, 'protein': 35, 'carbs': 65, 'fat': 50, 'fiber': 4, 'type': 'main', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': False, 'vegan': False},
            {'name': 'Zuppa di Legumi', 'calories': 320, 'protein': 18, 'carbs': 45, 'fat': 8, 'fiber': 12, 'type': 'main', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Pizza Margherita', 'calories': 900, 'protein': 30, 'carbs': 100, 'fat': 40, 'fiber': 4, 'type': 'main', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},
            {'name': 'Ravioli Burro Salvia', 'calories': 520, 'protein': 18, 'carbs': 55, 'fat': 25, 'fiber': 2, 'type': 'main', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},
            {'name': 'Gnocchi al Sugo', 'calories': 420, 'protein': 10, 'carbs': 75, 'fat': 10, 'fiber': 3, 'type': 'main', 'contains_lactose': False, 'contains_gluten': True, 'vegetarian': True, 'vegan': True},

            # --- SECONDI ---
            {'name': 'Grilled Chicken', 'calories': 400, 'protein': 45, 'carbs': 5, 'fat': 22, 'fiber': 0, 'type': 'second', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': False, 'vegan': False},
            {'name': 'Salmone alla Griglia', 'calories': 380, 'protein': 35, 'carbs': 2, 'fat': 25, 'fiber': 0, 'type': 'second', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': False, 'vegan': False},
            {'name': 'Bistecca ai Ferri', 'calories': 350, 'protein': 40, 'carbs': 0, 'fat': 20, 'fiber': 0, 'type': 'second', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': False, 'vegan': False},
            {'name': 'Tofu Salad', 'calories': 300, 'protein': 20, 'carbs': 15, 'fat': 20, 'fiber': 5, 'type': 'second', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Omelette', 'calories': 220, 'protein': 15, 'carbs': 2, 'fat': 17, 'fiber': 0, 'type': 'second', 'contains_lactose': True, 'contains_gluten': False, 'vegetarian': True, 'vegan': False},
            {'name': 'Polpette al Sugo', 'calories': 350, 'protein': 25, 'carbs': 15, 'fat': 22, 'fiber': 2, 'type': 'second', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': False, 'vegan': False},
            {'name': 'Merluzzo al Vapore', 'calories': 180, 'protein': 30, 'carbs': 2, 'fat': 5, 'fiber': 0, 'type': 'second', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': False, 'vegan': False},
            {'name': 'Burger di Lenticchie', 'calories': 280, 'protein': 18, 'carbs': 35, 'fat': 10, 'fiber': 8, 'type': 'second', 'contains_lactose': False, 'contains_gluten': True, 'vegetarian': True, 'vegan': True},
            {'name': 'Caprese (Mozzarella)', 'calories': 320, 'protein': 18, 'carbs': 5, 'fat': 25, 'fiber': 1, 'type': 'second', 'contains_lactose': True, 'contains_gluten': False, 'vegetarian': True, 'vegan': False},
            {'name': 'Parmigiana di Melanzane', 'calories': 600, 'protein': 20, 'carbs': 25, 'fat': 48, 'fiber': 6, 'type': 'second', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},

            # --- CONTORNI ---
            {'name': 'Insalata Mista', 'calories': 80, 'protein': 3, 'carbs': 10, 'fat': 4, 'fiber': 4, 'type': 'side', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Verdure Grigliate', 'calories': 120, 'protein': 4, 'carbs': 15, 'fat': 6, 'fiber': 5, 'type': 'side', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Patate al Forno', 'calories': 200, 'protein': 4, 'carbs': 40, 'fat': 4, 'fiber': 4, 'type': 'side', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Spinaci Saltati', 'calories': 90, 'protein': 5, 'carbs': 8, 'fat': 5, 'fiber': 4, 'type': 'side', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},

            # --- SNACK / DESSERT ---
            {'name': 'Mela', 'calories': 52, 'protein': 0, 'carbs': 14, 'fat': 0, 'fiber': 2, 'type': 'snack', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Banana', 'calories': 89, 'protein': 1, 'carbs': 23, 'fat': 0, 'fiber': 3, 'type': 'snack', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Cioccolato Fondente (20g)', 'calories': 110, 'protein': 2, 'carbs': 10, 'fat': 8, 'fiber': 2, 'type': 'dessert', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Fruit Salad', 'calories': 150, 'protein': 2, 'carbs': 35, 'fat': 1, 'fiber': 4, 'type': 'dessert', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Yogurt', 'calories': 120, 'protein': 10, 'carbs': 12, 'fat': 4, 'fiber': 0, 'type': 'snack', 'contains_lactose': True, 'contains_gluten': False, 'vegetarian': True, 'vegan': False},
            {'name': 'Mandorle (30g)', 'calories': 170, 'protein': 6, 'carbs': 6, 'fat': 15, 'fiber': 3, 'type': 'snack', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Tiramisù', 'calories': 350, 'protein': 8, 'carbs': 40, 'fat': 18, 'fiber': 0, 'type': 'dessert', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False}
        ]

    def filter_recipes(self, intolerances=[], dietary_preference=None):
        """Filtra ricette per intolleranze e preferenze."""
        available_recipes = []
        for r in self.recipes:
            allowed = True

            if 'lactose' in intolerances and r.get('contains_lactose', False):
                allowed = False
            if 'gluten' in intolerances and r.get('contains_gluten', False):
                allowed = False

            if dietary_preference == 'vegetarian' and not r.get('vegetarian', False):
                allowed = False
            if dietary_preference == 'vegan' and not r.get('vegan', False):
                allowed = False

            if allowed:
                available_recipes.append(r)

        return available_recipes

    def solve(self, target_calories, intolerances=[], dietary_preference=None,
              min_protein=None, max_fat=None, min_fiber=None, num_meals=3):
        """Risolve il CSP usando 'python-constraint' (Backtracking Algorithm)."""
        problem = Problem()

        available_recipes = self.filter_recipes(intolerances, dietary_preference)
        if len(available_recipes) < num_meals:
            return None

        recipes_by_type = {
            'breakfast': [], 'main': [], 'second': [],
            'side': [], 'snack': [], 'dessert': []
        }
        for i, r in enumerate(available_recipes):
            recipes_by_type[r['type']].append(i)

        if num_meals == 5:
            # Definizione Variabili
            meal_vars = ["Breakfast", "Lunch", "LunchSecond", "Dinner", "MorningSnack", "AfternoonSnack"]

            # Domini
            problem.addVariable("Breakfast", recipes_by_type['breakfast'] or list(range(len(available_recipes))))
            main_domain = recipes_by_type['main'] if recipes_by_type['main'] else list(range(len(available_recipes)))
            problem.addVariable("Lunch", main_domain)
            problem.addVariable("Dinner", main_domain)
            second_domain = recipes_by_type['second'] if recipes_by_type['second'] else list(range(len(available_recipes)))
            problem.addVariable("LunchSecond", second_domain)
            snack_domain = recipes_by_type['snack'] + recipes_by_type['dessert']
            if not snack_domain: snack_domain = list(range(len(available_recipes)))
            problem.addVariable("MorningSnack", snack_domain)
            problem.addVariable("AfternoonSnack", snack_domain)
        else:
            meal_vars = ["Lunch", "Dinner", "Snack"]
            lunch_dinner_domain = recipes_by_type['main'] + recipes_by_type['second']
            if not lunch_dinner_domain: lunch_dinner_domain = list(range(len(available_recipes)))
            snack_domain = recipes_by_type['snack'] + recipes_by_type['dessert']
            if not snack_domain: snack_domain = list(range(len(available_recipes)))
            problem.addVariable("Lunch", lunch_dinner_domain)
            problem.addVariable("Dinner", lunch_dinner_domain)
            problem.addVariable("Snack", snack_domain)

        # Vincoli
        tolerance = max(50, min(300, int(target_calories * 0.15)))

        def calorie_constraint(*meal_indices):
            total = sum(available_recipes[idx]['calories'] for idx in meal_indices)
            return (target_calories - tolerance) <= total <= (target_calories + tolerance)

        problem.addConstraint(calorie_constraint, meal_vars)

        if min_protein is not None:
            def protein_constraint(*meal_indices):
                return sum(available_recipes[idx].get('protein', 0) for idx in meal_indices) >= min_protein
            problem.addConstraint(protein_constraint, meal_vars)

        if max_fat is not None:
             def fat_constraint(*meal_indices):
                return sum(available_recipes[idx].get('fat', 0) for idx in meal_indices) <= max_fat
             problem.addConstraint(fat_constraint, meal_vars)

        if num_meals == 5:
            problem.addConstraint(AllDifferentConstraint(), ["Lunch", "Dinner"])
            problem.addConstraint(AllDifferentConstraint(), ["MorningSnack", "AfternoonSnack"])
        else:
            problem.addConstraint(AllDifferentConstraint(), ["Lunch", "Dinner"])

        # Soluzione
        try:
            sol = problem.getSolution()
            if sol:
                return self._build_result(sol, available_recipes, meal_vars, target_calories)
            return None
        except Exception:
            return None

    def solve_custom_backtracking(self, target_calories, intolerances=[], dietary_preference=None, num_meals=3):
        """
        CUSTOM BACKTRACKING SOLVER.
        Implementazione algoritma di backtracking per confronto con libreria standard.
        """
        available_recipes = self.filter_recipes(intolerances, dietary_preference)
        if len(available_recipes) < num_meals:
            return None

        recipes_by_type = {
            'breakfast': [], 'main': [], 'second': [],
            'side': [], 'snack': [], 'dessert': []
        }
        for i, r in enumerate(available_recipes):
            recipes_by_type[r['type']].append(i)

        # Definizione struttura variabili e domini
        if num_meals == 5:
            vars_order = ["Breakfast", "Lunch", "LunchSecond", "Dinner", "MorningSnack", "AfternoonSnack"]
            domains = {
                "Breakfast": recipes_by_type['breakfast'],
                "Lunch": recipes_by_type['main'],
                "Dinner": recipes_by_type['main'],
                "LunchSecond": recipes_by_type['second'],
                "MorningSnack": recipes_by_type['snack'] + recipes_by_type['dessert'],
                "AfternoonSnack": recipes_by_type['snack'] + recipes_by_type['dessert']
            }
        else:
            vars_order = ["Lunch", "Dinner", "Snack"]
            main_sec = recipes_by_type['main'] + recipes_by_type['second']
            domains = {
                "Lunch": main_sec,
                "Dinner": main_sec,
                "Snack": recipes_by_type['snack'] + recipes_by_type['dessert']
            }

        # Gestione domini vuoti fallback
        for v in vars_order:
            if not domains[v]: domains[v] = list(range(len(available_recipes)))

        tolerance = max(50, min(300, int(target_calories * 0.15)))

        # Algoritmo Backtracking Ricorsivo
        def recursive_backtrack(assignment):
            # Base case: Complete assignment
            if len(assignment) == len(vars_order):
                # Check Global Constraint (Calories)
                total_cal = sum(available_recipes[assignment[v]]['calories'] for v in vars_order)
                if (target_calories - tolerance) <= total_cal <= (target_calories + tolerance):
                    return assignment
                return None

            # Recursive step
            var_to_assign = vars_order[len(assignment)]

            for value_idx in domains[var_to_assign]:
                # Check Local Constraints (AllDifferent)
                if var_to_assign == "Dinner" and "Lunch" in assignment:
                    if assignment["Lunch"] == value_idx: continue
                if var_to_assign == "AfternoonSnack" and "MorningSnack" in assignment:
                    if assignment["MorningSnack"] == value_idx: continue

                # Forward Checking (Pruning) rudimentale sulle calorie
                # Se le calorie correnti + stima minima superano il massimo, taglia.
                # Se le calorie correnti + stima massima sono sotto il minimo, taglia.
                current_cal = sum(available_recipes[assignment[v]]['calories'] for v in assignment)
                current_cal += available_recipes[value_idx]['calories']
                remaining_vars = len(vars_order) - len(assignment) - 1

                # Euristica: Stima calorie minime/massime rimanenti
                min_potential = current_cal + (remaining_vars * 50)
                max_potential = current_cal + (remaining_vars * 1000)

                if min_potential > (target_calories + tolerance): continue # Pruning
                if max_potential < (target_calories - tolerance): continue # Pruning

                # Assegna e ricorri
                new_assignment = assignment.copy()
                new_assignment[var_to_assign] = value_idx
                result = recursive_backtrack(new_assignment)
                if result is not None:
                    return result

            return None # Backtrack

        # Avvio
        solution = recursive_backtrack({})
        if solution:
            return self._build_result(solution, available_recipes, vars_order, target_calories)
        return None

    def compare_solvers(self, target_calories, intolerances=[], num_meals=3):
        """Confronta CSP Library vs Custom Backtracking."""
        import time

        print(f"\n--- Confronto Solver (Target: {target_calories} kcal, Pasti: {num_meals}) ---")

        # 1. Library Solver
        start_time = time.time()
        lib_sol = self.solve(target_calories, intolerances, num_meals=num_meals)
        lib_time = time.time() - start_time
        lib_score = lib_sol['_diff'] if lib_sol else "N/A"
        print(f"Library CSP Solver: Tempo = {lib_time:.4f}s, Scarto = {lib_score}")

        # 2. Custom Solver
        start_time = time.time()
        cust_sol = self.solve_custom_backtracking(target_calories, intolerances, num_meals=num_meals)
        cust_time = time.time() - start_time
        cust_score = cust_sol['_diff'] if cust_sol else "N/A"
        print(f"Custom Backtracking: Tempo = {cust_time:.4f}s, Scarto = {cust_score}")

        return lib_sol, cust_sol

    def _build_result(self, solution, available_recipes, meal_vars, target_calories):
        """Costruisce il risultato finale."""
        result = {}
        totals = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0, 'fiber': 0}

        for var in meal_vars:
            recipe = available_recipes[solution[var]]
            result[var] = recipe
            totals['calories'] += recipe['calories']
            totals['protein'] += recipe.get('protein', 0)
            totals['carbs'] += recipe.get('carbs', 0)
            totals['fat'] += recipe.get('fat', 0)
            totals['fiber'] += recipe.get('fiber', 0)

        result['_totals'] = totals
        result['_target'] = target_calories
        result['_diff'] = abs(totals['calories'] - target_calories)

        return result

    def get_recipe_info(self, recipe_name):
        for r in self.recipes:
            if r['name'].lower() == recipe_name.lower():
                return r
        return None

if __name__ == '__main__':
    planner = DietPlanner()
    planner.compare_solvers(target_calories=2000, num_meals=3)
    planner.compare_solvers(target_calories=2200, num_meals=5)
