import json
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from googleapiclient import discovery


class Ingredient:
    def __init__(self, name, amount, unit):
        self.name = name
        self.amount = amount
        self.unit = unit


class Recipe:
    def __init__(self, name):
        self.name = name
        self.ingredients = []

    def add_ingredients(self, name, amount, unit):
        self.ingredients.append(Ingredient(name, amount, unit))


def get_data(spreadsheet_id, _range):
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=_range).execute()
    values = result.get('values', [])
    return values


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
recipes_dict = {}
current_recipe = None
shopping_list = {}
value_range = []
list_range = 'List!A2:C'
body = {
    'range': list_range,
    'majorDimension': 'ROWS',
    'values': value_range
}

with open('secret.json') as data_file:
    data = json.load(data_file)
    spreadsheet_id = data["spreadsheet_id"]

# Authentication
credentials = ServiceAccountCredentials.from_json_keyfile_name('secret.json', scopes=SCOPES)
http_auth = credentials.authorize(Http())
discoveryUrl = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
service = discovery.build('sheets', 'v4', http=http_auth, discoveryServiceUrl=discoveryUrl)

# Get data from sheet
menu = get_data(spreadsheet_id, 'Menu!C2:D')
recipes = get_data(spreadsheet_id, 'Recipes!A2:D')

# Prepare recipes
for recipe in recipes:
    if recipe[0]:
        current_recipe = Recipe(recipe[0])
        current_recipe.add_ingredients(recipe[1], recipe[2], recipe[3])
        recipes_dict[recipe[0]] = current_recipe
    if not recipe[0]:
        current_recipe.add_ingredients(recipe[1], recipe[2], recipe[3])

# Get ingredients for given menu
for item in menu:
    if item[1] != 'ANO':
        for ingredient in recipes_dict[item[0]].ingredients:
            if ingredient.name not in shopping_list:
                shopping_list.update({ingredient.name: [int(ingredient.amount), ingredient.unit]})
            else:
                shopping_list[ingredient.name][0] += int(ingredient.amount)

# Data preparation for update
for key in shopping_list:
    value_range.append([key, shopping_list[key][0], shopping_list[key][1]])

# Update list with shopping list
service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=list_range, valueInputOption="RAW",
                                       body=body).execute()

