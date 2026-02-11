% --- Knowledge Base NutriLogic ---

% --- 1. FATTI: Ingredienti ---
% ingredient(Name, MacroCategory, CaloriesPer100g).
% MacroCategory: meat, dairy, vegetable, fruit, grain, fish, legume, fat, unknown.

% Carni
ingredient(chicken, meat, 165).
ingredient(beef, meat, 250).
ingredient(pork, meat, 242).
ingredient(turkey, meat, 189).
ingredient(lamb, meat, 294).
ingredient(bacon, meat, 541).

% Pesce
ingredient(salmon, fish, 208).
ingredient(tuna, fish, 132).
ingredient(cod, fish, 82).
ingredient(shrimp, fish, 99).
ingredient(seabass, fish, 97).

% Latticini & Uova
ingredient(milk, dairy, 42).
ingredient(cheese, dairy, 402).
ingredient(yogurt, dairy, 59).
ingredient(egg, animal_product, 155).
ingredient(butter, dairy, 717).
ingredient(cream, dairy, 340).
ingredient(parmesan, dairy, 431).

% Cereali & Granaglie
ingredient(pasta, grain, 131).
ingredient(rice, grain, 130).
ingredient(oats, grain, 389).
ingredient(quinoa, grain, 120).
ingredient(bread, grain, 265).
ingredient(flour, grain, 364).

% Verdure
ingredient(tomato, vegetable, 18).
ingredient(lettuce, vegetable, 15).
ingredient(carrot, vegetable, 41).
ingredient(cucumber, vegetable, 16).
ingredient(broccoli, vegetable, 34).
ingredient(spinach, vegetable, 23).
ingredient(potato, vegetable, 77).
ingredient(onion, vegetable, 40).
ingredient(pepper, vegetable, 20).
ingredient(zucchini, vegetable, 17).
ingredient(eggplant, vegetable, 25).
ingredient(pumpkin, vegetable, 26).

% Frutta
ingredient(apple, fruit, 52).
ingredient(banana, fruit, 89).
ingredient(orange, fruit, 47).
ingredient(strawberry, fruit, 32).
ingredient(blueberry, fruit, 57).

% Legumi & Derivati
ingredient(tofu, legume, 76).
ingredient(beans, legume, 347).
ingredient(lentils, legume, 116).
ingredient(chickpeas, legume, 164).
ingredient(edamame, legume, 121).

% Altro
ingredient(oil, fat, 884).
ingredient(sugar, sweet, 387).
ingredient(honey, sweet, 304).
ingredient(chocolate, sweet, 546).
ingredient(nuts, nut, 607).


% --- 2. FATTI: Stagionalità ---
% season(Ingredient, Season).
% Seasons: spring, summer, autumn, winter.

season(tomato, summer).
season(zucchini, summer).
season(eggplant, summer).
season(pepper, summer).
season(strawberry, spring).
season(pumpkin, autumn).
season(broccoli, winter).
season(spinach, winter).
season(orange, winter).
season(apple, autumn).
season(lettuce, spring).
season(cucumber, summer).
% Gli altri ingredienti sono considerati "evergreen" o disponibili tutto l'anno importati.


% --- 3. FATTI: Ricette ---
% recipe(Name, ListOfIngredients).
% Nomi allineati (ove possibile) con csp_planner.py

% Colazione
recipe(porridge_con_frutta, [oats, milk, banana, blueberry]).
recipe(toast_avocado, [bread, avocado, egg]). % Avocado mancante, aggiungo regola
recipe(pancakes_proteici, [flour, egg, milk, sugar]).
recipe(yogurt_greco_miele, [yogurt, honey, nuts]).

% Primi
recipe(carbonara, [pasta, egg, cheese, bacon]).
recipe(pasta_pomodoro, [pasta, tomato, oil, onion]).
recipe(risotto_funghi, [rice, mushroom, butter, parmesan]). % Mushroom mancante
recipe(mac_and_cheese, [pasta, cheese, milk, butter]).
recipe(pasta_pesto, [pasta, basil, oil, parmesan, nuts]). % Basil mancante
recipe(lasagna, [pasta, beef, tomato, cheese, milk]).
recipe(zuppa_legumi, [beans, lentils, chickpeas, carrots, onion]).

% Secondi
recipe(grilled_chicken, [chicken, oil]).
recipe(salmone_griglia, [salmon, oil, lemon]). % Lemon mancante
recipe(bistecca, [beef, oil]).
recipe(tofu_salad, [tofu, lettuce, tomato, cucumber]).
recipe(omelette, [egg, cheese, oil]).
recipe(polpette, [beef, egg, bread, tomato]).
recipe(merluzzo_vapore, [cod, oil]).
recipe(burger_lenticchie, [lentils, bread, onion, carrot]).

