from app import app
from models.database import db
from models.bank_model import BankOperation

with app.app_context():
    total = BankOperation.query.count()
    categorized = BankOperation.query.filter(BankOperation.categorie_id.isnot(None)).count()
    
    print(f"Nombre total d'opérations: {total}")
    print(f"Nombre d'opérations catégorisées: {categorized}")
    
    if categorized > 0:
        print("\nExemples d'opérations catégorisées:")
        for op in BankOperation.query.filter(BankOperation.categorie_id.isnot(None)).limit(5):
            print(f"- {op.label} (Catégorie: {op.categorie_id}, Sous-catégorie: {op.sous_categorie_id})") 