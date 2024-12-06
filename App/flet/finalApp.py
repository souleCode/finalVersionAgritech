from dotenv import load_dotenv
import os
import json
from flet import *
from custom_checkbox import CustomCheckBox
import requests


def main(page: Page):
    BG = "#041955"
    FWG = "#97b4ff"
    FG = "#3450a1"
    PINK = "#eb06ff"

    # Les donnees meteorologiques
    # import librairies

    WEATHER_API_KEY = os.getenv('API_KEY')
    BASE_URL = os.getenv('BASE_URL')

    # @...Todo
    # API information

    VILLE = "MEKNES"

    # Fcontion pour fetcher les donnees depuis l'api

    def get_data_from_api(ville):
        # Construire url vers les donnees
        url = f"{BASE_URL}q={ville}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error : {response.status_code}")
            return None

    def analyze_data(data):
        if data:
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            vent = data["wind"]["speed"]
            max_tem = data['main']['temp_max']
            return {

                'temperature': temperature,
                'humidity': humidity,
                'vent': vent,
                'max_temp': max_tem,
            }
        else:
            return None

    # Submit data for recommandation

    def submit_re_data(e):
        recommendation_data = {
            "N": nitrogen_textfield.value,
            "P": phosphorus_textfield.value,
            "K": potassium_textfield.value,
            "temperature": temperature_textfield.value,
            "humidity": humidity_textfield.value,
            "ph": ph_textfield.value,
            "rainfall": rainfall_re_textfield.value
        }
        # Envoi à l'API de recommandation de culture
        try:
            response = requests.post(
                "http://127.0.0.1:5002/recommand", json=recommendation_data)
            predicted_culture = response.json().get(
                "recommandation", "Culture non trouvée")
            result_re_textfield.value = f"Recommandation : {
                predicted_culture}"
            result_re_textfield.update()
        except Exception as ex:
            result_re_textfield.value = f"Erreur : {str(ex)}"
            result_re_textfield.update()

    # Submit data for prediction
    def submit_data(e):
        data = [{
            "Area": area_input_dropdown.value,
            "avg_temp": float(avg_temp_textfield.value),
            "pesticides_tonnes": float(pesticides_textfield.value),
            "average_rain_fall_mm_per_year": float(rainfall_textfield.value),
            "Item": item_dropdown.value
        }]

        try:
            # Envoi des données à l'API Flask en local
            response = requests.post(
                "http://127.0.0.1:5000/predict", json=data)
            response_data = response.json()

            # Récupération de la prédiction en Hg/Ha
            prediction_hg_per_ha = response_data.get('prediction', 'Erreur')

            # Vérifie que la prédiction est bien un nombre avant de faire la conversion
            if isinstance(prediction_hg_per_ha, (int, float)):
                # Conversion de Hg/Ha en T/Ha et formatage avec deux chiffres après la virgule
                prediction_t_per_ha = prediction_hg_per_ha / 10000
                result_textfield.value = f"Prédiction (T/Ha) : {
                    round(prediction_t_per_ha, 2)}"
            else:
                result_textfield.value = f"Erreur dans la prédiction : {
                    round(prediction_hg_per_ha, 2)}"
        except Exception as ex:
            result_textfield.value = f"Erreur de connexion : {str(ex)}"

        result_textfield.update()

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
    list_culture = [
        'Maize', 'Potatoes', 'Sorghum', 'Soybeans', 'Wheat',
        'Cassava', 'Sweet potatoes', 'Plantains and others', 'Yams'
    ]

    # Les inputs sans Containers pour la prediction du rendement
    area_input_dropdown = Dropdown(
        label="Région (Pays)",
        options=[dropdown.Option(pays) for pays in list_pays],
        width=250,
        border_color=FWG,
    )
    result_textfield = Text(size=16, weight="Bold", color="#FF5722")
    avg_temp_textfield = TextField(
        label="Température moyenne (°C)",
        border_color=FWG,
        width=300,
        keyboard_type="number",
        color="white"
    )
    pesticides_textfield = TextField(
        label="Pesticides utilisées(Kg)",
        border_color=FWG,
        width=300,
        keyboard_type="number",
        color="white")
    item_dropdown = Dropdown(
        label="Cutlure",
        options=[dropdown.Option(item) for item in list_culture],
        width=250,
        border_color=FWG,

    )
    rainfall_textfield = TextField(label="Précipitations moyennes (mm/an)",
                                   border_color=FWG,
                                   width=300,
                                   keyboard_type="number",
                                   color="white"
                                   )
    area_input = Container(
        width=250,
        height=50,
        bgcolor=FG,
        border_radius=15,
        content=area_input_dropdown
    )

    avg_temp_input = Container(
        width=250,
        height=50,
        bgcolor=FG,
        border_radius=15,
        content=avg_temp_textfield
    )
    pesticides_input = Container(
        width=250,
        height=50,
        bgcolor=FG,
        border_radius=15,
        content=pesticides_textfield
    )

    rainfall_input = Container(
        width=250,
        height=50,
        bgcolor=FG,
        border_radius=15,
        content=rainfall_textfield
    )
    item = Container(
        width=250,
        height=50,
        bgcolor=FG,
        border_radius=15,
        content=item_dropdown
    )

    submit_button = Container(
        width=150,
        height=30,
        border_radius=35,
        content=ElevatedButton(
            "Prédire",
            bgcolor="#4CAF50",
            color="white",
            on_click=submit_data
        ),
        alignment=alignment.center
    )
    result_container = Container(
        border_radius=10,
        bgcolor=BG,
        height=80,
        width=200,
        padding=15,
        content=Column(
            controls=[
                Container(
                    content=result_textfield,
                ),
            ],
            alignment=alignment.center,
        )
    )