% Contorni
recipe(insalata_mista, [lettuce, tomato, carrot, cucumber]).
recipe(verdure_grigliate, [zucchini, eggplant, pepper]).
recipe(patate_forno, [potato, oil, rosemary]).
recipe(spinaci_saltati, [spinach, butter]).

% Snack/Dessert
recipe(mela, [apple]).
recipe(banana, [banana]).
recipe(cioccolato, [chocolate]).
recipe(fruit_salad, [apple, banana, orange, blueberry]).


% --- 4. REGOLE LOGICHE ---

% 4.1 Regole Dietetiche Base

% Contiene carne o derivati animali (escluso latte/uova per vegetariani, ma qui semplifichiamo)
contains_meat(Recipe) :-
    recipe(Recipe, Ingredients),
    member(Ing, Ingredients),
    ingredient(Ing, meat, _).

contains_fish(Recipe) :-
    recipe(Recipe, Ingredients),
    member(Ing, Ingredients),
    ingredient(Ing, fish, _).

contains_dairy(Recipe) :-
    recipe(Recipe, Ingredients),
    member(Ing, Ingredients),
    ingredient(Ing, dairy, _).

contains_eggs(Recipe) :-
    recipe(Recipe, Ingredients),
    member(Ing, Ingredients),
    ingredient(Ing, animal_product, _). % egg

% Definizione Vegana: Niente carne, pesce, latticini, uova
contains_animal_product(Recipe) :-
    contains_meat(Recipe);
    contains_fish(Recipe);
    contains_dairy(Recipe);
    contains_eggs(Recipe).

is_vegan(Recipe) :-
    \+ contains_animal_product(Recipe).

is_vegetarian(Recipe) :-
    \+ contains_meat(Recipe),
    \+ contains_fish(Recipe).

% Sicurezza Alimentare (Intolleranze)
safe_for(Recipe, lactose_intolerant) :-
    \+ contains_dairy(Recipe).

safe_for(Recipe, gluten_free) :-
    recipe(Recipe, Ingredients),
    \+ (member(Ing, Ingredients), ingredient(Ing, grain, _)). % Semplificazione: grain = glutine

safe_for(Recipe, nut_allergy) :-
    recipe(Recipe, Ingredients),
    \+ (member(Ing, Ingredients), ingredient(Ing, nut, _)).


% 4.2 Regole Avanzate: Piatto Completo
% Un piatto è completo se ha Carboidrati (grain), Proteine (meat/fish/legume/egg/dairy) e Verdure.
has_carb(Recipe) :-
    recipe(Recipe, Ingredients),
    member(Ing, Ingredients),
    ingredient(Ing, grain, _).

has_protein(Recipe) :-
    recipe(Recipe, Ingredients),
    member(Ing, Ingredients),
    (ingredient(Ing, meat, _); ingredient(Ing, fish, _); ingredient(Ing, legume, _); ingredient(Ing, animal_product, _); ingredient(Ing, dairy, _)).

has_veg(Recipe) :-
    recipe(Recipe, Ingredients),
    member(Ing, Ingredients),
    ingredient(Ing, vegetable, _).

complete_dish(Recipe) :-
    has_carb(Recipe),
    has_protein(Recipe),
    has_veg(Recipe).


% 4.3 Regole Avanzate: Stagionalità
% Una ricetta è "di stagione" se TUTTI i suoi ingredienti freschi (frutta/verdura) sono di quella stagione (o evergreens).
is_seasonal(Recipe, CurrentSeason) :-
    recipe(Recipe, Ingredients),
    forall(member(Ing, Ingredients), (
        (ingredient(Ing, vegetable, _); ingredient(Ing, fruit, _)) ->
        (season(Ing, CurrentSeason); \+ season(Ing, _)) % Se ha stagione, deve matchare. Se non ha stagione definite, ok.
        ; true % Se non è frutta/verdura, ok sempre
    )).


% 4.4 Regole Avanzate: Allergeni in Tracce (Gestione Rischio)
% Ipotizziamo che ingredienti prodotti in stabilimenti misti possano avere tracce.
% Fatti ipotetici di contaminazione
processed_in_mixed_facility(chocolate).
processed_in_mixed_facility(oats).

may_contain_traces(Recipe, Allergen) :-
    recipe(Recipe, Ingredients),
    member(Ing, Ingredients),
    processed_in_mixed_facility(Ing),
    % Mapping allergeni
    (Allergen = nuts ; Allergen = gluten). % Semplificazione: assumiamo rischio generico


% 4.5 Calcolo Calorie (Ricorsivo)
recipe_calories(Recipe, TotalCal) :-
    recipe(Recipe, Ingredients),
    calculate_cal(Ingredients, TotalCal).

calculate_cal([], 0).
calculate_cal([Ing|Tail], Tot) :-
    (ingredient(Ing, _, Cal) -> TrueCal = Cal ; TrueCal = 50), % Default 50 se ingrediente mancante
    calculate_cal(Tail, SubTot),
    Tot is TrueCal + SubTot.

