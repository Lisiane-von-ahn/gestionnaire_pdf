import requests
import streamlit as st
import PyPDF2

def creer_tableau_resume(st,listeBon, listeMauvais):
    st.markdown("<b><font color=red>" + str(len(listeMauvais)) + " Lien(s) ne marche(nt) pas</font> </b>", unsafe_allow_html=True)
    
    for lien in listeMauvais:
        st.write(lien)
    
    st.markdown("<b><font color=green>" + str(len(listeBon)) + " Lien(s) marche(nt) bien</font> </b>", unsafe_allow_html=True)
    
    for lien in listeBon:
        st.write(lien)

def afficher_accordion(name, liens):
    st.write("Nom du fichier:", name)
    
    liensBons = []
    liensMauvais = []

    for lien in liens:
        if mon_lien_est_bon(lien):
            liensBons.append(lien)
        else:
            liensMauvais.append(lien)

    with st.expander("Résumé des liens"):
        creer_tableau_resume(st, liensBons, liensMauvais)
        
def mon_lien_est_bon (lien):    
    try:
        response = requests.get(lien)
        response.raise_for_status()
    except requests.HTTPError as http_err:
        return False
    except Exception as err:
        return False
    else:
        return True    

def extraire_liens_dans_pdf(fichier_pdf):

    # c'est la clé des annotations trouvés dans le PDF, les annotations sont types d'objets comme hyperlinks    
    key = '/Annots'
    # c'est pour # specifier que je veux un hyperlink format URI/URL
    uri = '/URI'
    # ici je ne prends que les anchors (hyperlinks)
    ank = '/A'
    
    #ici c'est un array qui contient les liens qu'on va retourner
    liens = []
    
    # Ouvrir le fichier PDF avec rb qui signifie que je ne veux que lire (read) et b c'est pour normaliser le charset
    with open(fichier_pdf, 'rb') as fichier:
        # J'utilise la biblioteque pypdf2 pour ouvrir le pdf et pouvoir travailler avec lui
        lecteur = PyPDF2.PdfFileReader(fichier)
        # pour chaque page trouvée dans le document, je prends le texte et je vais chercher les liens
        for num_page in range(lecteur.numPages):
            page = lecteur.getPage(num_page)
            pageObject = page.getObject()
            # si le type d'objet est annotation (defini dans la variable précedente) on va prendre les hyperlinks et l'uri
            if key in pageObject.keys():
                ann = pageObject[key]
                for a in ann:
                    u = a.getObject()
                    if uri in u[ank].keys():
                        mylink = u[ank][uri]
                        liens.append(mylink)

    return liens