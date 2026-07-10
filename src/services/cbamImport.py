from fastapi import UploadFile, HTTPException
from openpyxl import load_workbook
import pandas as pd
from io import BytesIO
from sqlalchemy.orm import Session

from src.crud.cbamImport import create_import, get_imports
from src.services.validators import validate_row

EXPECTED_HEADERS = [
    "EORI Number",
    "Declarant Legal Name",
    "Declarant Address",
    "Contact Person",
    "Competent Authority",
    "CBAM Account Number",
    "Data Owner",
    "TARIC Code",
    "CN Code",
    "Goods Description",
    "Sector Category",
    "Product Type",
    "Import Volume",
    "Date of importation",
    "Country of Origin",
    "Customs Declaration Ref",
    "Supplier Name",
    "Notes / Comments",
]


def validate_excel(file: UploadFile):
    """
    Valida que un archivo sea un Excel válido (.xlsx).
    Levanta una excepción HTTP 400 si la validación falla.
    """
    # Validar extensión
    if not file.filename.lower().endswith(".xlsx"):
        raise HTTPException(
            status_code=400,
            detail="El archivo debe tener extensión .xlsx"
        )

    # Validar que realmente sea un Excel
    try:
        # Leer el contenido del archivo en memoria
        content = file.file.read()
        file.file.seek(0)  # Reiniciar el puntero
        load_workbook(BytesIO(content))
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="El archivo Excel está corrupto o no es válido."
        )


def validate_headers(headers):
    """
    Valida que los encabezados del Excel coincidan con el formato esperado.
    Levanta una excepción HTTP 400 si hay encabezados faltantes o extra.
    """
    missing = [h for h in EXPECTED_HEADERS if h not in headers]
    extra = [h for h in headers if h not in EXPECTED_HEADERS]

    if missing or extra:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Los encabezados del archivo no corresponden al template.",
                "missing_columns": missing,
                "extra_columns": extra
            }
        )


def process_excel(file: UploadFile, db: Session):
    """
    Procesa un archivo Excel y guarda los registros válidos en la base de datos.
    Retorna un diccionario con el resumen del procesamiento.
    """
    # 1. Validar el archivo
    validate_excel(file)

    # 2. Leer el Excel en un buffer para evitar problemas con el objeto UploadFile
    file_content = file.file.read()
    file.file.seek(0)  # Reiniciar el puntero por si acaso
    excel_buffer = BytesIO(file_content)
    dataframe = pd.read_excel(excel_buffer)

    # 3. Validar encabezados
    validate_headers(list(dataframe.columns))

    total_rows = len(dataframe)
    valid_rows = 0
    invalid_rows = 0
    errors = []

    for index, row in dataframe.iterrows():
        row_errors = validate_row(row, index + 2)

        if row_errors:
            invalid_rows += 1
            errors.extend(row_errors)
        else:
            create_import(db, row)
            valid_rows += 1

    return {
        "total_rows": total_rows,
        "valid_rows": valid_rows,
        "invalid_rows": invalid_rows,
        "errors": errors
    }


def list_imports(db: Session, page: int = 1, size: int = 10):
    """
    Obtiene una lista paginada de registros CBAM desde la base de datos.
    """
    skip = (page - 1) * size
    total, records = get_imports(
        db=db,
        skip=skip,
        limit=size
    )

    return {
        "page": page,
        "size": size,
        "total": total,
        "total_pages": (total + size - 1) // size,
        "data": records
    } 