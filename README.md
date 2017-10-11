# Cookbook
Cookbook is simple script that helps to prepare shopping list from given menu. Main idea is based on Google Drive Spreadsheet - 
spreadsheet works as UI. On one sheet list prepare your recipes with ingredients, second list should be your menu and last is list itself.
I strongly recommend use my prepared templates:
- cookbook_template.ods 

or
- cookbook_template.xlsx

because list names and ranges are hard coded. 

## Preparation
1. Make your Google Drive Spreadsheet based on template.
2. Make new project in console.cloud.google.com and generate credentials. For newbies like me I recommend first part of this tutorial:
- https://www.youtube.com/watch?v=vISRn5qFrkM
3. Save credetials as secret.json into same folder as cookbook.py.
4. Add "spreadsheet_id": spreadsheetId to secret.json where spreadsheetId is ID of your spreadsheet on Google Drive. 

## Running 
1. Prepare your recipes.
2. Add menu on Menu list.
3. Run cookbook.py.
4. Now go to drive on list List and there is your shopping list. 
