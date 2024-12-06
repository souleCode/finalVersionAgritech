import pandas as pd
import chromadb
import uuid


class Maladie:
    def __init__(self, file_path="../../Data/Tomato_Diseases_and_Treatments.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(
            name="maladie")
        # print("La collection:", self.collection.get())

    def load_maladie(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Maladie"],
                                    metadatas={"source": row["Traitement"]},
                                    ids=[str(uuid.uuid4())])

    def query_source(self, traitement):
        return self.collection.query(query_texts=traitement, n_results=2).get('metadatas', [])


if __name__ == "__main__":
    # Maladie()
    print("Bien reçu")
