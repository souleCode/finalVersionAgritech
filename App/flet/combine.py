import flet as ft
import requests

# Stockage temporaire pour la culture prédite sur la première page
predicted_culture = None

list_culture = [
    'Maize', 'Potatoes', 'Rice', 'paddy', 'Sorghum', 'Soybeans', 'Wheat',
    'Cassava', 'Sweet potatoes', 'Plantains and others', 'Yams'
]

list_pays = [
    'Albania', 'Algeria', 'Angola', 'Argentina', 'Armenia', 'Australia',
    'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Belarus',
    'Belgium', 'Botswana', 'Brazil', 'Bulgaria', 'Burkina Faso', 'Burundi',
    'Cameroon', 'Canada', 'Central African Republic', 'Chile', 'Colombia',
    'Croatia', 'Denmark', 'Dominican Republic', 'Ecuador', 'Egypt',
    'El Salvador', 'Eritrea', 'Estonia', 'Finland', 'France', 'Germany',
    'Ghana', 'Greece', 'Guatemala', 'Guinea', 'Guyana', 'Haiti', 'Honduras',
    'Hungary', 'India', 'Indonesia', 'Iraq', 'Ireland', 'Italy', 'Jamaica',
    'Japan', 'Kazakhstan', 'Kenya', 'Latvia', 'Lebanon', 'Lesotho', 'Libya',
    'Lithuania', 'Madagascar', 'Malawi', 'Malaysia', 'Mali', 'Mauritania',
    'Mauritius', 'Mexico', 'Montenegro', 'Morocco', 'Mozambique', 'Namibia',
    'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Norway',
    'Pakistan', 'Papua New Guinea', 'Peru', 'Poland', 'Portugal', 'Qatar',
    'Romania', 'Rwanda', 'Saudi Arabia', 'Senegal', 'Slovenia', 'South Africa',
    'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland',
    'Tajikistan', 'Thailand', 'Tunisia', 'Turkey', 'Uganda', 'Ukraine',
    'United Kingdom', 'Uruguay', 'Zambia', 'Zimbabwe'
]


