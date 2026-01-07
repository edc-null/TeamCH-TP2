import re

# Classe responsable de la validation des entrées de l'utilisateur
class Catch:

    @staticmethod
    def input_nom(value: str):
        if not value.strip(): # Vérifie d’abord si le champ est vide
            return False, "nom", "Ce champ ne peut pas être vide."

        regex = r"^[A-Za-zÀ-ÖØ-öø-ÿ\s\-']+$" # Accepte les accents, espaces, tirets, apostrophes
        if not re.fullmatch(regex, value):
            return False, "nom", "Le nom contient des caractères invalides."

        return True, None, ""

    @staticmethod
    def input_prenom(value: str):
        if not value.strip(): # Vérifie d’abord si le champ est vide
            return False, "prenom", "Ce champ ne peut pas être vide."

        regex = r"^[A-Za-zÀ-ÖØ-öø-ÿ\s\-']+$" # Accepte les accents, espaces, tirets, apostrophes
        if not re.fullmatch(regex, value):
            return False, "prenom", "Le prénom contient des caractères invalides."

        return True, None, ""

    @staticmethod
    def input_tel(value: str):
        if not value.strip(): # Vérifie d’abord si le champ est vide
            return False, "telephone", "Le numéro de téléphone est obligatoire."

        regex = r"^[0-9()\-\s]{7,20}$" # accepte chiffres, parenthèses, espaces, tiret, entre 7 et 20 caractères
        if not re.fullmatch(regex, value):
            return False, "telephone", "Format de numéro de téléphone invalide."

        return True, None, ""

    @staticmethod
    def input_email(value: str):
        if not value.strip(): # Vérifie d’abord si le champ est vide
            return False, "email", "L'adresse courriel est obligatoire."

        regex = r"^[A-Za-z0-9._\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$" # vérifie qu'il commence par des lettres, point,
        # tiret ou barre de soulignement. Suivi par nom de domaine et par extension de domaine.
        if not re.fullmatch(regex, value):
            return False, "email", "Format d'adresse courriel invalide."

        return True, None, ""

    # Méthode qui renvoit exactement quel champ pose problème
    @staticmethod
    def validate_contact(nom, prenom, telephone, email):
        validations = [
            Catch.input_nom(nom),
            Catch.input_prenom(prenom),
            Catch.input_tel(telephone),
            Catch.input_email(email)
        ]

        for is_valid, field, message in validations:
            if not is_valid:
                return False, field, message
                # False → contact invalide
                # field → nom du champ à colorer
                # message → message d’erreur à afficher

        return True, None, ""
