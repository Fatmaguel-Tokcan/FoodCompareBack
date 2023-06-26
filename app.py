from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

df = pd.read_csv('RAW_recipes.csv')
print(df.head())

@app.route('/api/gericht', methods=['GET'])
def get_gericht():
    name = request.args.get('name')
    if name is None:
        return jsonify({'error': 'Gerichtsname nicht angegeben.'}), 400

    gericht_data = df.loc[df['name'] == name]
    if gericht_data.empty:
        return jsonify({'error': 'Gericht nicht gefunden.'}), 404

    gericht = {
        'name': name,
        'minutes': gericht_data['minutes'].values[0],
        'tags': gericht_data['tags'].values[0],
        'nutrition': gericht_data['nutrition'].values[0],
        'steps': gericht_data['steps'].values[0],
        'description': gericht_data['description'].values[0],
        'ingredients': gericht_data['ingredients'].values[0],
    }

    return jsonify(gericht)

@app.route('/api/gerichte', methods=['GET'])
def get_gerichte():
    gerichte_data = df.to_dict('records')
    if len(gerichte_data) == 0:
        return jsonify({'error': 'Keine Gerichte gefunden.'}), 404

    return jsonify(gerichte_data)

@app.route('/api/zutaten/<name>', methods=['GET'])
def get_zutaten(name):
    zutaten_data = df.loc[df['name'] == name, 'ingredients'].values
    if len(zutaten_data) == 0:
        return jsonify({'error': 'Gericht nicht gefunden.'}), 404

    zutaten = zutaten_data[0].split(',')
    response = jsonify(zutaten)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

if __name__ == '__main__':
    app.run(port=8000, debug=True)
