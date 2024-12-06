from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import sklearn
from dotenv import load_dotenv
import os


app = Flask(__name__)

# Configuration des parametres pour le deploiment
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')
# Chargement du modèle
with open('../Models/model_pipeline_v1.pkl', 'rb') as f:
    model_pipeline = joblib.load(f)


@app.route('/predict', methods=['POST'])
def predict():
    json_ = request.json
    query_df = pd.DataFrame(json_)

    # Obtenir les prédictions
    y_reg_pred = model_pipeline.predict(query_df)

    # Convertir les prédictions en listes
    return jsonify({
        'prediction': y_reg_pred[0]
    })


if __name__ == "__main__":
    app.run()
