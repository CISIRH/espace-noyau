import requests
import os

def modif_menu(titre, cible):
    if os.path.exists("./src/_sidebar.md"):
        f = open("./src/_sidebar.md","a")
    else :
        f = open("./src/_sidebar.md","w")
    mark = """
- ["""+titre+"""]("""+cible+""")
    """
    f.write(mark)
    f.close()

def ecrire_contenu(path_fichier, contenu):
    f = open(path_fichier, "a")
    f.write(contenu)
    f.close()

def get_content(url):
    token = os.environ["GH_TOKEN"]
    username = 'MatthieuDEVALLE'
    #token = ''
    print(token)
    content = requests.get(url, auth=(username,token))
    return content.json()

def ecrire_gros_titre(fichier, gros_titre):
    res = "# "+gros_titre+"\n"
    ecrire_contenu(fichier,res)

def ecrire_moyen_titre(fichier, gros_titre):
    res = "## "+gros_titre+"\n"
    ecrire_contenu(fichier,res)

def ecrire_lien(fichier, titre, lien):
    res = "- ["+titre+"]("+lien+")"+"\n"
    ecrire_contenu(fichier, res)

def ecrire_titre(fichier, titre):
    res = "### "+titre+"\n"
    ecrire_contenu(fichier,res)

def explore_sub(contenu_inital,contenu_prec):
    content = get_content(contenu_prec["url"])
    for contenu2 in content:
        if str(contenu2["type"]) == "file":
            ecrire_lien(str("./docs/"+nom_doc(contenu_inital["name"]) + ".md"), contenu2["name"], contenu2["html_url"])
        else:
            ecrire_titre(str("./docs/"+nom_doc(contenu_inital["name"]) + ".md"), contenu2["name"])
            explore_sub(contenu_inital,contenu2)

def nom_doc(titre):
    titre = titre.replace(" ","_")
    titre = titre.replace(")","")
    titre = titre.replace("(","")
    titre = titre.replace("'","")
    titre = titre.upper()
    return titre

def explore_cree(url):
    #print("URL:" + url)
    url = str(url)
    content = get_content(url)
    #print(content)


    for contenu in content :
        if str(contenu["type"]) == "dir":
            open(str("./docs/"+nom_doc(contenu["name"])+".md"), "w")
            modif_menu(contenu["name"], str("./docs/"+nom_doc(contenu["name"])+".md"))
            ecrire_gros_titre(str("./docs/"+nom_doc(contenu["name"]) + ".md"), contenu["name"])
            content2 = get_content(contenu["url"])
            for contenu2 in content2 :
                if str(contenu2["type"]) == "file":
                    ecrire_lien(str("./docs/"+nom_doc(contenu["name"])+".md"),contenu2["name"],contenu2["html_url"])
                    #ecrire_contenu(str(contenu["name"]+".md"),contenu["html_url"])
                else :
                    ecrire_moyen_titre(str("./docs/"+nom_doc(contenu["name"])+".md"),contenu2["name"])
                    explore_sub(contenu,contenu2)

explore_cree("https://api.github.com/repos/CISIRH/espace-noyau/contents/Noyau RH FPE")