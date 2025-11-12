import sqlite3
from datetime import datetime

DB_PATH = 'database/blog.db'

def get_db_connection():
    """Ouvre et retourne une connexion à la base de données."""
    conn = sqlite3.connect(DB_PATH)
    # Permet de récupérer les résultats par noms de colonnes (dictionnaire)
    conn.row_factory = sqlite3.Row 
    return conn

# --- Fonctions CRUD (Read) ---

def get_all_articles():
    conn = get_db_connection()
    articles = conn.execute("""
        SELECT 
            A.id, 
            A.titre, 
            A.contenu, 
            A.auteur, 
            A.date_pub, 
            A.categorie_id, 
            A.image_url,  -- <--- CORRECTION : Suppression des astérisques (**)
            C.nom AS categorie_nom
        FROM Article A
        JOIN Categorie C ON A.categorie_id = C.id
        ORDER BY A.date_pub DESC
    """).fetchall()
    conn.close()
    return articles

def get_article_by_id(article_id):
    """Récupère un article spécifique par son ID."""
    conn = get_db_connection()
    article = conn.execute("""
        SELECT A.*, C.nom AS categorie_nom
        FROM Article A
        JOIN Categorie C ON A.categorie_id = C.id
        WHERE A.id = ?
    """, (article_id,)).fetchone()
    conn.close()
    return article

# --- Fonction d'Insertion pour le Formulaire (Étape 10) ---

def insert_contact_message(nom, email, message):
    """Insère un message de contact complet (Nom, Email, Message)."""
    conn = get_db_connection()
    date_soumission = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        conn.execute(
            "INSERT INTO Contact (nom, email, message, date_soumission) VALUES (?, ?, ?, ?)",
            (nom, email, message, date_soumission)
        )
        conn.commit()
        return True
    except sqlite3.Error: # Capture les erreurs SQL génériques
        return False
    finally:
        conn.close()

def insert_subscriber_email(email):
    """Insère un email pour l'abonnement à la newsletter (doit être unique)."""
    # NOTE : Si vous n'avez pas de table 'Abonnement', vous devez d'abord la créer
    #        dans db_setup.py. Supposons qu'elle s'appelle 'Abonnement'.
    conn = get_db_connection()
    date_soumission = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        conn.execute(
            "INSERT INTO Abonnement (email, date_inscription) VALUES (?, ?)",
            (email, date_soumission)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError: # L'email existe déjà (contrainte UNIQUE)
        return False
    finally:
        conn.close()