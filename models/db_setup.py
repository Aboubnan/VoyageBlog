import sqlite3

# Définition du chemin vers le fichier de BDD
DB_PATH = "database/blog.db"

def setup_database():
    """Crée la base de données et les tables nécessaires."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # --- 1. Table Catégorie ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Categorie (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL UNIQUE
        );
    """)

    # --- 2. Table Article ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Article (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            contenu TEXT NOT NULL,
            auteur TEXT NOT NULL,
            date_pub TEXT NOT NULL,
            image_url TEXT,
            categorie_id INTEGER,
            FOREIGN KEY (categorie_id) REFERENCES Categorie(id)
        )
    """)

    # --- 3. Table Contact (pour le Formulaire de Comptage/Abonnement) ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Contact (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            email TEXT NOT NULL UNIQUE,
            message TEXT,
            date_soumission TEXT NOT NULL
        );
    """)

    conn.commit()
    conn.close()
    print("Base de données et tables créées avec succès.")

if __name__ == '__main__':
    setup_database()