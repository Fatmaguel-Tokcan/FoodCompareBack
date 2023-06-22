from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS, cross_origin

app = Flask(__name__)

CORS(app, resources={r"/": {"origins": "http://localhost:8081", "headers": "", "methods": "*"}})


df = pd.read_csv('RAW_recipes.csv')
print(df.head())


@app.route('/gericht', methods=['GET'])
def get_gericht():
    gericht_id = request.args.get('id')
    gericht_data = df.loc[df['id'] == int(gericht_id)]
    if gericht_data.empty:
        return jsonify({'error': 'Gericht nicht gefunden.'}), 404
    
    gericht = {
        'id': gericht_id,
        'name': gericht_data['name'].values[0],
        'minutes': gericht_data['minutes'].values[0],
        'tags': gericht_data['tags'].values[0],
        'nutrition': gericht_data['nutrition'].values[0],
        'steps': gericht_data['steps'].values[0],
        'description': gericht_data['description'].values[0],
        'ingredients': gericht_data['ingredients'].values[0],

    }
    return jsonify(gericht)

@app.route('/zutaten', methods=['GET'])
def get_zutaten():
    gericht_id = request.args.get('id')
    zutaten_data = df.loc[df['id'] == int(gericht_id), 'ingredients'].values[0]
    if not zutaten_data:
        return jsonify({'error': 'Gericht nicht gefunden.'}), 404
    
    zutaten = zutaten_data.split(',')
    return jsonify(zutaten)

if __name__ == '_main_':
    app.run(debug=True)