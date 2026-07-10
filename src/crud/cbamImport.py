from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from src.models.cbamImport import CbamImport


def create_import(db: Session, row):
    """
    Crea un nuevo registro CBAM en la base de datos a partir de una fila de Excel.
    Retorna el registro creado.
    """
    # Convertir la fecha correctamente
    date_value = row["Date of importation"]
    if isinstance(date_value, str):
        date_value = datetime.strptime(date_value, "%Y-%m-%d").date()
    elif hasattr(date_value, 'date'):  # Si es un objeto datetime
        date_value = date_value.date()

    cbam = CbamImport(
        eori_number=row["EORI Number"],
        declarant_legal_name=row["Declarant Legal Name"],
        declarant_address=row["Declarant Address"],
        contact_person=row["Contact Person"],
        competent_authority=row["Competent Authority"],
        cbam_account_number=row["CBAM Account Number"],
        data_owner=row["Data Owner"],
        taric_code=row["TARIC Code"],
        cn_code=row["CN Code"],
        goods_description=row["Goods Description"],
        sector_category=row["Sector Category"],
        product_type=row["Product Type"],
        import_volume=row["Import Volume"],
        date_of_importation=date_value,
        country_of_origin=row["Country of Origin"],
        customs_declaration_ref=row["Customs Declaration Ref"],
        supplier_name=row["Supplier Name"],
        notes_comments=row["Notes / Comments"]
    )

    db.add(cbam)
    db.commit()
    db.refresh(cbam)
    return cbam


def get_imports(db: Session, skip: int = 0, limit: int = 10):
    """
    Obtiene una lista de registros CBAM con paginación, ordenados por ID descendente.
    Retorna el total de registros y la lista.
    """
    total = db.query(func.count(CbamImport.id)).scalar()
    records = db.query(CbamImport).order_by(CbamImport.id.desc()).offset(skip).limit(limit).all()
    return total, records


def count_imports(db: Session):
    """
    Cuenta el total de registros CBAM en la base de datos.
    """
    return db.query(func.count(CbamImport.id)).scalar()
