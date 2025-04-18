from models.database import db
from datetime import datetime

class BankCategorie(db.Model):
    __tablename__ = "bank_categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)

    sous_categories = db.relationship(
        "BankSousCategorie",
        backref="categorie",
        cascade="all, delete-orphan"
    )


class BankSousCategorie(db.Model):
    __tablename__ = "bank_sous_categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    categorie_id = db.Column(db.Integer, db.ForeignKey("bank_categories.id"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('categorie_id', 'nom', name='uq_bank_categorie_souscat'),
    )


class BankOperation(db.Model):
    __tablename__ = "bank_operations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    label = db.Column(db.Text, nullable=False)
    debit = db.Column(db.Numeric(10, 2), nullable=True)
    credit = db.Column(db.Numeric(10, 2), nullable=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    categorie_id = db.Column(db.Integer, db.ForeignKey("bank_categories.id"), nullable=True)
    sous_categorie_id = db.Column(db.Integer, db.ForeignKey("bank_sous_categories.id"), nullable=True)
    supplier = db.Column(db.String(100), nullable=True)
    person = db.Column(db.String(50), nullable=True)
    source_file = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    categorie = db.relationship("BankCategorie", lazy="joined", foreign_keys=[categorie_id])
    sous_categorie = db.relationship("BankSousCategorie", lazy="joined", foreign_keys=[sous_categorie_id])
