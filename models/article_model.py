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
    """Récupère tous les articles avec le nom de leur catégorie."""
    conn = get_db_connection()
    articles = conn.execute("""
        SELECT 
            A.id, A.titre, SUBSTR(A.contenu, 1, 150) AS resume, 
            A.auteur, A.date_pub, C.nom AS categorie_nom
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

def insert_contact(nom, email, message):
    """Insère un nouvel enregistrement de contact dans la table Contact."""
    conn = get_db_connection()
    date_soumission = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        conn.execute(
            "INSERT INTO Contact (nom, email, message, date_soumission) VALUES (?, ?, ?, ?)",
            (nom, email, message, date_soumission)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Gère le cas où l'email est déjà présent (UNIQUE)
        return False
    finally:
        conn.close()