def main(page: ft.Page):
    page.title = "AgriTech"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = "light"

    # Fonction de navigation entre les pages
    def go_to_recommendation(e):
        page.clean()
        recommendation_page()

    def go_to_prediction(e):
        page.clean()
        prediction_page()

    def go_to_home(e):
        page.clean()
        home_page()

    # Page d'accueil avec les informations du projet
    def home_page():
        header = ft.Text("👋Bienvenue sur AgriTech👩‍🌾", size=50,
                         weight="bold", color="#4CAF50")
        details = ft.Text(
            "AgriTech est votre Application de \n 🌽Recomandation de semences&prédiction agricole.🌾 ", size=16)

        # Boutons pour accéder aux autres pages
        go_to_recommendation_button = ft.ElevatedButton(
            "Recommandation de semences",
            bgcolor="#4CAF50",
            color="white",
            on_click=go_to_recommendation
        )

        go_to_prediction_button = ft.ElevatedButton(
            "Prédiction agricole",
            bgcolor="#4CAF50",
            color="white",
            on_click=go_to_prediction
        )

        page.add(
            ft.Column(
                [
                    header,
                    details,
                    go_to_recommendation_button,
                    go_to_prediction_button,
                ],
                alignment="center",
                horizontal_alignment="center",
                spacing=20,
            )
        )

    # Page de recommandation de semences
    def recommendation_page():
        global predicted_culture

        # Champs d'entrée pour la prédiction de la semence
        nitrogen_input = ft.TextField(
            label="Nitrogen (N)", keyboard_type="number", width=300)
        phosphorus_input = ft.TextField(
            label="Phosphorus (P)", keyboard_type="number", width=300)
        potassium_input = ft.TextField(
            label="Potassium (K)", keyboard_type="number", width=300)
        temperature_input = ft.TextField(
            label="Temperature (°C)", keyboard_type="number", width=300)
        humidity_input = ft.TextField(
            label="Humidity (%)", keyboard_type="number", width=300)
        ph_input = ft.TextField(label="PH", keyboard_type="number", width=300)
        rainfall_input = ft.TextField(
            label="Rainfall (mm)", keyboard_type="number", width=300)

        # Fonction pour soumettre les données de recommandation
        def submit_recommendation(e):
            global predicted_culture
            recommendation_data = {
                "N": nitrogen_input.value,
                "P": phosphorus_input.value,
                "K": potassium_input.value,
                "temperature": temperature_input.value,
                "humidity": humidity_input.value,
                "ph": ph_input.value,
                "rainfall": rainfall_input.value
            }
            # Envoi à l'API de recommandation de culture
            try:
                response = requests.post(
                    "http://127.0.0.1:5002/recommand", json=recommendation_data)
                predicted_culture = response.json().get(
                    "recommandation", "Culture non trouvée")
                recommendation_result.value = f"Culture recommandée : {
                    predicted_culture}"
                recommendation_result.update()
            except Exception as ex:
                recommendation_result.value = f"Erreur : {str(ex)}"
                recommendation_result.update()

        # Résultat de la recommandation
        recommendation_result = ft.Text(
            size=16, weight="bold", color="#FF5722")

        # Bouton pour soumettre la recommandation
        submit_button = ft.ElevatedButton(
            "Generer une semence",
            bgcolor="#4CAF50",
            color="white",
            on_click=submit_recommendation
        )

        # Bouton pour aller à la page de prédiction
        go_to_prediction_button = ft.ElevatedButton(
            "Predire la production agricole",
            bgcolor="#4CAF50",
            color="white",
            on_click=go_to_prediction
        )

        # Bouton pour revenir à la page d'accueil
        back_to_home_button = ft.ElevatedButton(
            "Retour à l'accueil",
            bgcolor="#4CAF50",
            color="white",
            on_click=go_to_home
        )

        page.add(
            ft.Column(
                [
                    nitrogen_input,
                    phosphorus_input,
                    potassium_input,
                    temperature_input,
                    humidity_input,
                    ph_input,
                    rainfall_input,
                    submit_button,
                    recommendation_result,
                    go_to_prediction_button,
                    back_to_home_button
                ],
                alignment="center",
                horizontal_alignment="center",
                spacing=10
            )
        )

    # Page de prédiction agricole
    def prediction_page():
        global predicted_culture

        # Champs d'entrée pour la prédiction agricole
        area_input = ft.Dropdown(
            label="Région (Pays)",
            options=[ft.dropdown.Option(pays) for pays in list_pays],
            border_color="#4CAF50",
            width=300
        )
        avg_temp_input = ft.TextField(
            label="Température moyenne (°C)", keyboard_type="number", width=300)
        pesticides_input = ft.TextField(
            label="Tonnes de pesticides utilisées", keyboard_type="number", width=300)
        rainfall_input = ft.TextField(
            label="Précipitations moyennes (mm/an)", keyboard_type="number", width=300)

        # Utiliser la culture prédite ou permettre la saisie si on vient du Home
        # item_input = ft.TextField(
        #     label="Culture (Item)",
        #     value=predicted_culture if predicted_culture else "",
        #     read_only=True if predicted_culture else True, width=300
        # )
        item_input = ft.Dropdown(
            label="Culture (Item)",
            options=[ft.dropdown.Option(culture) for culture in list_culture],
            border_color="#4CAF50",
            width=300
        )

        # Fonction pour soumettre les données de prédiction agricole
        def submit_prediction(e):
            prediction_data = [{
                "Area": area_input.value,
                "avg_temp": float(avg_temp_input.value),
                "pesticides_tonnes": float(pesticides_input.value),
                "average_rain_fall_mm_per_year": float(rainfall_input.value),
                "Item": item_input.value
            }]
            # Envoi à l'API de prédiction agricole
            try:
                response = requests.post(
                    "http://127.0.0.1:5001/predict", json=prediction_data)
                prediction_result.value = f"Si vous cultivez {item_input.value} au {area_input.value} dans ces conditions\n, vous allez récolter(en Hectogramme/Hectare) : {
                    response.json().get('prediction', 'Erreur')}"
                prediction_result.update()
            except Exception as ex:
                prediction_result.value = f"Erreur : {str(ex)}"
                prediction_result.update()

        # Résultat de la prédiction
        prediction_result = ft.Text(size=16, weight="bold", color="#FF5722")

        # Bouton pour soumettre la prédiction
        submit_button = ft.ElevatedButton(
            "Predire la production",
            bgcolor="#4CAF50",
            color="white",
            on_click=submit_prediction
        )

        # Bouton pour revenir à la page d'accueil
        back_to_home_button = ft.ElevatedButton(
            "Retour à l'accueil",
            bgcolor="#4CAF50",
            color="white",
            on_click=go_to_home
        )

        page.add(
            ft.Column(
                [
                    area_input,
                    avg_temp_input,
                    pesticides_input,
                    rainfall_input,
                    item_input,
                    submit_button,
                    prediction_result,
                    back_to_home_button
                ],
                alignment="center",
                horizontal_alignment="center",
                spacing=10
            )
        )

    # Afficher la page d'accueil initialement
    home_page()


ft.app(target=main)
