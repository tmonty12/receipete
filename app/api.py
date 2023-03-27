import requests


def query_ingredients(query):
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/ingredients/search"

    querystring = {"query": query, "number": "10"}

    headers = {
        "X-RapidAPI-Key": "2d4a8dd1fdmsh729ea9408c304cep1e20afjsn8778ac3491bf",
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    response.raise_for_status()

    return response.json()['results']


def query_recipes(ingredients, time):
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"

    querystring = {"ingredients": ingredients, "number": "10", "ignorePantry": "true", "ranking": "1"}

    headers = {
        "X-RapidAPI-Key": "2d4a8dd1fdmsh729ea9408c304cep1e20afjsn8778ac3491bf",
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    response.raise_for_status()

    return response.json()


def query_recipes_2(ingredients, time):
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/complexSearch"

    querystring = {"query": "", "includeIngredients": ingredients, "number": "10", "ignorePantry": "true", "ranking": "1", "maxReadyTime":time}

    headers = {
        "X-RapidAPI-Key": "2d4a8dd1fdmsh729ea9408c304cep1e20afjsn8778ac3491bf",
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    response.raise_for_status()

    return response.json()


def query_recipe_information(id):
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/" + id + "/information"

    headers = {
        "X-RapidAPI-Key": "2d4a8dd1fdmsh729ea9408c304cep1e20afjsn8778ac3491bf",
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)

    response.raise_for_status()

    return response.json()

# List storing allergies provided by API
allergies = ['dairy', 'egg', 'gluten', 'peanut', 'sesame', 'seafood', 'shellfish', 'soy', 'sulfite', 'tree nut', 'wheat']


if __name__ == "__main__":
    # print(query_recipes_2('tomato,cheese'))
    # print(query_recipe_ingredients('474396'))
    print(query_recipe_information('218125')['extendedIngredients'])
