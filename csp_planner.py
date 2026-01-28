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
    def __init__(self):
        self.recipes = [
            # COLAZIONE
            {'name': 'Porridge con Frutta', 'calories': 320, 'protein': 10, 'carbs': 55, 'fat': 8, 'fiber': 6, 'type': 'breakfast', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},
            {'name': 'Toast Integrale con Avocado', 'calories': 350, 'protein': 8, 'carbs': 40, 'fat': 18, 'fiber': 8, 'type': 'breakfast', 'contains_lactose': False, 'contains_gluten': True, 'vegetarian': True, 'vegan': True},
            {'name': 'Yogurt Greco con Miele e Noci', 'calories': 280, 'protein': 15, 'carbs': 25, 'fat': 14, 'fiber': 2, 'type': 'breakfast', 'contains_lactose': True, 'contains_gluten': False, 'vegetarian': True, 'vegan': False},
            {'name': 'Pancakes Proteici', 'calories': 400, 'protein': 25, 'carbs': 45, 'fat': 12, 'fiber': 3, 'type': 'breakfast', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},
            {'name': 'Smoothie Bowl', 'calories': 300, 'protein': 8, 'carbs': 50, 'fat': 8, 'fiber': 7, 'type': 'breakfast', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Uova Strapazzate con Pane', 'calories': 380, 'protein': 20, 'carbs': 30, 'fat': 20, 'fiber': 2, 'type': 'breakfast', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},
            {'name': 'Muesli con Latte', 'calories': 350, 'protein': 12, 'carbs': 55, 'fat': 10, 'fiber': 5, 'type': 'breakfast', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},
            {'name': 'Cornetto e Cappuccino', 'calories': 420, 'protein': 8, 'carbs': 50, 'fat': 22, 'fiber': 1, 'type': 'breakfast', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},
            {'name': 'Overnight Oats', 'calories': 340, 'protein': 12, 'carbs': 52, 'fat': 10, 'fiber': 6, 'type': 'breakfast', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},
            {'name': 'Fette Biscottate con Marmellata', 'calories': 250, 'protein': 5, 'carbs': 48, 'fat': 5, 'fiber': 2, 'type': 'breakfast', 'contains_lactose': False, 'contains_gluten': True, 'vegetarian': True, 'vegan': True},

            # PRIMI
            {'name': 'Carbonara', 'calories': 700, 'protein': 25, 'carbs': 70, 'fat': 35, 'fiber': 2, 'type': 'main', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': False, 'vegan': False},
            {'name': 'Mac and Cheese', 'calories': 800, 'protein': 22, 'carbs': 75, 'fat': 45, 'fiber': 2, 'type': 'main', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},
            {'name': 'Pasta Pomodoro', 'calories': 450, 'protein': 12, 'carbs': 80, 'fat': 10, 'fiber': 4, 'type': 'main', 'contains_lactose': False, 'contains_gluten': True, 'vegetarian': True, 'vegan': True},
            {'name': 'Pasta al Pesto', 'calories': 550, 'protein': 15, 'carbs': 70, 'fat': 25, 'fiber': 3, 'type': 'main', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},
            {'name': 'Risotto ai Funghi', 'calories': 480, 'protein': 10, 'carbs': 75, 'fat': 15, 'fiber': 3, 'type': 'main', 'contains_lactose': True, 'contains_gluten': False, 'vegetarian': True, 'vegan': False},
            {'name': 'Riso al Curry', 'calories': 400, 'protein': 8, 'carbs': 70, 'fat': 10, 'fiber': 4, 'type': 'main', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Lasagna', 'calories': 850, 'protein': 35, 'carbs': 65, 'fat': 50, 'fiber': 4, 'type': 'main', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': False, 'vegan': False},
            {'name': 'Zuppa di Legumi', 'calories': 320, 'protein': 18, 'carbs': 45, 'fat': 8, 'fiber': 12, 'type': 'main', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Minestrone', 'calories': 180, 'protein': 6, 'carbs': 30, 'fat': 5, 'fiber': 8, 'type': 'main', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Pizza Margherita', 'calories': 900, 'protein': 30, 'carbs': 100, 'fat': 40, 'fiber': 4, 'type': 'main', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},
            {'name': 'Sushi Mix (12 pz)', 'calories': 400, 'protein': 18, 'carbs': 60, 'fat': 10, 'fiber': 2, 'type': 'main', 'contains_lactose': False, 'contains_gluten': True, 'vegetarian': False, 'vegan': False},
            {'name': 'Quinoa Bowl', 'calories': 350, 'protein': 14, 'carbs': 50, 'fat': 12, 'fiber': 6, 'type': 'main', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Pasta Integrale Verdure', 'calories': 380, 'protein': 14, 'carbs': 65, 'fat': 8, 'fiber': 8, 'type': 'main', 'contains_lactose': False, 'contains_gluten': True, 'vegetarian': True, 'vegan': True},
            {'name': 'Ravioli Burro Salvia', 'calories': 520, 'protein': 18, 'carbs': 55, 'fat': 25, 'fiber': 2, 'type': 'main', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},
            {'name': 'Gnocchi al Sugo', 'calories': 420, 'protein': 10, 'carbs': 75, 'fat': 10, 'fiber': 3, 'type': 'main', 'contains_lactose': False, 'contains_gluten': True, 'vegetarian': True, 'vegan': True},
            {'name': 'Pasta e Fagioli', 'calories': 450, 'protein': 20, 'carbs': 70, 'fat': 10, 'fiber': 10, 'type': 'main', 'contains_lactose': False, 'contains_gluten': True, 'vegetarian': True, 'vegan': True},
            {'name': 'Risotto alla Milanese', 'calories': 520, 'protein': 12, 'carbs': 80, 'fat': 18, 'fiber': 2, 'type': 'main', 'contains_lactose': True, 'contains_gluten': False, 'vegetarian': True, 'vegan': False},
            {'name': 'Spaghetti Aglio Olio', 'calories': 500, 'protein': 12, 'carbs': 75, 'fat': 18, 'fiber': 3, 'type': 'main', 'contains_lactose': False, 'contains_gluten': True, 'vegetarian': True, 'vegan': True},
            {'name': 'Poke Bowl', 'calories': 480, 'protein': 28, 'carbs': 55, 'fat': 18, 'fiber': 5, 'type': 'main', 'contains_lactose': False, 'contains_gluten': True, 'vegetarian': False, 'vegan': False},
            {'name': 'Farro con Verdure', 'calories': 380, 'protein': 12, 'carbs': 65, 'fat': 10, 'fiber': 8, 'type': 'main', 'contains_lactose': False, 'contains_gluten': True, 'vegetarian': True, 'vegan': True},
            {'name': 'Couscous Vegetariano', 'calories': 420, 'protein': 14, 'carbs': 70, 'fat': 12, 'fiber': 7, 'type': 'main', 'contains_lactose': False, 'contains_gluten': True, 'vegetarian': True, 'vegan': True},
            {'name': 'Pasta alle Vongole', 'calories': 480, 'protein': 22, 'carbs': 68, 'fat': 14, 'fiber': 2, 'type': 'main', 'contains_lactose': False, 'contains_gluten': True, 'vegetarian': False, 'vegan': False},
            {'name': 'Risotto ai Frutti di Mare', 'calories': 520, 'protein': 25, 'carbs': 70, 'fat': 16, 'fiber': 2, 'type': 'main', 'contains_lactose': True, 'contains_gluten': False, 'vegetarian': False, 'vegan': False},
            {'name': 'Polenta con Funghi', 'calories': 350, 'protein': 8, 'carbs': 55, 'fat': 12, 'fiber': 4, 'type': 'main', 'contains_lactose': True, 'contains_gluten': False, 'vegetarian': True, 'vegan': False},

            # SECONDI
            {'name': 'Grilled Chicken', 'calories': 400, 'protein': 45, 'carbs': 5, 'fat': 22, 'fiber': 0, 'type': 'second', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': False, 'vegan': False},
            {'name': 'Tofu Salad', 'calories': 300, 'protein': 20, 'carbs': 15, 'fat': 20, 'fiber': 5, 'type': 'second', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Bistecca ai Ferri', 'calories': 350, 'protein': 40, 'carbs': 0, 'fat': 20, 'fiber': 0, 'type': 'second', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': False, 'vegan': False},
            {'name': 'Pollo alle Mandorle', 'calories': 450, 'protein': 35, 'carbs': 15, 'fat': 28, 'fiber': 3, 'type': 'second', 'contains_lactose': False, 'contains_gluten': True, 'vegetarian': False, 'vegan': False},
            {'name': 'Insalata di Mare', 'calories': 250, 'protein': 28, 'carbs': 8, 'fat': 12, 'fiber': 2, 'type': 'second', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': False, 'vegan': False},
            {'name': 'Salmone alla Griglia', 'calories': 380, 'protein': 35, 'carbs': 2, 'fat': 25, 'fiber': 0, 'type': 'second', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': False, 'vegan': False},
            {'name': 'Omelette', 'calories': 220, 'protein': 15, 'carbs': 2, 'fat': 17, 'fiber': 0, 'type': 'second', 'contains_lactose': True, 'contains_gluten': False, 'vegetarian': True, 'vegan': False},
            {'name': 'Hamburger (no bun)', 'calories': 300, 'protein': 28, 'carbs': 3, 'fat': 20, 'fiber': 0, 'type': 'second', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': False, 'vegan': False},
            {'name': 'Polpette al Sugo', 'calories': 350, 'protein': 25, 'carbs': 15, 'fat': 22, 'fiber': 2, 'type': 'second', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': False, 'vegan': False},
            {'name': 'Merluzzo al Vapore', 'calories': 180, 'protein': 30, 'carbs': 2, 'fat': 5, 'fiber': 0, 'type': 'second', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': False, 'vegan': False},
            {'name': 'Caprese (Mozzarella)', 'calories': 320, 'protein': 18, 'carbs': 5, 'fat': 25, 'fiber': 1, 'type': 'second', 'contains_lactose': True, 'contains_gluten': False, 'vegetarian': True, 'vegan': False},
            {'name': 'Uova Sode (2)', 'calories': 155, 'protein': 13, 'carbs': 1, 'fat': 11, 'fiber': 0, 'type': 'second', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': False},
            {'name': 'Parmigiana di Melanzane', 'calories': 600, 'protein': 20, 'carbs': 25, 'fat': 48, 'fiber': 6, 'type': 'second', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},
            {'name': 'Seitan alla Piastra', 'calories': 200, 'protein': 30, 'carbs': 8, 'fat': 5, 'fiber': 1, 'type': 'second', 'contains_lactose': False, 'contains_gluten': True, 'vegetarian': True, 'vegan': True},
            {'name': 'Petto di Tacchino', 'calories': 280, 'protein': 40, 'carbs': 0, 'fat': 12, 'fiber': 0, 'type': 'second', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': False, 'vegan': False},
            {'name': 'Tonno alla Piastra', 'calories': 320, 'protein': 38, 'carbs': 0, 'fat': 18, 'fiber': 0, 'type': 'second', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': False, 'vegan': False},
            {'name': 'Scaloppine al Limone', 'calories': 380, 'protein': 32, 'carbs': 10, 'fat': 24, 'fiber': 0, 'type': 'second', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': False, 'vegan': False},
            {'name': 'Burger di Lenticchie', 'calories': 280, 'protein': 18, 'carbs': 35, 'fat': 10, 'fiber': 8, 'type': 'second', 'contains_lactose': False, 'contains_gluten': True, 'vegetarian': True, 'vegan': True},
            {'name': 'Tempeh Marinato', 'calories': 250, 'protein': 22, 'carbs': 12, 'fat': 14, 'fiber': 4, 'type': 'second', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Cotoletta di Pollo', 'calories': 450, 'protein': 35, 'carbs': 20, 'fat': 28, 'fiber': 1, 'type': 'second', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': False, 'vegan': False},
            {'name': 'Spigola al Forno', 'calories': 220, 'protein': 32, 'carbs': 2, 'fat': 10, 'fiber': 0, 'type': 'second', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': False, 'vegan': False},
            {'name': 'Frittata di Verdure', 'calories': 280, 'protein': 18, 'carbs': 10, 'fat': 20, 'fiber': 3, 'type': 'second', 'contains_lactose': True, 'contains_gluten': False, 'vegetarian': True, 'vegan': False},
            {'name': 'Falafel (6 pz)', 'calories': 350, 'protein': 15, 'carbs': 40, 'fat': 16, 'fiber': 6, 'type': 'second', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},

            # CONTORNI
            {'name': 'Insalata Mista', 'calories': 80, 'protein': 3, 'carbs': 10, 'fat': 4, 'fiber': 4, 'type': 'side', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Verdure Grigliate', 'calories': 120, 'protein': 4, 'carbs': 15, 'fat': 6, 'fiber': 5, 'type': 'side', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Patate al Forno', 'calories': 200, 'protein': 4, 'carbs': 40, 'fat': 4, 'fiber': 4, 'type': 'side', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Spinaci Saltati', 'calories': 90, 'protein': 5, 'carbs': 8, 'fat': 5, 'fiber': 4, 'type': 'side', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Broccoli al Vapore', 'calories': 55, 'protein': 4, 'carbs': 8, 'fat': 1, 'fiber': 4, 'type': 'side', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Caponata', 'calories': 150, 'protein': 3, 'carbs': 18, 'fat': 8, 'fiber': 5, 'type': 'side', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Purè di Patate', 'calories': 180, 'protein': 4, 'carbs': 28, 'fat': 7, 'fiber': 2, 'type': 'side', 'contains_lactose': True, 'contains_gluten': False, 'vegetarian': True, 'vegan': False},
            {'name': 'Fagioli Lessati', 'calories': 140, 'protein': 9, 'carbs': 22, 'fat': 1, 'fiber': 7, 'type': 'side', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Zucchine Trifolate', 'calories': 100, 'protein': 3, 'carbs': 10, 'fat': 6, 'fiber': 3, 'type': 'side', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},

            # SNACK
            {'name': 'Yogurt', 'calories': 120, 'protein': 10, 'carbs': 12, 'fat': 4, 'fiber': 0, 'type': 'snack', 'contains_lactose': True, 'contains_gluten': False, 'vegetarian': True, 'vegan': False},
            {'name': 'Mela', 'calories': 52, 'protein': 0, 'carbs': 14, 'fat': 0, 'fiber': 2, 'type': 'snack', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Banana', 'calories': 89, 'protein': 1, 'carbs': 23, 'fat': 0, 'fiber': 3, 'type': 'snack', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Mandorle (30g)', 'calories': 170, 'protein': 6, 'carbs': 6, 'fat': 15, 'fiber': 3, 'type': 'snack', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Barretta Energetica', 'calories': 200, 'protein': 8, 'carbs': 28, 'fat': 8, 'fiber': 3, 'type': 'snack', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},
            {'name': 'Cioccolato Fondente (20g)', 'calories': 110, 'protein': 2, 'carbs': 10, 'fat': 8, 'fiber': 2, 'type': 'snack', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Avocado Toast', 'calories': 280, 'protein': 6, 'carbs': 25, 'fat': 18, 'fiber': 7, 'type': 'snack', 'contains_lactose': False, 'contains_gluten': True, 'vegetarian': True, 'vegan': True},
            {'name': 'Smoothie Frutti Bosco', 'calories': 140, 'protein': 3, 'carbs': 30, 'fat': 2, 'fiber': 4, 'type': 'snack', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Noci (20g)', 'calories': 130, 'protein': 3, 'carbs': 3, 'fat': 13, 'fiber': 1, 'type': 'snack', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Crackers Integrali (6 pz)', 'calories': 120, 'protein': 3, 'carbs': 20, 'fat': 4, 'fiber': 3, 'type': 'snack', 'contains_lactose': False, 'contains_gluten': True, 'vegetarian': True, 'vegan': True},
            {'name': 'Hummus con Verdure', 'calories': 180, 'protein': 8, 'carbs': 18, 'fat': 10, 'fiber': 5, 'type': 'snack', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Parmigiano (30g)', 'calories': 120, 'protein': 10, 'carbs': 0, 'fat': 9, 'fiber': 0, 'type': 'snack', 'contains_lactose': True, 'contains_gluten': False, 'vegetarian': True, 'vegan': False},
            {'name': 'Edamame (100g)', 'calories': 120, 'protein': 11, 'carbs': 9, 'fat': 5, 'fiber': 5, 'type': 'snack', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Arancia', 'calories': 62, 'protein': 1, 'carbs': 15, 'fat': 0, 'fiber': 3, 'type': 'snack', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Barretta Proteica', 'calories': 220, 'protein': 20, 'carbs': 22, 'fat': 8, 'fiber': 2, 'type': 'snack', 'contains_lactose': True, 'contains_gluten': False, 'vegetarian': True, 'vegan': False},
            {'name': 'Frutta Secca Mix (40g)', 'calories': 200, 'protein': 5, 'carbs': 10, 'fat': 18, 'fiber': 2, 'type': 'snack', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},

            # DESSERT
            {'name': 'Fruit Salad', 'calories': 150, 'protein': 2, 'carbs': 35, 'fat': 1, 'fiber': 4, 'type': 'dessert', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Tiramisù', 'calories': 350, 'protein': 8, 'carbs': 40, 'fat': 18, 'fiber': 0, 'type': 'dessert', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},
            {'name': 'Gelato', 'calories': 250, 'protein': 4, 'carbs': 30, 'fat': 14, 'fiber': 0, 'type': 'dessert', 'contains_lactose': True, 'contains_gluten': False, 'vegetarian': True, 'vegan': False},
            {'name': 'Biscotti (3)', 'calories': 150, 'protein': 2, 'carbs': 22, 'fat': 6, 'fiber': 1, 'type': 'dessert', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},
            {'name': 'Panna Cotta', 'calories': 280, 'protein': 4, 'carbs': 25, 'fat': 18, 'fiber': 0, 'type': 'dessert', 'contains_lactose': True, 'contains_gluten': False, 'vegetarian': True, 'vegan': False},
            {'name': 'Sorbetto al Limone', 'calories': 120, 'protein': 0, 'carbs': 30, 'fat': 0, 'fiber': 0, 'type': 'dessert', 'contains_lactose': False, 'contains_gluten': False, 'vegetarian': True, 'vegan': True},
            {'name': 'Cheesecake', 'calories': 400, 'protein': 8, 'carbs': 35, 'fat': 26, 'fiber': 1, 'type': 'dessert', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},
            {'name': 'Mousse al Cioccolato', 'calories': 320, 'protein': 5, 'carbs': 32, 'fat': 20, 'fiber': 2, 'type': 'dessert', 'contains_lactose': True, 'contains_gluten': False, 'vegetarian': True, 'vegan': False},
            {'name': 'Torta di Mele', 'calories': 280, 'protein': 3, 'carbs': 45, 'fat': 10, 'fiber': 2, 'type': 'dessert', 'contains_lactose': True, 'contains_gluten': True, 'vegetarian': True, 'vegan': False},
            {'name': 'Cantucci (3 pz)', 'calories': 150, 'protein': 4, 'carbs': 24, 'fat': 5, 'fiber': 1, 'type': 'dessert', 'contains_lactose': False, 'contains_gluten': True, 'vegetarian': True, 'vegan': True}
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
        """Risolve il CSP per trovare un piano alimentare ottimale."""
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
            meal_vars = ["Breakfast", "Lunch", "LunchSecond", "Dinner", "MorningSnack", "AfternoonSnack"]
            
            if recipes_by_type['breakfast']:
                problem.addVariable("Breakfast", recipes_by_type['breakfast'])
            else:
                problem.addVariable("Breakfast", list(range(len(available_recipes))))
            
            main_domain = recipes_by_type['main'] if recipes_by_type['main'] else list(range(len(available_recipes)))
            problem.addVariable("Lunch", main_domain)
            problem.addVariable("Dinner", main_domain)
            
            second_domain = recipes_by_type['second'] if recipes_by_type['second'] else list(range(len(available_recipes)))
            problem.addVariable("LunchSecond", second_domain)
            
            snack_domain = recipes_by_type['snack'] + recipes_by_type['dessert']
            if not snack_domain:
                snack_domain = list(range(len(available_recipes)))
            problem.addVariable("MorningSnack", snack_domain)
            problem.addVariable("AfternoonSnack", snack_domain)

        else:
            meal_vars = ["Lunch", "Dinner", "Snack"]
            
            lunch_dinner_domain = recipes_by_type['main'] + recipes_by_type['second']
            if not lunch_dinner_domain:
                lunch_dinner_domain = list(range(len(available_recipes)))
            
            snack_domain = recipes_by_type['snack'] + recipes_by_type['dessert']
            if not snack_domain:
                snack_domain = list(range(len(available_recipes)))
            
            problem.addVariable("Lunch", lunch_dinner_domain)
            problem.addVariable("Dinner", lunch_dinner_domain)
            problem.addVariable("Snack", snack_domain)

        tolerance = max(50, min(300, int(target_calories * 0.15)))

        def calorie_constraint(*meal_indices):
            total = sum(available_recipes[idx]['calories'] for idx in meal_indices)
            return (target_calories - tolerance) <= total <= (target_calories + tolerance)

        problem.addConstraint(calorie_constraint, meal_vars)

        if min_protein is not None:
            def protein_constraint(*meal_indices):
                total_protein = sum(available_recipes[idx].get('protein', 0) for idx in meal_indices)
                return total_protein >= min_protein
            problem.addConstraint(protein_constraint, meal_vars)

        if max_fat is not None:
            def fat_constraint(*meal_indices):
                total_fat = sum(available_recipes[idx].get('fat', 0) for idx in meal_indices)
                return total_fat <= max_fat
            problem.addConstraint(fat_constraint, meal_vars)

        if min_fiber is not None:
            def fiber_constraint(*meal_indices):
                total_fiber = sum(available_recipes[idx].get('fiber', 0) for idx in meal_indices)
                return total_fiber >= min_fiber
            problem.addConstraint(fiber_constraint, meal_vars)

        if num_meals == 5:
            problem.addConstraint(AllDifferentConstraint(), ["Lunch", "Dinner"])
            problem.addConstraint(AllDifferentConstraint(), ["MorningSnack", "AfternoonSnack"])
        else:
            problem.addConstraint(AllDifferentConstraint(), ["Lunch", "Dinner"])

        max_solutions_to_check = 50
        solutions = []
        
        try:
            solution_iter = problem.getSolutionIter()
            for idx, sol in enumerate(solution_iter):
                solutions.append(sol)
                if len(solutions) >= max_solutions_to_check:
                    break
        except StopIteration:
            pass
        except Exception:
            sol = problem.getSolution()
            if sol:
                solutions = [sol]

        if not solutions:
            return self._solve_greedy(target_calories, available_recipes, recipes_by_type, 
                                      meal_vars, num_meals, min_protein, max_fat, min_fiber)

        best_solution = None
        min_score = float('inf')

        for sol in solutions:
            total_cal = sum(available_recipes[sol[var]]['calories'] for var in meal_vars)
            total_protein = sum(available_recipes[sol[var]].get('protein', 0) for var in meal_vars)
            total_fiber = sum(available_recipes[sol[var]].get('fiber', 0) for var in meal_vars)
            
            cal_diff = abs(total_cal - target_calories)
            
            if target_calories > 1000:
                protein_bonus = max(0, 80 - total_protein) * 0.5
                fiber_bonus = max(0, 25 - total_fiber) * 0.5
            else:
                protein_bonus = 0
                fiber_bonus = 0
            
            score = cal_diff + protein_bonus + fiber_bonus
            
            if score < min_score:
                min_score = score
                best_solution = sol

        return self._build_result(best_solution, available_recipes, meal_vars, target_calories)
    
    def _solve_greedy(self, target_calories, available_recipes, recipes_by_type, 
                      meal_vars, num_meals, min_protein, max_fat, min_fiber):
        """Ricerca greedy come fallback."""
        import itertools
        
        domains = {}
        if num_meals == 5:
            domains['Breakfast'] = recipes_by_type['breakfast'] or list(range(len(available_recipes)))
            domains['Lunch'] = recipes_by_type['main'] or list(range(len(available_recipes)))
            domains['LunchSecond'] = recipes_by_type['second'] or list(range(len(available_recipes)))
            domains['Dinner'] = recipes_by_type['main'] or list(range(len(available_recipes)))
            snack_dom = recipes_by_type['snack'] + recipes_by_type['dessert']
            domains['MorningSnack'] = snack_dom or list(range(len(available_recipes)))
            domains['AfternoonSnack'] = snack_dom or list(range(len(available_recipes)))
        else:
            lunch_dinner_dom = recipes_by_type['main'] + recipes_by_type['second']
            domains['Lunch'] = lunch_dinner_dom or list(range(len(available_recipes)))
            domains['Dinner'] = lunch_dinner_dom or list(range(len(available_recipes)))
            snack_dom = recipes_by_type['snack'] + recipes_by_type['dessert']
            domains['Snack'] = snack_dom or list(range(len(available_recipes)))
        
        best_solution = None
        min_diff = float('inf')
        
        max_combinations = 10000
        count = 0
        
        domain_lists = [domains[var] for var in meal_vars]
        
        for combo in itertools.product(*domain_lists):
            count += 1
            if count > max_combinations:
                break
            
            if num_meals == 5:
                lunch_idx = meal_vars.index('Lunch')
                dinner_idx = meal_vars.index('Dinner')
                if combo[lunch_idx] == combo[dinner_idx]:
                    continue
                morning_idx = meal_vars.index('MorningSnack')
                afternoon_idx = meal_vars.index('AfternoonSnack')
                if combo[morning_idx] == combo[afternoon_idx]:
                    continue
            else:
                lunch_idx = meal_vars.index('Lunch')
                dinner_idx = meal_vars.index('Dinner')
                if combo[lunch_idx] == combo[dinner_idx]:
                    continue
            
            total_cal = sum(available_recipes[idx]['calories'] for idx in combo)
            cal_diff = abs(total_cal - target_calories)
            
            if min_protein is not None:
                total_protein = sum(available_recipes[idx].get('protein', 0) for idx in combo)
                if total_protein < min_protein:
                    continue
            if max_fat is not None:
                total_fat = sum(available_recipes[idx].get('fat', 0) for idx in combo)
                if total_fat > max_fat:
                    continue
            if min_fiber is not None:
                total_fiber = sum(available_recipes[idx].get('fiber', 0) for idx in combo)
                if total_fiber < min_fiber:
                    continue
            
            if cal_diff < min_diff:
                min_diff = cal_diff
                best_solution = dict(zip(meal_vars, combo))
        
        if best_solution:
            return self._build_result(best_solution, available_recipes, meal_vars, target_calories)
        return None
    
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
        """Info nutrizionali di una ricetta."""
        for r in self.recipes:
            if r['name'].lower() == recipe_name.lower():
                return r
        return None
    
    def suggest_alternatives(self, recipe_name, intolerances=[], dietary_preference=None):
        """Suggerisce ricette alternative simili."""
        original = self.get_recipe_info(recipe_name)
        if not original:
            return []
        
        available = self.filter_recipes(intolerances, dietary_preference)
        alternatives = []
        
        for r in available:
            if r['name'] != recipe_name and r['type'] == original['type']:
                cal_diff = abs(r['calories'] - original['calories'])
                if cal_diff <= 150:  # Alternative con calorie simili (+/- 150)
                    alternatives.append((r, cal_diff))
        
        # Ordina per differenza calorica
        alternatives.sort(key=lambda x: x[1])
        return [alt[0] for alt in alternatives[:5]]  # Restituisce le prime 5
