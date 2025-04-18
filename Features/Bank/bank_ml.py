from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from models.bank_model import BankOperation, BankCategorie, BankSousCategorie
from models.database import db
from flask import current_app
import numpy as np
import re
import pickle
import base64
import sys

def print_log(message):
    """Fonction utilitaire pour afficher les logs"""
    print(f"[BANK_ML] {message}", file=sys.stdout, flush=True)

class CategoryPredictor:
    def __init__(self):
        print_log("Initialisation du prédicteur de catégories...")
        self.vectorizer = TfidfVectorizer(
            analyzer='char_wb',
            ngram_range=(2, 4),
            max_features=1000
        )
        self.train_data = []
        self.train_labels = []
        self.train_sub_labels = []
        self.is_trained = False
        print_log("Prédicteur initialisé avec succès")
        print_log(f"Configuration du vectorizer: {self.vectorizer.get_params()}")

    def clean_label(self, label):
        """Nettoie un libellé pour la comparaison"""
        print_log(f"Nettoyage du libellé: {label}")
        # Convertir en majuscules et supprimer les espaces début/fin
        clean = label.strip().upper()
        
        # Supprimer les dates et références
        clean = re.sub(r'\d{2}/\d{2}', '', clean)  # Dates JJ/MM
        clean = re.sub(r'\d{2}/\d{2}/\d{4}', '', clean)  # Dates JJ/MM/AAAA
        clean = re.sub(r'\d{8,}', '', clean)  # Numéros longs
        
        # Supprimer les caractères spéciaux sauf les chiffres
        clean = re.sub(r'[^\w\s\d]', ' ', clean)
        
        # Supprimer les espaces multiples
        clean = re.sub(r'\s+', ' ', clean)
        
        # Supprimer les mots courts (1-2 lettres)
        clean = ' '.join([word for word in clean.split() if len(word) > 2])
        
        # Normaliser certains termes
        clean = re.sub(r'PAIEMENT PAR CARTE', 'CARTE', clean)
        clean = re.sub(r'VIREMENT EN VOTRE FAVEUR', 'VIREMENT', clean)
        clean = re.sub(r'VIREMENT EMIS WEB', 'VIREMENT', clean)
        
        print_log(f"Libellé nettoyé: {clean}")
        return clean.strip()

    def load_training_data(self):
        """Charge les données d'entraînement depuis la base de données"""
        try:
            print_log("Chargement des données d'entraînement...")
            # Récupérer les opérations déjà catégorisées
            operations = BankOperation.query.filter(
                BankOperation.categorie_id.isnot(None)
            ).all()
            
            print_log(f"Nombre d'opérations trouvées: {len(operations)}")
            
            self.train_data = [self.clean_label(op.label) for op in operations]
            self.train_labels = [op.categorie_id for op in operations]
            self.train_sub_labels = [op.sous_categorie_id for op in operations]
            
            if self.train_data:
                print_log("Entraînement du modèle...")
                self.vectorizer.fit(self.train_data)
                self.is_trained = True
                print_log(f"Modèle entraîné avec {len(self.train_data)} exemples")
                print_log(f"Exemples d'entraînement: {self.train_data[:5]}")
            else:
                print_log("Aucune donnée d'entraînement trouvée")
        except Exception as e:
            print_log(f"Erreur lors du chargement des données d'entraînement: {e}")
            print_log(f"Type d'erreur: {type(e)}")
            print_log(f"Message d'erreur: {str(e)}")
            self.train_data = []
            self.train_labels = []
            self.train_sub_labels = []
            self.is_trained = False

    def train(self):
        """Entraîne le modèle avec les opérations existantes"""
        print_log("Démarrage de l'entraînement...")
        self.load_training_data()

    def predict(self, label, threshold=0.15):
        """Prédit la catégorie et sous-catégorie pour un nouveau libellé"""
        print_log(f"Début de la prédiction pour: {label}")
        
        if not self.is_trained:
            print_log("Tentative de prédiction avec un modèle non entraîné")
            return None, None

        clean_label = self.clean_label(label)
        print_log(f"Libellé nettoyé pour prédiction: '{clean_label}'")
        
        # Règles spécifiques pour certains types d'opérations
        if 'CARTE' in clean_label:
            if 'AMAZON' in clean_label:
                print_log("Règle spécifique: Paiement Amazon détecté")
                return 8, 38  # Achats en ligne
            elif 'BI' in clean_label or 'SUPERMARCHE' in clean_label:
                print_log("Règle spécifique: Paiement supermarché détecté")
                return 1, 1   # Alimentation
            elif 'FREE' in clean_label:
                print_log("Règle spécifique: Paiement Free Mobile détecté")
                return 3, 12  # Téléphonie
        
        if 'VIREMENT' in clean_label:
            if 'DRFIP' in clean_label or 'SALAIRE' in clean_label:
                print_log("Règle spécifique: Virement salaire détecté")
                return 11, 52  # Salaire
            elif 'CPAM' in clean_label or 'HENNER' in clean_label:
                print_log("Règle spécifique: Remboursement santé détecté")
                return 11, 53  # Remboursement santé
        
        print_log("Recherche de correspondances par similarité...")
        label_vector = self.vectorizer.transform([clean_label])
        train_vectors = self.vectorizer.transform(self.train_data)
        
        similarities = cosine_similarity(label_vector, train_vectors)[0]
        max_similarity_idx = np.argmax(similarities)
        
        # Afficher les 3 meilleures correspondances
        top_indices = np.argsort(similarities)[-3:][::-1]
        for idx in top_indices:
            print_log(f"Correspondance trouvée: '{self.train_data[idx]}' (similarité: {similarities[idx]:.2f})")
        
        if similarities[max_similarity_idx] >= threshold:
            print_log(f"Prédiction réussie pour '{label}' (similarité: {similarities[max_similarity_idx]:.2f})")
            return (
                self.train_labels[max_similarity_idx],
                self.train_sub_labels[max_similarity_idx]
            )
        print_log(f"Aucune prédiction fiable pour '{label}' (similarité max: {similarities[max_similarity_idx]:.2f})")
        return None, None

    def learn(self, label, categorie_id, sous_categorie_id):
        """Apprend à partir d'une nouvelle opération catégorisée"""
        print_log(f"Apprentissage d'une nouvelle opération: {label}")
        clean_label = self.clean_label(label)
        
        # Vérifier si l'exemple existe déjà
        if clean_label in self.train_data:
            idx = self.train_data.index(clean_label)
            self.train_labels[idx] = categorie_id
            self.train_sub_labels[idx] = sous_categorie_id
            print_log("Mise à jour d'un exemple existant")
        else:
            self.train_data.append(clean_label)
            self.train_labels.append(categorie_id)
            self.train_sub_labels.append(sous_categorie_id)
            print_log("Ajout d'un nouvel exemple")
        
        # Réentraîner le modèle
        self.vectorizer.fit(self.train_data)
        self.is_trained = True
        print_log(f"Modèle mis à jour avec {len(self.train_data)} exemples")

# Instance globale du prédicteur
print_log("Création de l'instance du prédicteur...")
predictor = CategoryPredictor()
print_log("Instance du prédicteur créée avec succès") 