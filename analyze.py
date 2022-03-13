import os
import glob
import ntpath

PONC = ["!", ",", ".", "-", ":", ";", "?", "«", "»", "(", ")", "[", "]", "{", "}", "…", "/", "'", "*", "<", ">", "&",
        "~", "–", "„", "“", "‚", "‘", "“", "”", "‘", "’", "\n"]

dict = {}
noPonc = True
author = "zola"
directory = "TextesPourEtudiants"
textsPath = directory + "/" + author + "/"  # Chemin des textes de l'auteur

for file in os.listdir(textsPath):  # Pour chaque texte dans le répertoire
    if file.endswith(".txt"):  # Vérification de l'extension du fichier
        f = open(textsPath + file, "r")  # Ouverture du fichier
        textContent = f.read().lower().split()  # Lecture du fichier et séparation de chaque mot (séparé par : espace)

        if noPonc == True:  # Si le mode sans ponctuation est activé (noPonc) on repasse sur tous les mots et on
            # vérifie s'il a un caractère parmis le tableau PONC
            formatStr = ""  # Chaîne temporaire qui sevira à remettre tout les mots sans ponctuation pour les
            # re-séparer (permet d'éviter d'avoir des indexs possédants des espaces)
            index = 0
            while index != len(textContent):  # Pour tout les mots dans le texte
                for character in textContent[index]:  # Pour chaque caractère dans le texte
                    for ponctuation in PONC:  # Vérifier si le caractère en est un dans le tableau PONC
                        if character == ponctuation:  # Si caractère est caractère ponctué
                            textContent[index] = textContent[index].replace(character, ' ')  # Remplace par un espace
                formatStr += textContent[index] + " "  # Ajout du mot formatté dans la chaîne temporaire
                index = index + 1
            textContent = formatStr.split()  # Re-séparation des mots dans la liste

        index = 0
        # Boucle qui permet d'enlever tous les mots de deux caractères et moins
        while index != len(textContent):  # Pour chaque mot dans le tableau
            if len(textContent[index]) <= 2:  # Si taille du mot < 2
                textContent.pop(index)  # Retrait du mot
            index = index + 1

        index = 0
        # Boucle permettant de placer les éléments dans le dictionnaire, permet aussi de compter chaque mot
        while index != len(textContent):  # Pour chaque mot dans le tableau
            if textContent[index] in dict:  # Si la clé existe déjà dans le dictionnaire
                dict.update({textContent[index]: dict.get(textContent[index]) + 1})  # Mise à jour du nombre de
                # répétition du mot pour cette clé
            else:
                dict.update({textContent[index]: 1})  # Mettre un nouveau mot au compte de 1 si pas existant
            index = index + 1
print(dict)
