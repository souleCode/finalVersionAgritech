import flet as ft
import requests
import pandas as pd

# Listes de sélection pour les cultures et les pays
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
    # Définir la couleur de fond de la page
    page.bgcolor = ft.colors.BLACK  # Fond noir

    page.title = "AgriTech - Prédiction Agricole"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # En-tête de l'application
    header = ft.Text("AgriTech", size=50, weight="bold", color="#4CAF50")

    # Champs de saisie avec des menus déroulants
    area_input = ft.Dropdown(
        label="Région (Pays)",
        options=[ft.dropdown.Option(pays) for pays in list_pays],
        border_color="#4CAF50",
        width=300
    )
    avg_temp_input = ft.TextField(label="Température moyenne (°C)",
                                  border_color="#4CAF50", width=300, keyboard_type="number", color="white")
    pesticides_input = ft.TextField(
        label="Tonnes de pesticides utilisées", border_color="#4CAF50", width=300, keyboard_type="number", color="white")
    rainfall_input = ft.TextField(label="Précipitations moyennes (mm/an)",
                                  border_color="#4CAF50", width=300, keyboard_type="number", color="white")
    item_input = ft.Dropdown(
        label="Culture (Item)",
        options=[ft.dropdown.Option(culture) for culture in list_culture],
        border_color="#4CAF50",
        width=300
    )

    # Fonction pour soumettre les données
    def submit_data(e):
        data = [{
            "Area": area_input.value,
            "avg_temp": float(avg_temp_input.value),
            "pesticides_tonnes": float(pesticides_input.value),
            "average_rain_fall_mm_per_year": float(rainfall_input.value),
            "Item": item_input.value
        }]

        try:
            # Envoi des données à l'API Flask en local
            response = requests.post(
                "http://127.0.0.1:5000/predict", json=data)
            response_data = response.json()
            result_text.value = f"Prédiction : {
                response_data.get('prediction', 'Erreur')}"
        except Exception as ex:
            result_text.value = f"Erreur de connexion : {str(ex)}"

        result_text.update()

    # Bouton de soumission
    submit_button = ft.ElevatedButton(
        "Predire la production",
        bgcolor="#4CAF50",
        color="white",
        on_click=submit_data
    )

    # Zone de résultat
    result_text = ft.Text(size=16, weight="bold", color="#FF5722")

    # Ajout des éléments à la page
    page.add(
        ft.Column(
            [
                header,
                area_input,
                avg_temp_input,
                pesticides_input,
                rainfall_input,
                item_input,
                submit_button,
                result_text
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=10
        )
    )


# Exécution de l'application
ft.app(target=main)
