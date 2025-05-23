from models.bank_model import BankOperation, BankCategorie, BankSousCategorie
from models.database import db
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.sql.expression import case

def get_all_operations():
    """Récupère toutes les opérations bancaires avec leurs catégories et sous-catégories."""
    return BankOperation.query.order_by(BankOperation.date.desc()).all()

def get_all_categories():
    return BankCategorie.query.order_by(BankCategorie.nom).all()

def get_all_subcategories():
    return BankSousCategorie.query.order_by(BankSousCategorie.categorie_id).all()

def add_category(nom):
    category = BankCategorie(nom=nom)
    db.session.add(category)
    return category

def update_category(category_id, nom):
    category = BankCategorie.query.get_or_404(category_id)
    category.nom = nom
    return category

def delete_category(category_id):
    category = BankCategorie.query.get_or_404(category_id)
    db.session.delete(category)

def add_subcategory(nom, categorie_id):
    subcategory = BankSousCategorie(nom=nom, categorie_id=categorie_id)
    db.session.add(subcategory)
    return subcategory

def update_subcategory(subcategory_id, nom):
    subcategory = BankSousCategorie.query.get_or_404(subcategory_id)
    subcategory.nom = nom
    return subcategory

def delete_subcategory(subcategory_id):
    subcategory = BankSousCategorie.query.get_or_404(subcategory_id)
    db.session.delete(subcategory)

def add_operation(date, label, amount, categorie_id=None, sous_categorie_id=None, supplier=None, person=None):
    """
    Ajoute une nouvelle opération bancaire.
    
    Args:
        date (date): Date de l'opération
        label (str): Libellé de l'opération
        amount (float): Montant de l'opération (positif pour un crédit, négatif pour un débit)
        categorie_id (int, optional): ID de la catégorie
        sous_categorie_id (int, optional): ID de la sous-catégorie
        supplier (str, optional): Fournisseur
        person (str, optional): Personne concernée
    """
    try:
        # Vérification de la cohérence des catégories
        if sous_categorie_id and not categorie_id:
            raise ValueError("Une sous-catégorie ne peut pas être associée sans catégorie parente")
            
        if sous_categorie_id:
            sous_categorie = BankSousCategorie.query.get(sous_categorie_id)
            if not sous_categorie:
                raise ValueError(f"Sous-catégorie {sous_categorie_id} non trouvée")
            if sous_categorie.categorie_id != categorie_id:
                raise ValueError(f"La sous-catégorie {sous_categorie_id} n'appartient pas à la catégorie {categorie_id}")
        
        # Création de l'opération
        operation = BankOperation(
            date=date,
            label=label,
            amount=amount,
            categorie_id=categorie_id,
            sous_categorie_id=sous_categorie_id,
            supplier=supplier,
            person=person
        )
        
        db.session.add(operation)
        db.session.commit()
        
        return operation
    except Exception as e:
        db.session.rollback()
        raise e

def update_operation(operation_id, date, label, amount, categorie_id=None, sous_categorie_id=None, supplier=None, person=None):
    """Met à jour une opération bancaire existante."""
    operation = BankOperation.query.get_or_404(operation_id)
    operation.date = datetime.strptime(date, '%Y-%m-%d')
    operation.label = label
    operation.amount = amount
    operation.debit = abs(amount) if amount < 0 else None
    operation.credit = amount if amount > 0 else None
    operation.categorie_id = categorie_id
    operation.sous_categorie_id = sous_categorie_id
    operation.supplier = supplier
    operation.person = person
    db.session.commit()
    return operation

def delete_operation(operation_id):
    """Supprime une opération bancaire."""
    operation = BankOperation.query.get_or_404(operation_id)
    db.session.delete(operation)
    db.session.commit()

def get_last_six_months_analysis(category_id=None):
    """Retourne les totaux par mois pour les 6 derniers mois."""
    month_label = func.strftime('%Y-%m', BankOperation.date).label('month')
    query = db.session.query(
        month_label,
        func.sum(BankOperation.amount).label('total')
    ).group_by(month_label).order_by(month_label.asc())

    if category_id:
        query = query.filter(BankOperation.categorie_id == category_id)

    query = query.limit(6)  # Applique la limite après le filtre

    return [{"month": row.month, "total": row.total} for row in query.all()]

def get_last_four_months_summary(category_id=None):
    """Retourne les débits, crédits et totaux pour les 4 derniers mois."""
    month_label = func.strftime('%Y-%m', BankOperation.date).label('month')
    debits_case = case((BankOperation.amount < 0, BankOperation.amount), else_=0)
    credits_case = case((BankOperation.amount > 0, BankOperation.amount), else_=0)

    query = db.session.query(
        month_label,
        func.coalesce(func.sum(debits_case), 0).label('debits'),  # Utilisez coalesce pour remplacer NULL par 0
        func.coalesce(func.sum(credits_case), 0).label('credits')  # Utilisez coalesce pour remplacer NULL par 0
    ).group_by(month_label).order_by(month_label.asc())

    if category_id:
        query = query.filter(BankOperation.categorie_id == category_id)

    query = query.limit(4)

    return [{"month": row.month, "debits": row.debits, "credits": row.credits} for row in query.all()]