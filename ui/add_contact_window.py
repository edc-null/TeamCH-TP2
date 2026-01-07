from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox)
from PyQt6.QtCore import Qt

from db.database import Database
from models.contact import Contact
from catch.input_errors import Catch

class AddContactWindow(QWidget):
    def __init__(self, contact_data=None, on_save_callback=None):
        # Appel du constructeur de la classe parente QWidget
        super().__init__()

        # Données du contact à modifier (None si on est en mode ajout)
        # Contient : (id, nom, prénom, téléphone, courriel)
        self.contact_data = contact_data

        # Fonction de rappel (callback) appelée après un enregistrement réussi
        # Permet de rafraîchir la table dans la fenêtre principale
        self.on_save_callback = on_save_callback

        # Identifiant SQLite du contact
        # Utilisé uniquement en mode modification
        self.contact_id = None

        self.setWindowTitle("Modifier un contact" if contact_data else "Ajouter un contact")
        self.setMinimumSize(420, 280)

        #Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        #Titre
        title = QLabel(self.windowTitle())
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

        #Formulaire
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.input_nom = QLineEdit()
        self.input_prenom = QLineEdit()
        self.input_telephone = QLineEdit()
        self.input_email = QLineEdit()

        self.input_nom.setPlaceholderText("Nom")
        self.input_prenom.setPlaceholderText("Prénom")
        self.input_telephone.setPlaceholderText("Téléphone")
        self.input_email.setPlaceholderText("exemple@domaine.com")

        form_layout.addRow("Nom :", self.input_nom)
        form_layout.addRow("Prénom :", self.input_prenom)
        form_layout.addRow("Téléphone :", self.input_telephone)
        form_layout.addRow("Courriel :", self.input_email)

        # Si des données de contact sont fournies, la fenêtre est en mode édition
        if contact_data:
            # Extraction de l'identifiant unique et des informations du contact
            # Ces données proviennent de la sélection dans la QTableView
            self.contact_id, nom, prenom, telephone, email = contact_data

            # Initialisation des champs du formulaire avec les données existantes
            # afin de permettre à l'utilisateur de modifier le contact
            self.input_nom.setText(nom)
            self.input_prenom.setText(prenom)
            self.input_telephone.setText(telephone)
            self.input_email.setText(email)

        #Boutons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        btn_save = QPushButton("Enregistrer")
        btn_cancel = QPushButton("Annuler")

        btn_save.setMinimumWidth(110)
        btn_cancel.setMinimumWidth(110)

        btn_save.clicked.connect(self.save_contact)
        btn_cancel.clicked.connect(self.close)

        button_layout.addWidget(btn_save)
        button_layout.addWidget(btn_cancel)

        #Assemblage
        main_layout.addWidget(title)
        main_layout.addLayout(form_layout)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    # Sauvegarde (AJOUT ou MODIFICATION)
    def save_contact(self):
        # Récupération des valeurs
        nom = self.input_nom.text()
        prenom = self.input_prenom.text()
        telephone = self.input_telephone.text()
        email = self.input_email.text()

        field_map = {
            "nom": [self.input_nom],
            "prenom": [self.input_prenom],
            "telephone": [self.input_telephone],
            "email": [self.input_email]
        }

        # Réinitialise le style de tous les champs du formulaire
        # Cela permet de supprimer les bordures rouges ajoutées
        # lors d'une validation précédente
        for widgets in field_map.values():
            for widget in widgets:
                widget.setStyleSheet("")

        # Validation des input par catch
        is_valid, field, message = Catch.validate_contact(
            nom, prenom, telephone, email
        )

        if not is_valid:
            for widget in field_map[field]:
                widget.setStyleSheet("border: 2px solid red;")
                widget.setFocus()  # Place le curseur sur le champ invalide

            QMessageBox.warning(self, "Erreur de validation", message)
            return

        # Création de l'objet Contact
        contact = Contact(nom=nom, prenom=prenom, telephone=telephone, email=email)
        db = Database()

        # Si des données de contact existent, cela signifie que l'utilisateur modifie un contact déjà présent dans la base de données
        if self.contact_data:
            # Exécution d'une requête UPDATE en utilisant l'identifiant SQLite
            db.update_contact(self.contact_id, contact)
            message = "Contact modifié avec succès."
        else:
            # Aucun contact existant : création d'un nouveau contact
            # Exécution d'une requête INSERT
            db.add_contact(contact)
            message = "Contact ajouté avec succès."

        QMessageBox.information(self, "Succès", message)

        # Vérifie si une fonction de rappel (callback) a été fournie
        # Si oui, elle est appelée après l'enregistrement réussi
        # afin de rafraîchir la liste des contacts dans la fenêtre principale
        if self.on_save_callback:
            self.on_save_callback()

        self.close()
