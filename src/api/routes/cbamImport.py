from fastapi import APIRouter, UploadFile, File, Depends, Query
from sqlalchemy.orm import Session

from src.databases.session import get_db
from src.services.cbamImport import process_excel, list_imports

router = APIRouter(
    prefix="/cbam",
    tags=["CBAM"]
)


@router.post("/upload")
async def upload_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Endpoint para subir y procesar un archivo Excel con registros CBAM.
    """
    total = process_excel(file, db)

    return {
        "message": "Archivo cargado correctamente.",
        "rows_imported": total
    }

@router.get("")
def get_cbam_imports(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener una lista paginada de registros CBAM.
    """
    return list_imports(
        db=db,
        page=page,
        size=size
    )
