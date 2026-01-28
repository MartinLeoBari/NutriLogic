% --- Lista Ingredienti ---
% ingredient(Name, Type, CaloriesPer100g).
ingredient(chicken, meat, 165).
ingredient(beef, meat, 250).
ingredient(tofu, vegetable, 76).
ingredient(milk, dairy, 42).
ingredient(cheese, dairy, 402).
ingredient(pasta, grain, 131).
ingredient(tomato, vegetable, 18).
ingredient(egg, animal_product, 155).

% --- Le Mie Ricette ---
% recipe(Name, ListOfIngredients).
recipe(carbonara, [pasta, egg, cheese, beef]). % Uso manzo per semplicità al posto del guanciale
recipe(grilled_chicken, [chicken, tomato]).
recipe(tofu_salad, [tofu, tomato]).
recipe(mac_and_cheese, [pasta, cheese, milk]).
recipe(pasta_pomodoro, [pasta, tomato]).

% --- Regole Logiche ---

% C'è carne o derivati?
contains_animal_product(Recipe) :-
    recipe(Recipe, Ingredients),
    member(Ing, Ingredients),
    (ingredient(Ing, meat, _); ingredient(Ing, dairy, _); ingredient(Ing, animal_product, _)).

% Ci sono latticini?
contains_dairy(Recipe) :-
    recipe(Recipe, Ingredients),
    member(Ing, Ingredients),
    ingredient(Ing, dairy, _).

% È Vegano?
is_vegan(Recipe) :-
    \+ contains_animal_product(Recipe).

% È sicuro da mangiare per chi ha intolleranze?
% safe_for(Recipe, Intolerance)
safe_for(Recipe, lactose) :-
    \+ contains_dairy(Recipe).

safe_for(Recipe, vegetarian) :-
    recipe(Recipe, Ingredients),
    \+ (member(Ing, Ingredients), ingredient(Ing, meat, _)).

% Calcolo calorie (metodo semplificato)
recipe_calories(Recipe, TotalCal) :-
    recipe(Recipe, Ingredients),
    calculate_cal(Ingredients, TotalCal).

calculate_cal([], 0).
calculate_cal([Ing|Tail], Tot) :-
    ingredient(Ing, _, Cal),
    calculate_cal(Tail, SubTot),
    Tot is Cal + SubTot.
