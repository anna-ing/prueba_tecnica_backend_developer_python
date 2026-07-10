from sqlalchemy import Column, Integer, String, Text, Date, Numeric
from src.databases.base_class import Base


class CbamImport(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    eori_number = Column(String(17), nullable=False)
    declarant_legal_name = Column(String(255), nullable=False)
    declarant_address = Column(Text, nullable=False)
    contact_person = Column(String(255), nullable=False)
    competent_authority = Column(String(100), nullable=False)
    cbam_account_number = Column(String(100), nullable=False)
    data_owner = Column(String(255), nullable=False)
    taric_code = Column(String(10))
    cn_code = Column(String(8), nullable=False)
    goods_description = Column(Text, nullable=False)
    sector_category = Column(String(100), nullable=False)
    product_type = Column(String(20), nullable=False)
    import_volume = Column(Numeric(12, 2), nullable=False)
    date_of_importation = Column(Date, nullable=False)
    country_of_origin = Column(String(100), nullable=False)
    customs_declaration_ref = Column(String(100), nullable=False)
    supplier_name = Column(String(255), nullable=False)
    notes_comments = Column(Text)