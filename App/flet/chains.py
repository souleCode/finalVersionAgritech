import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0,
                            groq_api_key=GROQ_API_KEY,
                            model_name="llama-3.1-70b-versatile"
                            )

    def extract_maladies(self, maladies):
        prompt_template = PromptTemplate.from_template(
            """
                ### MALADIE DES PLANTES:
                {maladie}
                ### INSTRUCTION:
                Tu es un Assistant AgriTech. Tu réponds juste à ce qu'on te demande.
                Une liste de maladies des plantes est une détection par mon Modèle AgriTech.
                Ton travail est de proposer 5 traitements pour chaque maladie. Tu garde les maladies en anglais comme on t'a donné.
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
        # Lancer le prompt avec le modèle LLM
        chaine_extraite = prompt_template | self.llm
        res = chaine_extraite.invoke(input={'maladie': maladies})
        # print(res.content)
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException(
                "Le context est trop grand. Impossible de trouver le traitement")
        return res if isinstance(res, list) else [res]

    def ecrire_traitement(self, maladie, traitements):
        prompt_maladie = PromptTemplate.from_template(
            """
                ### Maladie
                {maladie}
                ### INSTRUCTION:
                Tu es l'Assistant AgriTech IA. Ecris donc une proposition de traitement des maladies de plantes que va recevoir
                Tu donnes d'abord la liste des maladies que tu as reçue en les ecrivant en gras.
                ### Ne traduit pas les maladies en francais.
                ### Tu decris un peu les maladies en francais.
                Pour les propositions de traitement,
                tu choisis les traitements disponibles sur le {traitement}.
                ### Tu reponds juste avec les traitement qui sont {traitement}.
                Tu n'invente rien.
                Pour les Traitements, essaie d'expliquer un peu les termes technique.
                Ecris les traitements en gras, mais pour les details, tu ecris en simple
                ### Fais des lignes courtes
                Rappelle tu es l'Assistant AgriTech IA.
                ### Tu repond en disaant Salut Assistant AgriTech,...La suite de ta reponse
                """
        )
        chain_maladie = prompt_maladie | self.llm
        res = chain_maladie.invoke(
            {"maladie": str(maladie), "traitement": traitements})
        return res.content


if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))
