#!/usr/bin/env python3
# -*- coding: utf-8 -*-


""" Ce fichier contient la classe markov, à utiliser pour solutionner la problématique.
    C'est un gabarit pour l'application de traitement des fréquences de mots dans les oeuvres d'auteurs divers.

    Les méthodes aparaissant dans ce fichier définissent une API qui est utilisée par l'application
    de test testmarkov.py
    Les paramètres d'entrée et de sortie (Application Programming Interface, API) sont définis,
    mais le code est à écrire au complet.
    Vous pouvez ajouter toutes les méthodes et toutes les variables nécessaires au bon fonctionnement du système

    La classe markov est invoquée par la classe testmarkov (contenue dans testmarkov.py):

        - Tous les arguments requis sont présents et accessibles dans args (dans le fichier testmarkov.py)
        - Note: vous pouvez tester votre code en utilisant les commandes:
            + "python testmarkov.py"
            + "python testmarkov.py -h" (donne la liste des arguments possibles)
            + "python testmarkov.py -v" (mode "verbose", qui indique les valeurs de tous les arguments)

    Copyright 2018-2022, F. Mailhot et Université de Sherbrooke
"""

import argparse
import math
import os
import glob
import ntpath
import numpy as np
import random


def normalize(vecteur):
    norme = math.sqrt(sum([pow(value, 2) for value in vecteur.values()]))
    for key in vecteur.keys():
        vecteur[key] = vecteur[key] / norme
    return vecteur