#  Les inputs sans container pour la recommandation
    nitrogen_textfield = TextField(
        label="Nitrogene (N)", keyboard_type="number", width=300)
    phosphorus_textfield = TextField(
        label="Phosphore (P)", keyboard_type="number", width=300)
    potassium_textfield = TextField(
        label="Potassium (K)", keyboard_type="number", width=300)
    temperature_textfield = TextField(
        label="Température (°C)", keyboard_type="number", width=300)
    humidity_textfield = TextField(
        label="Humidité (%)", keyboard_type="number", width=300)
    ph_textfield = TextField(label="PH", keyboard_type="number", width=300)
    rainfall_re_textfield = TextField(
        label="La pluviométrie (mm)", keyboard_type="number", width=300)
    result_re_textfield = Text(
        size=16, weight="bold", color="#FF5722")
    # Les inpts en conainters
    nitrogen_input = Container(
        width=250,
        height=50,
        bgcolor=FG,
        border_radius=15,
        content=nitrogen_textfield
    )
    phosphorus_input = Container(
        width=250,
        height=50,
        bgcolor=FG,
        border_radius=15,
        content=phosphorus_textfield
    )
    potassium_input = Container(
        width=250,
        height=50,
        bgcolor=FG,
        border_radius=15,
        content=potassium_textfield
    )
    temperature_input = Container(
        width=250,
        height=50,
        bgcolor=FG,
        border_radius=15,
        content=temperature_textfield
    )
    humidity_input = Container(
        width=250,
        height=50,
        bgcolor=FG,
        border_radius=15,
        content=humidity_textfield
    )
    ph_input = Container(
        width=250,
        height=50,
        bgcolor=FG,
        border_radius=15,
        content=ph_textfield
    )
    rainfall_re_input = Container(
        width=250,
        height=50,
        bgcolor=FG,
        border_radius=15,
        content=rainfall_re_textfield
    )
    result_re_container = Container(
        border_radius=10,
        bgcolor=BG,
        height=80,
        width=200,
        padding=15,
        content=Column(
            controls=[
                Container(
                    content=result_re_textfield,
                ),
            ],
            alignment=alignment.center,
        )
    )
    submit_re_button = Container(
        width=150,
        height=30,
        border_radius=20,
        content=ElevatedButton(
            "Recommander",
            bgcolor="#4CAF50",
            color="white",
            on_click=submit_re_data
        ),
        alignment=alignment.center
    )
    # functions

    def menuBtn(e):
        page_2.controls[0].width = 80
        page_2.controls[0].scale = transform.Scale(
            0.8, alignment=alignment.center_right)
        page_2.controls[0].border_radius = border_radius.only(
            top_left=35,
            top_right=0,
            bottom_left=35,
            bottom_right=0,
        )
        page_2.update()

    def restore(e):
        page_2.controls[0].width = 300
        page_2.controls[0].scale = transform.Scale(
            1, alignment=alignment.center_right)
        page_2.update()

    Circle = Stack(
        controls=[
            Container(
                width=80,
                height=80,
                border_radius=50,
                bgcolor='white12'
            ),
            Container(
                gradient=SweepGradient(
                    center=alignment.center,
                    start_angle=0.0,
                    end_angle=3,
                    stops=[0.5, 0.5],
                    colors=['#00000000', PINK],
                ),
                width=80,
                height=80,
                border_radius=50,
                content=Row(alignment='center',
                            controls=[
                                Container(padding=padding.all(5),
                                          bgcolor=BG,
                                          width=90, height=90,
                                          border_radius=50,
                                          content=Container(bgcolor=FG,
                                                            height=50, width=50,
                                                            border_radius=40,
                                                            content=CircleAvatar(opacity=0.8,
                                                                                 foreground_image_url=""
                                                                                 )
                                                            )
                                          )
                            ],
                            ),
            ),

        ]
    )
    # container of predictions
    prediction = Container(
        # container of predictions values
        width=300,
        height=650,
        bgcolor=FG,
        border_radius=35,
        padding=padding.only(left=40, top=40, right=200),

        content=Column(
            controls=[
                Row(
                    controls=[
                        Container(
                            height=40,
                            width=40,
                            content=Text('X', color='white', size=30),
                            on_click=lambda _: page.go('/')
                        ),
                        result_container,
                        Container(height=20),

                    ]
                ),
                Container(height=20),
                Row(
                    controls=[
                        Container(
                            padding=padding.only(top=1, left=3),
                            width=200,
                            content=Text("Faire une Prédiction agricole",
                                         color="white", size=15)
                        )
                    ]
                ),
                Container(height=20),
                # Ajoutez ensuite dans votre Row
                Row(
                    controls=[
                        area_input
                    ]
                ),
                Row(
                    controls=[
                        avg_temp_input
                    ]
                ),
                Row(
                    controls=[
                        pesticides_input
                    ]
                ),
                Row(
                    controls=[
                        rainfall_input
                    ]
                ),
                Row(
                    controls=[
                        item
                    ]
                ),
                Row(
                    controls=[
                        submit_button
                    ]
                )
            ]
        )
    )

    recommandation = Container(
        # container of predictions values
        width=300,
        height=650,
        bgcolor=FG,
        border_radius=35,
        padding=padding.only(left=40, top=40, right=200),

        content=Column(
            controls=[
                Row(alignment="spaceBetween",
                    controls=[
                        Container(
                            height=40,
                            width=40,
                            content=Text('X', color='white', size=20),
                            on_click=lambda _: page.go('/'),
                            # padding=padding.only(left=5, top=40)
                        ),
                        result_re_container,

                    ]
                    ),
                # Container(height=20),
                Row(
                    controls=[
                        Container(
                            padding=padding.only(top=1, left=3),
                            width=200,
                            content=Text("Recommandation de culture",
                                         color="white", size=15)
                        )
                    ]
                ),
                # Ajoutez ensuite dans votre Row
                Row(
                    controls=[
                        nitrogen_input
                    ]
                ),
                Row(
                    controls=[
                        phosphorus_input
                    ]
                ),
                Row(
                    controls=[
                        potassium_input
                    ]
                ),
                Row(
                    controls=[
                        temperature_input
                    ]
                ),
                Row(
                    controls=[
                        humidity_input
                    ]
                ),
                Row(
                    controls=[
                        ph_input
                    ]
                ),
                Row(
                    controls=[
                        rainfall_re_input
                    ]
                ),
                Row(
                    controls=[
                        submit_re_button
                    ]
                )
            ]
        )
    )

    maladie = Container(
        content=Container(height=40,
                          width=40,
                          content=Text('X', color='white'),
                          on_click=lambda _: page.go('/')
                          ),
        width=300,
        height=650,
        bgcolor=FG,
        border_radius=35,
        padding=padding.only(left=40, top=40, right=200),
    )
    # added values

    added_values = Column(
        height=400,
        scroll='auto',
        controls=[
            Container(

            )
        ]
    )
    for i in range(4):
        added_values.controls.append(
            Container(height=50,
                      width=300,
                      bgcolor=BG,
                      border_radius=20,
                      content=Text(
                          'Faire les prédictions de vos cultures', color='white', text_align='center',),
                      alignment=alignment.center
                      ),

        )
    # Donnees recuperer depuis API wheather
    donnees_clim_card = Row(
        scroll='auto',
    )
    climats = ['Temperature', 'Pluviometrie', 'La vitesse du vent']
    for i, clim in enumerate(climats):
        donnees_clim_card.controls.append(
            Container(
                border_radius=20,
                bgcolor=BG,
                height=100,
                width=150,
                padding=15,
                content=Column(
                    controls=[
                        Text("400", color='white'),
                        Text(clim, color='white'),
                        Container(
                            border_radius=20,
                            bgcolor='white12',
                            height=5,
                            width=150,
                            padding=padding.only(right=i*30),
                            content=Container(
                                bgcolor=PINK,
                            )
                        )
                    ]
                )
            )
        )
    # Pages principales de mon
    first_page_contents = Container(
        content=Column(
            controls=[
                Row(alignment='spaceBetween',
                    controls=[
                        Container(on_click=lambda e: menuBtn(e),
                                  content=Icon(
                            icons.MENU,
                            color="white")),
                        Row(
                            controls=[
                                Icon(icons.SEARCH, color='white'),
                                Icon(icons.NOTIFICATION_ADD_OUTLINED,
                                     color='white')
                            ],
                        ),
                    ],
                    ),
                Container(height=20),
                Text(
                    value="🌽AgriTech, IA🌾",
                    color='white',
                ),
                Container(height=10),
                Text(
                    value="CLIMAT",
                    color='white',
                ),
                Container(
                    padding=padding.only(
                        top=10,
                        bottom=20,),
                    content=donnees_clim_card
                ),
                Container(height=20),
                Text(
                    value="Utilisation de AgriTech, IA",
                    color='white',
                ),
                Stack(
                    controls=[
                        added_values,
                        FloatingActionButton(top=2, right=10,
                                             icon=icons.ADS_CLICK,
                                             on_click=lambda _: page.go(
                                                 '/prediction')
                                             ),
                    ],
                ),
                Container(height=20),


            ]
        )
    )
    page_1 = Container(
        width=300,
        height=650,
        bgcolor=FG,
        border_radius=35,
        padding=padding.only(left=40, top=40, right=200),
        content=Column(
            controls=[
                Row(alignment='end',
                    controls=[
                        Container(
                            on_click=lambda e: restore(e),
                            border_radius=25,
                            padding=padding.only(top=1, left=3),
                            height=50,
                            width=50,
                            border=border.all(color='white', width=1),
                            content=Text("↩", color="white", size=30)
                        )
                    ]
                    ),
                Container(height=20),
                # CustomCircle

                # Circle,
                CircleAvatar(
                    foreground_image_url=""
                ),
                Text("AgriTech.", size=13, weight='bold', color='white'),
                Container(height=20),
                Row(alignment='end',
                    controls=[
                        Container(
                            on_click=lambda _: page.go('/recommandation'),
                            border_radius=25,
                            padding=padding.only(top=1, left=3),
                            width=150,
                            height=50,
                            border=border.all(color=BG, width=2),
                            content=Text("Trouve une semence",
                                         color="white", size=15),
                            alignment=alignment.center,
                        )
                    ]
                    ),
                Container(height=20),
                Row(
                    controls=[
                        Container(
                            on_click=lambda _: page.go('/prediction'),
                            border_radius=25,
                            padding=padding.only(top=1, left=3),
                            border=border.all(color=BG, width=2),
                            width=150,
                            height=50,
                            content=Text("Prediction Agricole",
                                         color="white", size=15),
                            alignment=alignment.center,
                        )
                    ]
                ),
                Container(height=20),
                Row(
                    controls=[
                        Container(
                            on_click=lambda _: page.go('/maladie'),
                            border_radius=25,
                            padding=padding.only(top=1, left=3),
                            width=150,
                            height=50,
                            border=border.all(color=BG, width=2),
                            content=Text("Santé Agricole",
                                         color="white", size=15),
                            alignment=alignment.center,
                        ),

                    ]
                ),
            ]
        )
    )
    page_2 = Row(alignment='end',
                 controls=[
                     Container(
                         width=300,
                         height=650,
                         bgcolor=FG,
                         border_radius=35,
                         animate=animation.Animation(
                           600, AnimationCurve.DECELERATE),
                         animate_scale=animation.Animation(
                             400, AnimationCurve.DECELERATE),
                         padding=padding.only(
                             top=50,
                             left=20,
                             right=20,
                             bottom=5

                         ),
                         content=Column(
                             controls=[
                                 first_page_contents,

                             ]
                         )
                     )
                 ]
                 )
    container = Container(
        width=300,
        height=650,
        bgcolor=FG,
        border_radius=35,
        content=Stack(
            controls=[
                page_1,
                page_2
            ]
        )
    )

    # Routing Parameters

    pages = {
        '/': View(
            "/",
            [
                container
            ],
        ),
        '/prediction': View(
            "/prediction",
            [
                prediction,
            ]
        ),
        '/recommandation': View(
            "/recommandation",
            [
                recommandation,
            ]
        ),
        '/maladie': View(
            "/maladie",
            [
                maladie,
            ]
        ),
    }

    # Routing functions
    def route_change(route):
        page.views.clear()
        page.views.append(
            pages[page.route]
        )
    page.scroll = 'auto'
    page.add(container)

    page.on_route_change = route_change
    page.go(page.route)
    # essaie API OpenWeather
    # data = get_data_from_api(VILLE)
    # analysed_data = analyze_data(data)
    # print(analysed_data)


app(target=main)
