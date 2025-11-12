import sqlite3
from datetime import datetime

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

    # --- 2. Récupération des IDs ---
    europe_id = cursor.execute("SELECT id FROM Categorie WHERE nom='Europe'").fetchone()[0]
    asie_id = cursor.execute("SELECT id FROM Categorie WHERE nom='Asie'").fetchone()[0]
    amerique_id = cursor.execute("SELECT id FROM Categorie WHERE nom='Amérique du Sud'").fetchone()[0]

    # --- 3. Insertion des Articles (10+ Exemples avec URL Internet) ---
    # Le format des données est : (titre, contenu, auteur, date_pub, image_url, categorie_id)
    articles = [
        # Les URLs pointent vers des images de placeholder externes
        ("Aventure à Lisbonne : Pastel de Nata et Fado", 
         "Ceci est le contenu complet de mon article sur Lisbonne, une ville magnifique et colorée...", 
         "Alex V.", "2025-11-01", "https://picsum.photos/id/160/600/400", europe_id),
        
        ("Road Trip en Irlande : Le vert est partout", 
         "De Dublin aux falaises de Moher, le vert est partout. Préparez-vous à affronter la pluie...", 
         "Chris M.", "2025-10-15", "https://picsum.photos/id/157/600/400", europe_id),
         
        ("Randonnée dans les Dolomites : L'Italie au sommet", 
         "Découvrez les plus belles randonnées en Italie. Des lacs turquoise aux pics rocheux, une aventure inoubliable...", 
         "Laura S.", "2025-09-08", "https://picsum.photos/id/212/600/400", europe_id),
         
        ("Séjour romantique à Venise : Secrets des Canaux", 
         "Flânerie dans les ruelles, tour en gondole et dégustation de spritz. Venise est toujours une ville magique...", 
         "Sophie B.", "2025-08-20", "https://picsum.photos/id/238/600/400", europe_id),
         
        ("Les Temples Cachés de Kyoto : Voyage spirituel", 
         "Un voyage spirituel à travers les jardins zen et les temples moins connus. La saison des cerisiers en fleurs est magique.", 
         "Léa K.", "2025-10-25", "https://picsum.photos/id/21/600/400", asie_id),
         
        ("Immersion à Hanoi : Le Vietnam vibrant", 
         "Le bruit, les odeurs, la foule... Hanoi est une ville qui ne dort jamais. Conseils pour traverser la route...", 
         "Marc D.", "2025-09-28", "https://picsum.photos/id/1018/600/400", asie_id),
         
        ("Trekking au Népal : Face aux Annapurnas", 
         "Une expérience physique et mentale au cœur de l'Himalaya. Des paysages grandioses et des rencontres humaines marquantes.", 
         "Elsa R.", "2025-08-10", "https://picsum.photos/id/354/600/400", asie_id),
         
        ("Canyon de Colca, Pérou : Sur la route des Condors", 
         "Le deuxième plus profond canyon du monde. Récit de notre exploration et de nos observations du majestueux condor des Andes.", 
         "David P.", "2025-11-05", "https://picsum.photos/id/1080/600/400", amerique_id),
         
        ("Rio de Janeiro : Entre plages et Favelas", 
         "Découverte de la 'Cidade Maravilhosa'. Conseils pour la sécurité, les plages de Copacabana et la montée au Corcovado.", 
         "Karim Z.", "2025-07-22", "https://picsum.photos/id/1041/600/400", amerique_id),
         
        ("Patagonie : Glaciers et Fin du Monde", 
         "Une région sauvage et extrême, parfaite pour les amoureux de la nature. Récit de notre randonnée sur le Perito Moreno.", 
         "Julie A.", "2025-06-01", "https://picsum.photos/id/1025/600/400", amerique_id)
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO Article (titre, contenu, auteur, date_pub, image_url, categorie_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, articles)

    conn.commit()
    conn.close()
    print("Articles insérés.")

if __name__ == '__main__':
    insert_initial_data()
    print("Seeding de la base de données terminé.")