import requests

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/ingredients/search"

querystring = {"query":"yogurt", "number":"10"}

headers = {
	"X-RapidAPI-Key": "2d4a8dd1fdmsh729ea9408c304cep1e20afjsn8778ac3491bf",
	"X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)