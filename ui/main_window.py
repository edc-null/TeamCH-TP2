import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox, QMessageBox)
from PyQt6.QtCore import Qt

# Fenêtre : Ajouter un enregistrement

class AjouterContact(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ajouter un enregistrement")
        self.setMinimumSize(420, 280)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        title = QLabel("Ajouter un contact")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

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

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        btn_save = QPushButton("Enregistrer")
        btn_cancel = QPushButton("Annuler")

        btn_save.setMinimumWidth(110)
        btn_cancel.setMinimumWidth(110)

        btn_cancel.clicked.connect(self.close)
        btn_save.clicked.connect(self.enregistre_contact)

        button_layout.addWidget(btn_save)
        button_layout.addWidget(btn_cancel)

        main_layout.addWidget(title)
        main_layout.addLayout(form_layout)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def enregistre_contact(self):

        fields = [self.input_nom, self.input_prenom, self.input_telephone, self.input_email]

        has_error = False

        # Réinitialisation des styles
        for field in fields:
            field.setStyleSheet("")

        # Validation visuelle
        for field in fields:
            if not field.text().strip():
                field.setStyleSheet("border: 2px solid red;")
                has_error = True

        if has_error:
            QMessageBox.warning(
                self,
                "Erreur",
                "Veuillez remplir tous les champs obligatoires."
            )
            return

        # Message de succès (simulation)
        QMessageBox.information(
            self,
            "Succès",
            "L'enregistrement a été ajouté avec succès."
        )

        # Fermeture automatique après succès
        self.close()


# Fenêtre principale

class FenetrePrincipal(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Carnet d'adresses")
        self.setMinimumSize(420, 380)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)

        title = QLabel("Carnet d'adresses")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        subtitle = QLabel("Menu principal")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px; color: gray;")

        actions_group = QGroupBox("Actions disponibles")
        actions_layout = QVBoxLayout()
        actions_layout.setSpacing(10)

        btn_init_db = QPushButton("Initialiser / Créer la base de données")
        btn_add = QPushButton("Ajouter un enregistrement")
        btn_edit = QPushButton("Modifier un enregistrement")
        btn_delete = QPushButton("Supprimer un enregistrement")
        btn_refresh = QPushButton("Actualiser le carnet")

        for btn in (btn_init_db, btn_add, btn_edit, btn_delete, btn_refresh):
            btn.setMinimumHeight(40)
            actions_layout.addWidget(btn)

        actions_group.setLayout(actions_layout)

        btn_add.clicked.connect(self.open_add_window)
        btn_refresh.clicked.connect(self.refresh_carnet)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()

        btn_quit = QPushButton("Quitter l'application")
        btn_quit.setMinimumHeight(35)
        btn_quit.setStyleSheet("""
            background-color: #b00020;
            color: white;
            font-weight: bold;
        """)

        btn_quit.clicked.connect(QApplication.instance().quit)

        bottom_layout.addWidget(btn_quit)

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addWidget(actions_group)
        main_layout.addStretch()
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

        self.add_window = None

    def open_add_window(self):
        self.add_window = AjouterContact()
        self.add_window.show()

    def refresh_carnet(self):
        QMessageBox.information(
            self,
            "Actualisation",
            "Le carnet d'adresses a été actualisé (simulation)."
        )


# Point d'entrée

def main():
    app = QApplication(sys.argv)
    window = FenetrePrincipal()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