class markov():
    """Classe à utiliser pour coder la solution à la problématique:

        - Contient certaines fonctions de base pour faciliter le travail (recherche des auteurs).
        - Les interfaces du code à développer sont présentes, mais tout le code est à écrire
        - En particulier, il faut compléter les fonctions suivantes:
            - find_author(oeuvre)
            - gen_text(auteur, taille, textname)
            - get_nth_element(auteur, n)
            - analyze()

    Copyright 2018-2022, F. Mailhot et Université de Sherbrooke
    """

    # Le code qui suit est fourni pour vous faciliter la vie.  Il n'a pas à être modifié
    # Signes de ponctuation à retirer (compléter la liste qui ne comprend que "!" et "," au départ)
    PONC = ["!", ",", ".", "-", ":", ";", "?", "«", "»",
            "(", ")", "[", "]", "{", "}", "…", "/", "'", "*", "<", ">", "&", "~", "–", "„", "“", "‚", "‘", "“", "”",
            "‘", "’", "\n" "\xa0", "—", "_", ]

    def set_ponc(self, value):
        """Détermine si les signes de ponctuation sont conservés (True) ou éliminés (False)

        Args:
            value (boolean) : Conserve la ponctuation (Vrai) ou élimine la ponctuation (Faux)

        Returns:
            void : ne fait qu'assigner la valeur du champs keep_ponc
        """
        self.keep_ponc = value

    def print_ponc(self):
        print("Signes de ponctuation à retirer: ", self.PONC)

    def set_auteurs(self):
        """Obtient la liste des auteurs, à partir du répertoire qui les contient tous

        Note: le champs self.rep_aut doit être prédéfini:
            - Par défaut, il contient le répertoire d'exécution du script
            - Peut être redéfini par la méthode set_aut_dir

        Returns:
            void : ne fait qu'obtenir la liste des répertoires d'auteurs et modifier la liste self.auteurs
        """
        files = self.rep_aut + "/*"
        full_path_auteurs = glob.glob(files)
        for auteur in full_path_auteurs:
            self.auteurs.append(ntpath.basename(auteur))
        return

    def get_aut_files(self, auteur):
        """Obtient la liste des fichiers (avec le chemin complet) des oeuvres d'un auteur

        Args:
            auteur (string): le nom de l'auteur dont on veut obtenir la liste des oeuvres

        Returns:
            oeuvres (Liste[string]): liste des oeuvres (avec le chemin complet pour y accéder)
        """
        auteur_dir = self.rep_aut + "/" + auteur + "/*"
        oeuvres = glob.glob(auteur_dir)
        return oeuvres

    def set_aut_dir(self, aut_dir):
        """Définit le nom du répertoire qui contient l'ensemble des répertoires d'auteurs

        Note: L'appel à cette méthode extrait la liste des répertoires d'auteurs et les ajoute à self.auteurs

        Args (string) : Nom du répertoire en question (peut être absolu ou bien relatif au répertoire d'exécution)

        Returns:
            void : ne fait que définir le nom du répertoire qui contient les répertoires d'auteurs
        """
        cwd = os.getcwd()
        if os.path.isabs(aut_dir):
            self.rep_aut = aut_dir
        else:
            self.rep_aut = os.path.join(cwd, aut_dir)

        self.rep_aut = os.path.normpath(self.rep_aut)
        self.set_auteurs()
        return

    def set_ngram(self, ngram):
        """Indique que l'analyse et la génération de texte se fera avec des n-grammes de taille ngram

        Args:
            ngram (int) : Indique la taille des n-grammes (1, 2, 3, ...)

        Returns:
            void : ne fait que mettre à jour le champs ngram
        """
        self.ngram = ngram

    def __init__(self):
        """Initialize l'objet de type markov lorsqu'il est créé

        Args:
            aucun: Utilise simplement les informations fournies dans l'objet Markov_config

        Returns:
            void : ne fait qu'initialiser l'objet de type markov
        """

        # Initialisation des champs nécessaires aux fonctions fournies
        self.keep_ponc = True
        self.rep_aut = os.getcwd()
        self.oeuvre = ""
        self.auteur = ""
        self.auteurs = []
        self.analyze_all_auteurs = True
        self.ngram = 1
        self.do_analyze = False
        self.do_gen_text = False
        self.do_get_nth_ngram = False
        self.nth_ngram = 1
        self.gen_basename = "Gen_text"
        self.gen_size = 1000

        return

    # Ajouter les structures de données et les fonctions nécessaires à l'analyse des textes,
    #   la production de textes aléatoires, la détection d'oeuvres inconnues,
    #   l'identification des n-ièmes mots les plus fréquents
    #
    # If faut coder les fonctions find_author(), gen_text(), get_nth_element() et analyse()
    # La fonction analyse() est appelée en premier par testmarkov.py
    # Ensuite, selon ce qui est demandé, les fonctions find_author(), gen_text() ou get_nth_element() sont appelées

    def find_author(self, oeuvre):
        """Après analyse des textes d'auteurs connus, retourner la liste d'auteurs
            et le niveau de proximité (un nombre entre 0 et 1) de l'oeuvre inconnue avec les écrits de chacun d'entre eux

        Args:
            oeuvre (string): Nom du fichier contenant l'oeuvre d'un auteur inconnu

        Returns:
            resultats (Liste[(string,float)]) : Liste de tuples (auteurs, niveau de proximité), où la proximité est un nombre entre 0 et 1)
        """
        freq_mots_oeuvre = self.get_freq_mots(oeuvre)
        freq_mots_oeuvre = normalize(freq_mots_oeuvre)
        vec_oeuvre = np.array(list(freq_mots_oeuvre.values()))

        resultats = []

        for auteur in self.auteurs:
            auteur["mots"] = normalize(auteur["mots"])

            vec_auteur = np.empty(len(vec_oeuvre))
            i = 0
            for key in freq_mots_oeuvre:
                if key in auteur["mots"]:
                    vec_auteur[i] = (auteur["mots"][key])
                else:
                    vec_auteur[i] = 0
                i += 1

            value = format(np.dot(vec_oeuvre, vec_auteur), ".4f")

            resultats.append((auteur["nom"], value))

        return resultats

    def gen_text(self, auteur, taille, textname):
        """Après analyse des textes d'auteurs connus, produire un texte selon des statistiques d'un auteur

        Args:
            auteur (string): Nom de l'auteur à utiliser
            taille (int): Taille du texte à générer
            textname (string): Nom du fichier texte à générer.

        Returns:
            void : ne retourne rien, le texte produit doit être écrit dans le fichier "textname"
        """

        mots_auteur = {}
        for a in self.auteurs:
            if a["nom"] == auteur:
                mots_auteur = a["mots"]
        if len(mots_auteur) == 0:
            return
        generated_text = random.choices(
            list(mots_auteur.keys()), list(mots_auteur.values()), k=taille)

        file = open(textname, "w")
        file.write(auteur + " :: Début: ")
        for word in generated_text:
            file.write(word + " ")
        file.write(":: Fin")
        file.close()
        return

    def get_nth_element(self, auteur, n):
        """Après analyse des textes d'auteurs connus, retourner le n-ième plus fréquent n-gramme de l'auteur indiqué

        Args:
            auteur (string): Nom de l'auteur à utiliser
            n (int): Indice du n-gramme à retourner

        Returns:
            ngram (List[Liste[string]]) : Liste de liste de mots composant le n-gramme recherché (il est possible qu'il y ait plus d'un n-gramme au même rang)
        """

        mots_auteur = {}
        for a in self.auteurs:
            if a["nom"] == auteur:
                mots_auteur = a["mots"]
        if mots_auteur is None:
            return

        values = sorted(set(mots_auteur.values()))

        index = len(values) - n
        if index < 0:
            index = 0

        value = values[index]

        ngram = []
        for key in mots_auteur.keys():
            if mots_auteur[key] == value:
                ngram.append(key)

        return ngram
        # ngram = [['un', 'roman']]  # Exemple du format de sortie d'un bigramme

    def analyze(self):
        """Fait l'analyse des textes fournis, en traitant chaque oeuvre de chaque auteur

        Args:
            void: toute l'information est contenue dans l'objet markov

        Returns:
            void : ne retourne rien, toute l'information extraite est conservée dans des strutures internes
        """
        if self.analyze_all_auteurs:
            self.auteurs = []
            self.set_auteurs()
        else:
            self.auteurs = []
            self.auteurs.append(self.auteur)

        auteurs = []
        for auteur in self.auteurs:
            auteur = {"nom": auteur, "mots": {}}

            oeuvres = self.get_aut_files(auteur["nom"])

            for oeuvre in oeuvres:
                auteur["mots"].update(self.get_freq_mots(oeuvre))
            auteurs.append(auteur)

        self.auteurs = auteurs

        if self.do_get_nth_ngram:
            for auteur in self.auteurs:
                ngram = self.get_nth_element(auteur["nom"], self.nth_ngram)
                print(ngram)

        if self.do_analyze:
            resultats = self.find_author(self.oeuvre)
            print(resultats)

        if self.do_gen_text:
            for auteur in self.auteurs:
                self.gen_text(auteur["nom"], self.gen_size,
                              auteur["nom"] + "_" + self.gen_basename + ".txt")

        return

    def get_freq_mots(self, oeuvre):
        """Retourne une dictionnaire de la fréquence des mors dans l'oeuvre

        Args:
            Oeuvre: L'oeuvre dans lequel on veut compter les mots

        Returns:
            Mots : Retourne un dictionnaire contenant les mots (clé) ainsi que la fréquence (valeur) d'un chacun.
        """
        mots = {}
        xgram = self.ngram
        indexToAdd = xgram - 1
        if oeuvre.endswith(".txt"):  # Vérification de l'extension du fichier
            f = open(oeuvre, "r")  # Ouverture du fichier
            # Lecture du fichier et séparation de chaque mot (séparé par : espace)
            textContent = f.read().lower().split()

            # Si le mode sans ponctuation est activé (noPonc) on repasse sur tous les mots et on
            if not self.keep_ponc:
                # vérifie s'il a un caractère parmis le tableau PONC
                formatStr = ""  # Chaîne temporaire qui sevira à remettre tout les mots sans ponctuation pour les
                # re-séparer (permet d'éviter d'avoir des indexs possédants des espaces)
                index = 0
                while index < len(textContent):  # Pour tout les mots dans le texte
                    # Pour chaque caractère dans le texte
                    for character in textContent[index]:
                        for ponctuation in self.PONC:  # Vérifier si le caractère en est un dans le tableau PONC
                            if character == ponctuation:  # Si caractère est caractère ponctué
                                textContent[index] = textContent[index].replace(character,
                                                                                ' ')  # Remplace par un espace
                    # Ajout du mot formatté dans la chaîne temporaire
                    formatStr += textContent[index] + " "
                    index = index + 1
                textContent = formatStr.split()  # Re-séparation des mots dans la liste

            index = 0
            # Boucle qui permet d'enlever tous les mots de deux caractères et moins
            while index < len(textContent):  # Pour chaque mot dans le tableau
                if len(textContent[index]) <= 2:  # Si taille du mot < 2
                    textContent.pop(index)  # Retrait du mot
                index = index + 1

            index = 0
            # Boucle permettant de placer les éléments dans le dictionnaire, permet aussi de compter chaque mot
            while index < len(textContent):  # Pour chaque mot dans le tableau
                if xgram == 1:
                    # Si la clé existe déjà dans le dictionnaire
                    if textContent[index] in mots:
                        # Mise à jour du nombre de
                        mots.update(
                            {textContent[index]: mots.get(textContent[index]) + 1})
                        # répétition du mot pour cette clé
                    else:
                        # Mettre un nouveau mot au compte de 1 si pas existant
                        mots.update({textContent[index]: 1})
                else:
                    wordListGram = ""
                    wordIndex = 0
                    while wordIndex < xgram:
                        if (index + xgram) <= len(textContent):
                            if wordIndex < indexToAdd:
                                wordListGram = wordListGram + \
                                    textContent[index + wordIndex] + " "
                            else:
                                wordListGram = wordListGram + \
                                    textContent[index + wordIndex]
                        wordIndex = wordIndex + 1
                    if wordListGram != "":
                        if wordListGram in mots:  # Si la clé existe déjà dans le dictionnaire
                            # Mise à jour du nombre de
                            mots.update(
                                {wordListGram: mots.get(wordListGram) + 1})
                            # répétition du mot pour cette clé
                        else:
                            # Mettre un nouveau mot au compte de 1 si pas existant
                            mots.update({wordListGram: 1})
                index = index + 1
        return mots

    def setup_and_parse_cli(self, args):
        """Utilise le module argparse pour:
            - Enregistrer les commandes à reconnaître
            - Lire la ligne de commande et créer le champ args qui récupère la structure produite

        Returns:
            void: Au retour, toutes les commandes reconnues sont comprises dans args
        """
        if args.d:
            self.rep_aut = args.d

        if args.m:
            self.ngram = args.m

        if args.a:
            self.auteur = args.a
            self.analyze_all_auteurs = False

        if args.A:
            self.analyze_all_auteurs = True

        if args.f:
            self.oeuvre = args.f
            self.do_analyze = True

        if args.F:
            self.do_get_nth_ngram = True
            self.nth_ngram = args.F

        if args.g:
            self.gen_basename = args.g
            self.do_gen_text = True

        if args.G:
            self.gen_size = args.G
            self.do_gen_text = True

        self.set_ponc(False)

        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', default='.',
        help="Répertoire : Pour indiquer le répertoire dans lequel se trouvent les sous-répertoires de chacun des auteurs à traiter.")
    parser.add_argument(
        '-a', help="Auteur : Pour indiquer que l'analyse se fera sur les textes de cet auteur.")
    parser.add_argument(
        '-A', help="Pour indiquer que l'analyse se fera sur le textes de tous les auteurs.")
    parser.add_argument(
        '-m', default=1, type=int, choices=range(1, 20),
        help="N-grammes : Pour faire le calcul avec des n-grammes de mots.")
    parser.add_argument(
        '-f', help="Fichier : Pour indiquer un fichier de texte à comparer.")
    parser.add_argument(
        '-F', type=int, help="Afficher l'élément le plus fréquent.")
    parser.add_argument(
        '-g', default='Gen_text', help='Nom de base du fichier de texte à générer')
    parser.add_argument(
        '-G', default=1000, type=int, help="Nombre : Produit un texte aléatoire de n mot pour chaque auteur.")
    args = parser.parse_args()

    m = markov()
    m.setup_and_parse_cli(args)
    m.analyze()
