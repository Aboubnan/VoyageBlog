# app.py (Le Contrôleur)

from flask import Flask, render_template, request, redirect, url_for, flash
import models.article_model as article_model # Importation du Modèle (Axe 1)
from datetime import datetime

app = Flask(__name__)
# Clé secrète nécessaire pour les sessions (messages flash) et la sécurité
# REMPLACER CECI par une clé secrète forte en production !
app.config['SECRET_KEY'] = 'une_cle_secrete_tres_faible_pour_dev' 

# Fonction utilitaire pour le pied de page Jinja2
app.jinja_env.globals.update(now=datetime.now)

# ----------------------------------------------------------------------
# F1 & F2 : Routes d'Affichage des Articles
# ----------------------------------------------------------------------

@app.route('/')
def home():
    """Affiche la page d'accueil avec la liste des articles."""
    # 1. Requête au Modèle (M)
    articles = article_model.get_all_articles() 
    
    # 2. Rendu de la Vue (V)
    # articles est passé au template index.html (Axe 2)
    return render_template('index.html', articles=articles) 


@app.route('/article/<int:article_id>')
def show_article(article_id):
    """Affiche le contenu complet d'un seul article."""
    # 1. Requête au Modèle (M)
    article = article_model.get_article_by_id(article_id)
    
    # Gestion d'erreur (si l'article n'existe pas)
    if article is None:
        return render_template('404.html'), 404 # Nécessite la création d'un template 404.html
    
    # 2. Rendu de la Vue (V)
    return render_template('article_detail.html', article=article)


# ----------------------------------------------------------------------
# F4 : Route du Formulaire de Comptage/Contact
# ----------------------------------------------------------------------

# NOUVELLE ROUTE : Page "À Propos"
@app.route('/about')
def about():
    """Affiche la page statique À Propos."""
    # Ne fait pas appel au Modèle, renvoie une Vue simple
    return render_template('about.html') # Nécessite la création de about.html

# MODIFICATION : La route /contact gère maintenant UNIQUEMENT le formulaire de contact
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Gère l'affichage du formulaire de contact et l'envoi du message."""
    if request.method == 'POST':
        # Récupère les données du formulaire de contact
        nom = request.form['nom']
        email = request.form['email']
        message = request.form['message']
        
        # NOTE : Vous devez ajouter une nouvelle fonction dans article_model.py
        #       pour gérer spécifiquement l'insertion des contacts.
        success = article_model.insert_contact_message(nom, email, message) 
        
        if success:
            flash('Merci ! Votre message a été envoyé avec succès.', 'success')
        else:
            flash('Erreur lors de l\'envoi du message. Veuillez réessayer.', 'danger')
            
        return redirect(url_for('contact')) 

    # Rendu de la Vue contact.html (GET)
    return render_template('contact.html')


# NOUVELLE ROUTE : Formulaire d'Abonnement (Newsletter)
@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    """Gère l'affichage du formulaire d'abonnement et la soumission de l'email."""
    if request.method == 'POST':
        email = request.form['email']
        
        # NOTE : Vous devez ajouter une fonction dans article_model.py
        #       pour gérer l'insertion des emails d'abonnement.
        success = article_model.insert_subscriber_email(email)
        
        if success:
            flash('Félicitations ! Votre abonnement à la newsletter est confirmé.', 'success')
        else:
            flash('Cet email est déjà abonné ou les données sont invalides.', 'danger')
            
        return redirect(url_for('subscribe')) 

    # Rendu de la Vue subscribe.html (GET)
    return render_template('subscribe.html')

# ----------------------------------------------------------------------

if __name__ == '__main__':
    # Initialisation de la BDD si elle n'existe pas (optionnel mais pratique)
    # Vous devez importer et exécuter models.db_setup.setup_database() ici si nécessaire
    app.run(debug=True)