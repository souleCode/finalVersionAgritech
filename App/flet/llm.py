from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    temperature=0,
    groq_api_key=GROQ_API_KEY,
    model_name='llama-3.1-70b-versatile'
)
# response = llm.invoke(
#     "Qui est la premiere personne a faire un pas sur la lune?")
# print(response.content)


# Construction du template avec échappement correct
prompt_template = PromptTemplate.from_template(
    """
                ### MALADIE DES PLANTES:
                {maladie}
                ### INSTRUCTION:
                Tu es un Assistant AgriTech. Tu réponds juste à ce qu'on te demande.
                Une liste de maladies des plantes est une détection par mon Modèle AgriTech.
                Ton travail est de traduire les maladies de la plante en français. Ensuite, tu proposes 5 traitements pour chaque maladie.
                Retourne seulement un fichier JSON de ces traitements comme suit :
                {{
                    "maladie1 en français": {{
                        "1": "traitement1",
                        "2": "traitement2",
                        "3": "traitement3",
                        "4": "traitement4",
                        "5": "traitement5"
                    }},
                    "maladie2 en français": {{
                        "1": "traitement1",
                        "2": "traitement2",
                        "3": "traitement3",
                        "4": "traitement4",
                        "5": "traitement5"
                    }}                        
                }}
                Tu me donnes la réponse sans préambule, sans explication, ni titre.
                
                FORMAT JSON VALID### :
                """
)

# Exemple d'utilisation
maladies = "Healthy Leaf,Bacterial Spot,Early Blight"

# Lancer le prompt avec le modèle LLM
chaine_extraite = prompt_template | llm
res = chaine_extraite.invoke(input={'maladie': maladies})
print(res.content)
