import sqlite3
from models.contact import Contact


class Database:
    def __init__(self, db_path="contacts.db"):
        # Chemin vers le fichier de base de données SQLite
        # Si le fichier n'existe pas, SQLite le créera automatiquement
        self.db_path = db_path

        # Création automatique de la table des contacts
        # Cette méthode est appelée au démarrage pour garantir que la structure de la base existe
        self._create_table()

    def connect(self):
        # Crée et retourne une connexion SQLite vers le fichier de base de données
        # Cette connexion sera utilisée pour exécuter les requêtes SQL
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        # Ouverture d'une connexion SQLite
        conn = self.connect()

        # Le curseur permet d'envoyer des commandes SQL à la base
        cursor = conn.cursor()

        # Création de la table contacts avec une clé primaire auto-incrémentée
        # Les champs sont définis comme NOT NULL afin de garantir l'intégrité des données
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS contacts
                       (
                           id        INTEGER PRIMARY KEY AUTOINCREMENT, -- Clé primaire unique pour chaque contact | AUTOINCREMENT garantit un identifiant unique généré automatiquement
                           nom       TEXT NOT NULL,    -- Nom du contact (obligatoire)
                           prenom    TEXT NOT NULL,    -- Prénom du contact (obligatoire)
                           telephone TEXT NOT NULL,    -- Numéro de téléphone du contact (obligatoire)
                           email     TEXT NOT NULL     -- Adresse courriel du contact (obligatoire)
                       )
                       """)

        # Sauvegarde permanente des changements effectués
        conn.commit()

        # Fermeture explicite de la connexion à la base de données
        conn.close()

    # CRUD
    def add_contact(self, contact: Contact):
        conn = self.connect()
        cursor = conn.cursor()
        # Insertion d'un nouvel enregistrement dans la table contacts
        # L'utilisation de paramètres (?, ?, ?, ?) protège contre les injections SQL
        # et assure une liaison sécurisée des valeurs
        cursor.execute("""
                       INSERT INTO contacts (nom, prenom, telephone, email) 
                       -- Indique que l’on veut ajouter un nouvel enregistrement | La table ciblée est contacts
                       -- Liste des colonnes dans lesquelles les données seront insérées et l’ordre est important : il doit correspondre aux valeurs fournies ensuite
                       VALUES (?, ?, ?, ?)
                       -- Les ? sont des paramètres SQL (placeholders) | Ils seront remplacés par des valeurs réelles au moment de l’exécution | Chaque ? correspond à une colonne listée au-dessus
                       """,
                       (contact.nom, contact.prenom, contact.telephone, contact.email))
        conn.commit()
        conn.close()

    def get_all_contacts(self):
        # Ouverture d'une connexion vers la base SQLite
        conn = self.connect()

        # Le curseur permet d'exécuter des requêtes SQL
        cursor = conn.cursor()

        # Lecture de tous les enregistrements de la table contacts
        # Chaque ligne contient l'identifiant et les informations du contact
        cursor.execute("""
                       SELECT id, nom, prenom, telephone, email
                       FROM contacts
                       """)

        # fetchall() retourne une liste de tuples
        # Chaque tuple représente un contact
        rows = cursor.fetchall()

        conn.close()

        # Les données sont retournées à la couche interface (UI)
        return rows

    def delete_contact(self, contact_id):
        conn = self.connect()
        cursor = conn.cursor()
        # Suppression d'un enregistrement dans la table contacts
        # La WHERE garantit que seul le contact correspondant à l'identifiant SQLite fourni sera supprimé
        cursor.execute("""
                       DELETE
                       FROM contacts
                       WHERE id = ?
                       """, (contact_id,))
        conn.commit()
        conn.close()

    def update_contact(self, contact_id, contact):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE contacts -- Met à jour un contact existant dans la table contacts
            SET nom = ?, prenom = ?, telephone = ?, email = ? -- Définit les nouvelles valeurs des champs du contact
            WHERE id = ? -- Condition obligatoire pour cibler un seul contact | L'identifiant (id) provient de la clé primaire SQLite
        """, (contact.nom, contact.prenom, contact.telephone, contact.email, contact_id))
        conn.commit()
        conn.close()
