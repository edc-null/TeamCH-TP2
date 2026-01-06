import webbrowser
from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTableView, QMessageBox)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt

from ui.add_contact_window import AddContactWindow
from db.database import Database

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Carnet d'adresses")
        self.setMinimumSize(800, 450)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        #Titre
        title = QLabel("Carnet d'adresses")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        #Table
        # Création de la table qui affichera les contacts
        self.table = QTableView()

        # Lorsqu'un utilisateur clique sur une cellule,
        # toute la ligne (le contact complet) est sélectionnée
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

        # Empêche la sélection de plusieurs lignes en même temps
        # (une seule personne peut être modifiée ou supprimée à la fois)
        self.table.setSelectionMode(QTableView.SelectionMode.SingleSelection)

        # Désactive l'édition directe des cellules dans la table
        # Les modifications doivent se faire via la fenêtre "Modifier un contact"
        self.table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)

        # Création du modèle de données qui contiendra les contacts
        # Ce modèle fait le lien entre les données (SQLite) et l'affichage (QTableView)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Nom", "Prénom", "Téléphone", "Courriel"])

        # Association du modèle à la table
        # La QTableView affichera automatiquement le contenu du modèle
        self.table.setModel(self.model)

        # Ajuste automatiquement la largeur de la dernière colonne
        # pour occuper tout l'espace disponible dans la table
        self.table.horizontalHeader().setStretchLastSection(True)

        #Boutons
        btn_layout = QHBoxLayout()

        btn_add = QPushButton("Ajouter")
        btn_edit = QPushButton("Modifier")
        btn_delete = QPushButton("Supprimer")
        btn_refresh = QPushButton("Actualiser")
        btn_quit = QPushButton("Quitter")
        btn_aide = QPushButton("Aide et à propos de")

        btn_add.clicked.connect(self.open_add_window)
        btn_edit.clicked.connect(self.edit_contact)
        btn_delete.clicked.connect(self.delete_contact)
        btn_refresh.clicked.connect(self.load_contacts_from_db)
        btn_quit.clicked.connect(self.close)
        btn_aide.clicked.connect(self.open_website)

        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        btn_layout.addWidget(btn_refresh)
        btn_layout.addWidget(btn_aide)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_quit)

        # ----- Assemblage -----
        main_layout.addWidget(title)
        main_layout.addWidget(self.table)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

        # Référence vers la fenêtre "Ajouter / Modifier un contact"
        # Initialisée à None pour éviter toute référence invalide
        self.add_window = None

        # Chargement initial des contacts depuis la base de données SQLite
        # Cette méthode remplit la table dès l'ouverture de l'application
        self.load_contacts_from_db()


    #Actions
    def open_add_window(self):
        # Instancie la fenêtre d'ajout de contact
        # La fonction load_contacts_from_db est passée comme callback
        # afin de rafraîchir la QTableView après l'enregistrement en base SQLite
        self.add_window = AddContactWindow(on_save_callback=self.load_contacts_from_db)
        self.add_window.show()

    def edit_contact(self):
        index = self.table.currentIndex()
        if not index.isValid():
            QMessageBox.warning(
                self,
                "Aucune sélection",
                "Veuillez sélectionner un contact à modifier."
            )
            return

        # Obtient l'indice de la ligne sélectionnée dans la QTableView
        row = index.row()

        # Extrait l'identifiant unique du contact depuis le modèle
        # Cet identifiant provient de la base SQLite et est stocké
        # dans la colonne "Nom" à l'aide du rôle UserRole
        contact_id = self.model.item(row, 0).data(Qt.ItemDataRole.UserRole)

        contact_data = (
            contact_id,
            self.model.item(row, 0).text(),
            self.model.item(row, 1).text(),
            self.model.item(row, 2).text(),
            self.model.item(row, 3).text()
        )

        # Instancie la fenêtre d'ajout/modification en mode édition
        # Les données du contact sélectionné sont passées afin de préremplir le formulaire
        # Un callback est fourni pour recharger les données après la mise à jour SQLite
        self.add_window = AddContactWindow(contact_data=contact_data, on_save_callback=self.load_contacts_from_db)
        self.add_window.show()

    def delete_contact(self):
        index = self.table.currentIndex()
        if not index.isValid():
            QMessageBox.warning(
                self,
                "Aucune sélection",
                "Veuillez sélectionner un contact à supprimer."
            )
            return

        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Voulez-vous vraiment supprimer ce contact ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        # Vérifie si l'utilisateur a confirmé l'action de suppression
        if reply == QMessageBox.StandardButton.Yes:
            # Extraction de l'identifiant unique du contact depuis le modèle
            # Cet identifiant permet d'effectuer la suppression dans SQLite
            contact_id = self.model.item(index.row(), 0).data(Qt.ItemDataRole.UserRole)

            # Instanciation de la classe de gestion de la base de données
            db = Database()

            # Exécution de l'opération DELETE sur la table contacts
            db.delete_contact(contact_id)

            self.load_contacts_from_db()

    def load_contacts_from_db(self):
        # Efface toutes les lignes du QStandardItemModel
        # Cette opération est nécessaire avant de recharger les données
        # depuis SQLite pour éviter les doublons dans la table
        self.model.removeRows(0, self.model.rowCount())
        db = Database()
        contacts = db.get_all_contacts()

        for contact in contacts:
            contact_id, nom, prenom, telephone, email = contact

            row = [
                QStandardItem(nom),
                QStandardItem(prenom),
                QStandardItem(telephone),
                QStandardItem(email)
            ]

            # Stocker l'ID SQLite dans la première colonne
            row[0].setData(contact_id, Qt.ItemDataRole.UserRole)

            self.model.appendRow(row)

    def open_website(self):
        webbrowser.open_new("http://localhost:63342/TeamCH-TP2/Website/index.html?_ijt=ndj24pg7rlvsukdi3ov67r25ek&_ij_reload=RELOAD_ON_SAVE#")