import streamlit as st
from chains import Chain
from maladie_plantes import Maladie


def create_streamlit_app(llm, maladie):
    st.title("Santé Plante")
    # Les maladies doivent etre une detection de notre modele YOLO v5
    maladies = "Bacterial Spot,Early Blight"
    submit_button = st.button("Traiter")

    if submit_button:
        try:
            maladie.load_maladie()
            list_maladie = chain.extract_maladies(maladies)
            # print("list_maladie:", list_maladie)
            for mal in list_maladie:
                malad = list(mal.keys())  # Obtenir une liste de maladies
                # print("maladie:", mal)
                trait = maladie.query_source(malad)
                proposition = llm.ecrire_traitement(malad, trait)
                st.code(proposition, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    maladie = Maladie()
    st.set_page_config(
        layout="wide", page_title="Sante Vegetale", page_icon="")
    create_streamlit_app(chain, maladie)
