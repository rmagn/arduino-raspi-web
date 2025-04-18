from flask import Blueprint, render_template, request, jsonify
from utils.decorators import login_required, role_required
from Features.Bank.bank_service import (
    get_all_operations,
    get_all_categories,
    get_all_subcategories,
    add_category,
    update_category,
    delete_category,
    add_subcategory,
    update_subcategory,
    delete_subcategory,
    add_operation,
    update_operation,
    delete_operation
)
from models.database import db
from models.bank_model import BankSousCategorie, BankOperation
from datetime import datetime, timedelta
import re
from Features.Bank.bank_ml import predictor
import logging

bank_bp = Blueprint("bank", __name__, url_prefix="/bank", template_folder="Templates", static_folder="Static")

logger = logging.getLogger(__name__)

def clean_label(label):
    """Nettoie un libellé pour la comparaison
    - Supprime les espaces en début/fin
    - Met en majuscules
    - Supprime les caractères spéciaux
    - Supprime tous les espaces et retours à la ligne
    - Ne prend que les 50 premiers caractères
    """
    # Convertir en majuscules et supprimer les espaces début/fin
    clean = label.strip().upper()
    # Supprimer les caractères spéciaux sauf les chiffres
    clean = re.sub(r'[^\w\s\d]', ' ', clean)
    # Supprimer tous les espaces et retours à la ligne
    clean = re.sub(r'\s+', '', clean)
    # Ne prendre que les 50 premiers caractères
    clean = clean[:50]
    return clean

@bank_bp.route("/operations")
@login_required
def bank_operations():
    operations = get_all_operations()
    categories = get_all_categories()
    subcategories = get_all_subcategories()
    return render_template(
        "bank_operations.html",
        operations=operations,
        categories=categories,
        subcategories=subcategories
    )

