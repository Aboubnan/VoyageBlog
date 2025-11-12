import sqlite3
# Assurez-vous d'avoir la fonction get_db_connection() disponible, 
# soit en l'important, soit en la copiant ici si vous ne voulez pas créer de dépendance.
# Pour l'exemple, nous allons la redéfinir :
DB_PATH = 'database/blog.db'

def get_db_connection():
    """Ouvre et retourne une connexion à la base de données."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row 
    return conn

def insert_initial_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # --- 1. Insertion des Catégories ---
    categories = [
        ("Europe",),
        ("Asie",),
        ("Amérique du Sud",)
    ]
    cursor.executemany("INSERT OR IGNORE INTO Categorie (nom) VALUES (?)", categories)
    conn.commit()
    print("Catégories insérées.")

    # --- 2. Récupération des IDs pour les Articles ---
    europe_id = cursor.execute("SELECT id FROM Categorie WHERE nom='Europe'").fetchone()[0]
    asie_id = cursor.execute("SELECT id FROM Categorie WHERE nom='Asie'").fetchone()[0]

    # --- 3. Insertion des Articles (Jeu de Données) ---
    articles = [
        ("Aventure à Lisbonne", "Ceci est le contenu complet de mon article sur Lisbonne, une ville magnifique et colorée. On y a mangé des Pastéis de Nata incroyables...", "Alex V.", "2025-11-01", europe_id),
        ("Les Temples Cachés de Kyoto", "Un voyage spirituel à travers les jardins zen et les temples moins connus. La saison des cerisiers en fleurs est magique.", "Léa K.", "2025-10-25", asie_id),
        ("Road Trip en Irlande", "De Dublin aux falaises de Moher, le vert est partout. Préparez-vous à affronter la pluie et à boire beaucoup de thé !", "Chris M.", "2025-10-15", europe_id)
    ]

    # On utilise INSERT OR IGNORE pour éviter les erreurs si la table est déjà remplie
    cursor.executemany("""
        INSERT OR IGNORE INTO Article (titre, contenu, auteur, date_pub, categorie_id)
        VALUES (?, ?, ?, ?, ?)
    """, articles)

    conn.commit()
    conn.close()
    print("Articles insérés.")

if __name__ == '__main__':
    # Assurez-vous que le script db_setup.py a déjà été exécuté !
    insert_initial_data()
    print("Seeding de la base de données terminé.")