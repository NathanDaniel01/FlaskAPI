from flask import Flask, jsonify, request
from http import HTTPStatus
import content
import config
#### INIT ####
app = Flask(__name__)
db=config.DB_TEST_NAME
recipes = []

#### int and find LENGTH ####
i = 1
length =  content.fetch_row_length(db) 
for i in range(1, length + 1):
    recipes.append(content.select_content_by_id(i,db))

#### Basic GET ####
@app.route('/recipes', methods=['GET'])
def get_recipes():
    return jsonify({'data': recipes})


@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = next((recipe for recipe in recipes if recipe['ContentID'] == recipe_id), None)
    if recipe:
        return jsonify(recipe)

    return jsonify({'message': 'recipe not found'}), HTTPStatus.NOT_FOUND

@app.route('/recipes/Group/<int:GroupID>', methods=['GET'])
def get_Group(GroupID):
    recipelist = []
    for recipe in recipes:
        if recipe['GroupID'] == GroupID:
            recipelist.append(recipe)
    if recipe:
        return jsonify(recipelist)

    return jsonify({'message': 'recipe not found'}), HTTPStatus.NOT_FOUND

@app.route('/recipes/Page/<int:PageID>', methods=['GET'])
def get_Page(PageID):
    recipelist = []
    for recipe in recipes:
        if recipe['PageID'] == PageID:
            recipelist.append(recipe)
    if recipe:
        return jsonify(recipelist)

    return jsonify({'message': 'recipe not found'}), HTTPStatus.NOT_FOUND

@app.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    GroupID = data.get("GroupID")
    ContentType = data.get('ContentType')
    ContentHeld = data.get('ContentHeld')
    PageID = data.get("PageID")

    recipe = {
        'ContentID': len(recipes) + 1,
        'GroupID': GroupID,
        'ContentType': ContentType,
        'ContentHeld': ContentHeld,
        'PageID': PageID
    }
    print(recipe)

    recipes.append(recipe)
    content.insert_content(recipe, db)
    return jsonify(recipe), HTTPStatus.CREATED

@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    recipe = next((recipe for recipe in recipes if recipe['ContentID'] == recipe_id), None)

    if not recipe:
        return jsonify({'message': 'recipe not found'}), HTTPStatus.NOT_FOUND

    data = request.get_json()
    recipe.update(
        {
        'GroupID': data.get("GroupID"),
        'ContentType': data.get('ContentType'),
        'ContentHeld': data.get('ContentHeld'),
        'PageID':  data.get('PageID')
        }
    )
    content.update_content_by_id(recipe_id,recipe, db)

    return jsonify(recipe)


if __name__ == '__main__':
    app.run()