# Category Routes
@bank_bp.route("/api/categories", methods=["POST"])
@login_required
def api_add_category():
    data = request.form.to_dict()
    try:
        category = add_category(data["nom"])
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "Catégorie créée avec succès",
            "category": {
                "id": category.id,
                "nom": category.nom,
                "sous_categories": []
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 400

@bank_bp.route("/api/categories/edit", methods=["POST"])
@login_required
def api_edit_category():
    data = request.form.to_dict()
    try:
        category = update_category(data["id"], data["nom"])
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "Catégorie mise à jour avec succès",
            "category": {
                "id": category.id,
                "nom": category.nom,
                "sous_categories": [{"id": sc.id, "nom": sc.nom} for sc in category.sous_categories]
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 400

@bank_bp.route("/api/categories/<int:category_id>", methods=["DELETE"])
@login_required
def api_delete_category(category_id):
    try:
        delete_category(category_id)
        db.session.commit()
        return jsonify({"success": True, "message": "Catégorie supprimée avec succès"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 400

# SubCategory Routes
@bank_bp.route("/api/subcategories", methods=["POST"])
@login_required
def api_add_subcategory():
    data = request.form.to_dict()
    try:
        subcategory = add_subcategory(data["nom"], data["categorie_id"])
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "Sous-catégorie créée avec succès",
            "subcategory": {
                "id": subcategory.id,
                "nom": subcategory.nom,
                "categorie_id": subcategory.categorie_id
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 400

@bank_bp.route("/api/subcategories/edit", methods=["POST"])
@login_required
def api_edit_subcategory():
    data = request.form.to_dict()
    try:
        subcategory = update_subcategory(data["id"], data["nom"])
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "Sous-catégorie mise à jour avec succès",
            "subcategory": {
                "id": subcategory.id,
                "nom": subcategory.nom,
                "categorie_id": subcategory.categorie_id
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 400

@bank_bp.route("/api/subcategories/<int:subcategory_id>", methods=["DELETE"])
@login_required
def api_delete_subcategory(subcategory_id):
    try:
        delete_subcategory(subcategory_id)
        db.session.commit()
        return jsonify({"success": True, "message": "Sous-catégorie supprimée avec succès"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 400

@bank_bp.route('/api/operations', methods=['POST'])
def api_add_operation():
    try:
        data = request.form
        operation = add_operation(
            date=data.get('date'),
            label=data.get('label'),
            amount=float(data.get('amount')),
            categorie_id=data.get('categorie_id') or None,
            sous_categorie_id=data.get('sous_categorie_id') or None,
            supplier=data.get('supplier') or None,
            person=data.get('person') or None
        )
        return jsonify({
            'success': True,
            'message': 'Opération ajoutée avec succès',
            'operation': {
                'id': operation.id,
                'date': operation.date.isoformat(),
                'label': operation.label,
                'amount': operation.amount,
                'debit': float(operation.debit) if operation.debit else None,
                'credit': float(operation.credit) if operation.credit else None,
                'categorie_id': operation.categorie_id,
                'sous_categorie_id': operation.sous_categorie_id,
                'supplier': operation.supplier,
                'person': operation.person,
                'categorie': {'nom': operation.categorie.nom} if operation.categorie else None,
                'sous_categorie': {'nom': operation.sous_categorie.nom} if operation.sous_categorie else None
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur lors de l\'ajout de l\'opération: {str(e)}'
        }), 400

@bank_bp.route('/api/operations/edit', methods=['POST'])
def api_edit_operation():
    try:
        data = request.form
        operation = update_operation(
            operation_id=data.get('id'),
            date=data.get('date'),
            label=data.get('label'),
            amount=float(data.get('amount')),
            categorie_id=data.get('categorie_id') or None,
            sous_categorie_id=data.get('sous_categorie_id') or None,
            supplier=data.get('supplier') or None,
            person=data.get('person') or None
        )
        return jsonify({
            'success': True,
            'message': 'Opération modifiée avec succès',
            'operation': {
                'id': operation.id,
                'date': operation.date.isoformat(),
                'label': operation.label,
                'amount': operation.amount,
                'debit': float(operation.debit) if operation.debit else None,
                'credit': float(operation.credit) if operation.credit else None,
                'categorie_id': operation.categorie_id,
                'sous_categorie_id': operation.sous_categorie_id,
                'supplier': operation.supplier,
                'person': operation.person,
                'categorie': {'nom': operation.categorie.nom} if operation.categorie else None,
                'sous_categorie': {'nom': operation.sous_categorie.nom} if operation.sous_categorie else None
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur lors de la modification de l\'opération: {str(e)}'
        }), 400

@bank_bp.route('/api/operations/<int:operation_id>', methods=['DELETE'])
def api_delete_operation(operation_id):
    try:
        delete_operation(operation_id)
        return jsonify({
            'success': True,
            'message': 'Opération supprimée avec succès'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur lors de la suppression de l\'opération: {str(e)}'
        }), 400

@bank_bp.route('/api/categories/<int:category_id>/subcategories')
@login_required
def api_get_subcategories(category_id):
    try:
        subcategories = BankSousCategorie.query.filter_by(categorie_id=category_id).all()
        return jsonify([{
            'id': sub.id,
            'nom': sub.nom
        } for sub in subcategories])
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur lors de la récupération des sous-catégories: {str(e)}'
        }), 400

@bank_bp.route('/import', methods=['POST'])
def import_operations():
    try:
        operations = request.get_json()
        print(f"[BANK_ROUTE] Début de l'import de {len(operations)} opérations")
        imported = 0
        
        # Entraîner le modèle si ce n'est pas déjà fait
        if not predictor.is_trained:
            print("[BANK_ROUTE] Entraînement du modèle avant l'import...")
            predictor.train()
            if not predictor.is_trained:
                print("[BANK_ROUTE] Échec de l'entraînement du modèle")
                return jsonify({
                    'success': False,
                    'error': "Impossible d'entraîner le modèle de prédiction"
                }), 500
        
        for op in operations:
            try:
                print(f"[BANK_ROUTE] Traitement de l'opération: {op['libelle']}")
                # Prédire la catégorie et sous-catégorie
                predicted_cat, predicted_sub = predictor.predict(op['libelle'])
                
                # Si une prédiction est faite, l'utiliser
                if predicted_cat:
                    op['categorie_id'] = predicted_cat
                    op['sous_categorie_id'] = predicted_sub
                    print(f"[BANK_ROUTE] Prédiction utilisée pour '{op['libelle']}': catégorie {predicted_cat}, sous-catégorie {predicted_sub}")
                else:
                    print(f"[BANK_ROUTE] Aucune prédiction pour '{op['libelle']}'")
                
                # Vérification et conversion des données
                date = datetime.strptime(op['date'], '%Y-%m-%d').date()
                montant = float(op['montant'])
                categorie_id = int(op['categorie_id']) if op['categorie_id'] else None
                sous_categorie_id = int(op['sous_categorie_id']) if op['sous_categorie_id'] else None
                
                # Vérification de la cohérence des catégories
                if sous_categorie_id and not categorie_id:
                    print(f"[BANK_ROUTE] Opération ignorée: sous-catégorie sans catégorie pour '{op['libelle']}'")
                    continue
                
                if sous_categorie_id:
                    sous_categorie = BankSousCategorie.query.get(sous_categorie_id)
                    if not sous_categorie or sous_categorie.categorie_id != categorie_id:
                        print(f"[BANK_ROUTE] Opération ignorée: incohérence catégorie/sous-catégorie pour '{op['libelle']}'")
                        continue
                
                add_operation(
                    date=date,
                    label=op['libelle'],
                    amount=montant,
                    categorie_id=categorie_id,
                    sous_categorie_id=sous_categorie_id,
                    supplier=op['fournisseur'],
                    person=op['personne']
                )
                
                # Apprendre de la nouvelle opération si elle a été catégorisée
                if categorie_id:
                    predictor.learn(op['libelle'], categorie_id, sous_categorie_id)
                
                imported += 1
                print(f"[BANK_ROUTE] Opération importée avec succès: {op['libelle']}")
            except Exception as e:
                print(f"[BANK_ROUTE] Erreur lors de l'import d'une opération: {str(e)}")
                continue
        
        print(f"[BANK_ROUTE] Import terminé: {imported}/{len(operations)} opérations importées")
        return jsonify({
            'success': True,
            'imported': imported,
            'total': len(operations)
        })
        
    except Exception as e:
        print(f"[BANK_ROUTE] Erreur lors de l'import: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bank_bp.route('/api/operations/check', methods=['POST'])
@login_required
def check_operations():
    try:
        operations = request.get_json()
        existing_operations = []
        
        for op in operations:
            # Nettoyer le libellé pour la comparaison
            clean_label_op = clean_label(op['libelle'])
            
            # Convertir la date
            op_date = datetime.strptime(op['date'], '%Y-%m-%d')
            
            # Rechercher les opérations similaires dans une fenêtre de 3 jours
            existing = BankOperation.query.filter(
                BankOperation.date.between(
                    op_date - timedelta(days=3),
                    op_date + timedelta(days=3)
                ),
                BankOperation.amount == op['montant']
            ).all()
            
            # Vérifier si une des opérations correspond au libellé
            for e in existing:
                if clean_label(e.label) == clean_label_op:
                    existing_operations.append({
                        'date': op['date'],
                        'libelle': op['libelle'],
                        'montant': op['montant'],
                        'existing_date': e.date.strftime('%Y-%m-%d'),
                        'existing_label': e.label
                    })
                    break
        
        return jsonify({
            'success': True,
            'existing_operations': existing_operations
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bank_bp.route('/api/categories', methods=['GET', 'POST'])
def api_categories():
    if request.method == 'GET':
        categories = get_all_categories()
        return jsonify([{
            'id': cat.id,
            'nom': cat.nom,
            'sous_categories': [{
                'id': sub.id,
                'nom': sub.nom
            } for sub in cat.sous_categories]
        } for cat in categories])
    elif request.method == 'POST':
        nom = request.form.get('nom')
        if not nom:
            return jsonify({'success': False, 'message': 'Le nom est requis'}), 400
        try:
            categorie = add_category(nom)
            return jsonify({
                'success': True,
                'message': 'Catégorie créée avec succès',
                'category': {
                    'id': categorie.id,
                    'nom': categorie.nom,
                    'sous_categories': []
                }
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
