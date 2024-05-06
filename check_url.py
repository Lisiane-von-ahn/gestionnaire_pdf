import streamlit as st
import base64
from util import *

st.title("Gestionnaire de fichiers")

# Liste pour stocker les fichiers PDF chargés
pdf_files = []

# Fonction pour afficher les fichiers PDF
def display_pdf(pdf_data):
    base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

checkbox_result = st.checkbox('Afficher Preview ?')

# Section pour charger les fichiers
st.subheader("Télécharger des fichiers PDF")
fichiers_uploades = st.file_uploader("Choisissez des fichiers PDF", type="pdf", accept_multiple_files=True)

# Si des fichiers ont été téléchargés
if fichiers_uploades:
    with st.spinner('En train de charger, merci de bien vouloir patienter !'):
        for fichier_uploadé in fichiers_uploades:
            # Lit les données du fichier PDF
            données_pdf = fichier_uploadé.read()
            # Ajoute les données du PDF à la liste des fichiers PDF
            pdf_files.append(données_pdf)

            # Save the uploaded file with the safe filename
            with open(fichier_uploadé.name, 'wb') as f:
                f.write(données_pdf)

            # Obtenir les liens
            liens = extraire_liens_dans_pdf(fichier_uploadé.name)
            
            afficher_accordion(fichier_uploadé.name,liens)        
            
            if checkbox_result == True:
                display_pdf(données_pdf)