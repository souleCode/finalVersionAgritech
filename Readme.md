# AgriTech : Solution d'Intelligence Agricole
![image alt](https://github.com/souleCode/finalVersionAgritech/blob/2cba5886612ae06e1eb517e56a6188479d8ba647/agro.jpg)
## Présentation

AgriTech est une application avancée basée sur l'apprentissage automatique, conçue pour fournir des solutions innovantes aux défis agricoles. En exploitant des technologies de pointe, nous visons à soutenir les agriculteurs avec des insights intelligents et basés sur les données.

## Description du Projet
![image app](https://github.com/souleCode/finalVersionAgritech/blob/5ed86c17a9da567c43576f33216e11f8e08d41a3/home.PNG)

AgriTech répond à des besoins agricoles critiques grâce à trois fonctionnalités clés :
*Structure du modele de Production agricole (Recommandation et Prediction du rendement agricole)*
![image structure du modele de producttion](https://github.com/souleCode/finalVersionAgritech/blob/e53939f35f968ea0fa55badb11e4eb3b9e0221b0/strct_pred.png)


- Recommandation de Culture
- Prédiction de Production de Champ
- Reconnaissance des Maladies des Plantes

## Stack Technologique

### Machine Learning

- _Frameworks_ : TensorFlow, Scikit-learn
- _Sources de Données_ :
  - Plant Village
  - Roboflow

### Technologies Web

- _Backend_ : Node.js
- _Frontend_ :
  - React
  - React Native

## Fonctionnalités Principales

### 1. Système de Recommandation de Culture
![image recommandation](https://github.com/souleCode/finalVersionAgritech/blob/7eccaeb72d478a2d661c74733cd5a89cf493d74e/recomm.PNG)

#### Caractéristiques Utilisées

- _N_ : Teneur en azote du sol (kg/ha)
- _P_ : Teneur en phosphore du sol (kg/ha)
- _K_ : Teneur en potassium du sol (kg/ha)
- _Température_ : Température ambiante (°C)
- _Humidité_ : Taux d'humidité (%)
- _pH_ : Niveau de pH du sol
- _Pluviométrie_ : Quantité de précipitations (mm)

#### Modèles de Machine Learning Testés

- LightGBM
- Random Forest
- Support Vector Machine
- Réseau de Neurones
- Naïve Bayes

_Meilleur Modèle_ : Naïve Bayes avec 99% de précision

### 2. Prédiction de Production Agricole
![image prediction app](https://github.com/souleCode/finalVersionAgritech/blob/f50b6d1d45f5b878f423e4aa2bd635c82fc4f2f1/pred.PNG)

#### Caractéristiques Utilisées

- _Surface_ : Surface cultivée (hectares)
- _Produit_ : Type de culture
- _Année_ : Année de production
- _Rendement_ : Rendement par hectare (hectogrammes)
- _Pluviométrie Moyenne_ : Précipitations annuelles (mm)
- _Pesticides_ : Quantité de pesticides utilisés (tonnes)
- _Température Moyenne_ : Température moyenne (°C)

#### Machine Learning Models Tested

- Linear Regression
- Lasso
- Ridge
- K-Nearest Neighbors
- Decision Tree Regressor
- Random Forest Regressor
- Gradient Boosting
- XGBoost

_Meilleur Modèle_ : Random Forest

- Erreur Quadratique Moyenne : 9892.72
- Score R² : 0.9867

### 3. Reconnaissance et Recommandation de Traitement des Maladies des Plantes
![image sante vegetal](https://github.com/souleCode/finalVersionAgritech/blob/54d41bb5e0efd546018e43c5422d26ab95be5b1e/sante%20vege.jpg)

#### Reconnaissance des Maladies

- _Modèle_ : YOLOv5
- Entraîné sur divers jeux de données de maladies agricoles
- Classification précise des maladies à partir d'images

#### Recommandation de Traitement
![image structure du modele de traitement des maladies vegetales](https://github.com/souleCode/finalVersionAgritech/blob/58b73a96d45c1f837e8c1b71335a6efcb6ba2dda/Llma.png)

- Approche de Traitement du Langage Naturel
- Modèles avancés utilisés :
  - Llama 3.1 (70B-versatile) pour le traitement des données textuelles. En effet ce modele sera utilisé pour nous proposer un traitement des maladies detectées par notre modele YOLO. Ce modele a ete juste ete soumis a un prompt engineering car nous n'avons pas assez de données pour faire le RAG.
  - Groq pour l'optimisation des réponses

## Installation

### Prérequis

- Node.js (v14+)
- npm ou yarn
- Python (3.7+)
- TensorFlow
- Scikit-learn

### Étapes d'Installation

1. Cloner le dépôt
   bash
   git clone [https://github.com/votre-nom/agritech.git](https://github.com/souleCode/finalVersionAgritech)
   cd agritech

2. Installer les dépendances backend
   bash
   cd backend
   npm install

3. Installer les dépendances frontend
   bash
   cd ../frontend
   npm install

4. Configurer l'environnement machine learning
   bash
   pip install -r requirements.txt

## Contribution
 Ce projet est Open Source donc il reste ouvert a toute la communauté pour n'importe qu'elle modification ou retour constructif.
 Pour l'utiliser vous avez juste besoin de suivre les etapes suivantes:

1. Forker le dépôt
2. Créer une branche de fonctionnalité (git checkout -b feature/MaFantastiqueFonctionnalite)
3. Commiter vos modifications (git commit -m 'Ajout de MaFantastiqueFonctionnalite')
4. Pusher la branche (git push origin feature/MaFantastiqueFonctionnalite)
5. Ouvrir une Pull Request

## Licence

Distribué sous la Licence MIT. Voir LICENSE pour plus d'informations.

## Contact

Responsable du Projet : [TRAORE Souleymane & CHALI Malama]
Email : contact@agritech.com
Lien du Projet : [https://github.com/votre-nom/agritech](https://github.com/votre-nom/agritech)

## Remerciements

- Pr MASROUR Tawfik
- Plant Village
- Roboflow
- Communauté TensorFlow
- Contributeurs open-source

---

_Note_ : Ce projet est en développement actif. Les contributions et retours sont les bienvenus !
